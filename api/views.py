from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CUser, PersonalContact, SpamNumber
from .serialiazers import (
    CustomUserSerializer,
    LoginSerializer,
    UserSerializer,
    PersonalContactSerializer,
    SpamNumberSerializer,
    DetailedPersonSerializer)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SignUpAPIView(generics.CreateAPIView):
    queryset = CUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def perform_create(self, serializer):
            hashed_password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = hashed_password

            
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
            serializer.data['tokens'] = data


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
       
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']

        user = CUser.objects.filter(phone_number=phone_number).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            data = {'access': str(refresh.access_token), 'refresh': str(refresh)}
            return Response(data, status=status.HTTP_200_OK)
        else:
            print("Invalid credentials")
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
      
# List Users For HELPING PURPOSE
class UserListAPIView(generics.ListAPIView):
    queryset = CUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated] 

class PersonalContactListCreateView(generics.ListCreateAPIView):
    queryset = PersonalContact.objects.all()
    serializer_class = PersonalContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PersonalContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonalContact.objects.all()
    serializer_class = DetailedPersonSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class MarkSpamNumberAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=SpamNumberSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SpamNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']

        # Check if the number is already marked as spam
        if SpamNumber.objects.filter(phone_number=phone_number).exists():
            return Response({'detail': 'Number is already marked as spam'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new SpamNumber entry
        SpamNumber.objects.create(
            phone_number=phone_number,
            name=serializer.validated_data.get('name'),
            email=serializer.validated_data.get('email'),
            spam_likelihood=serializer.validated_data.get('spam_likelihood', 0)
        )

        return Response({'detail': 'Number marked as spam'}, status=status.HTTP_201_CREATED)

# FOR HELPING PURPOSE
class ListSpamNumbersAPIView(generics.ListAPIView):
    queryset = SpamNumber.objects.all()
    serializer_class = SpamNumberSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class SearchByNameAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING),
        ],
        responses={200: DetailedPersonSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')

        # Search by name in PersonalContact model
        name_starting_with_query_personal = PersonalContact.objects.filter(name__istartswith=query)
        name_containing_query_personal = PersonalContact.objects.filter(name__icontains=query).exclude(id__in=name_starting_with_query_personal)

        # Search by name in CUser model
        name_starting_with_query_user = CUser.objects.filter(name__istartswith=query)
        name_containing_query_user = CUser.objects.filter(name__icontains=query).exclude(id__in=name_starting_with_query_user)

        # Combine results
        name_results_personal = name_starting_with_query_personal | name_containing_query_personal
        name_results_user = name_starting_with_query_user | name_containing_query_user

        # Combine both results from PersonalContact and CUser
        name_results = list(name_results_personal) + list(name_results_user)
        
        # Serialize the combined results
        name_results_serializer = DetailedPersonSerializer(name_results, many=True)
        
        return Response(name_results_serializer.data, status=status.HTTP_200_OK)



class SearchByPhoneNumberAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING),
        ],
        responses={200: DetailedPersonSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')

        # Check if there is a registered user with the provided phone number
        user_with_phone_number = CUser.objects.filter(phone_number=query).first()

        if user_with_phone_number:
            # If there is a registered user, show only that result
            result_serializer = DetailedPersonSerializer(user_with_phone_number, many=False)
            return Response([result_serializer.data], status=status.HTTP_200_OK)
        else:
            # If there is no registered user, show all results matching the phone number completely
            phone_results_starting_with_query = PersonalContact.objects.filter(phone_number__istartswith=query)
            phone_results_containing_query = PersonalContact.objects.filter(phone_number__icontains=query).exclude(id__in=phone_results_starting_with_query)

            phone_results = phone_results_starting_with_query | phone_results_containing_query
            phone_results_serializer = DetailedPersonSerializer(phone_results, many=True)
            
            return Response(phone_results_serializer.data, status=status.HTTP_200_OK)
