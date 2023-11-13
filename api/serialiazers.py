# authentication/serializers.py
from rest_framework import serializers
from .models import CUser, PersonalContact, SpamNumber

class PersonalContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalContact
        fields = ('id', 'name', 'phone_number', 'email')
        read_only_fields = ['id']

class DetailedPersonSerializer(serializers.ModelSerializer):
    spam_likelihood = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = PersonalContact
        fields = ['name', 'phone_number', 'email', 'spam_likelihood']

    def get_spam_likelihood(self, obj):
        return SpamNumber.objects.filter(phone_number=obj.phone_number).count()

    def get_email(self, obj):
        # Check if the person is a registered user and the searching user is in the contact list
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            searching_user = request.user
            if searching_user.personal_contacts.filter(phone_number=obj.phone_number).exists():
                return obj.email
        return None

    def to_representation(self, instance):
        if isinstance(instance, CUser):
            return {
                'name': instance.name,
                'phone_number': instance.phone_number,
                'email': instance.email,
                'spam_likelihood': 0,  # Adjust accordingly if needed
            }
        elif isinstance(instance, PersonalContact):
            return super().to_representation(instance)

        raise ValueError("Unexpected instance type in DetailedPersonSerializer")

class CustomUserSerializer(serializers.ModelSerializer):
    personal_contacts = PersonalContactSerializer(many=True, read_only=True)
    
    class Meta:
        model = CUser
        fields = ('id', 'phone_number', 'name', 'email', 'password', 'personal_contacts')
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CUser
        fields = ['id', 'name', 'phone_number', 'email',]
    
    
class SpamNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamNumber
        fields = ['id', 'phone_number', 'name', 'email', 'spam_likelihood']
        read_only_fields = ['id']
    


