# authentication/urls.py
from django.urls import path
from .views import (
    SignUpAPIView,
    LoginAPIView,
    UserListAPIView,
    PersonalContactListCreateView,
    PersonalContactDetailView,
    MarkSpamNumberAPIView,
    ListSpamNumbersAPIView,
    SearchByNameAPIView,
    SearchByPhoneNumberAPIView
    )

urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('personal-contacts/', PersonalContactListCreateView.as_view(), name='personal-contact-list-create'),
    path('personal-contacts/<int:pk>/', PersonalContactDetailView.as_view(), name='personal-contact-detail'),
    path('mark-spam/', MarkSpamNumberAPIView.as_view(), name='mark-spam'),
    path('list-spam/', ListSpamNumbersAPIView.as_view(), name='list-spam'),
    path('search/name/', SearchByNameAPIView.as_view(), name='search-by-name'),
    path('search/phone/', SearchByPhoneNumberAPIView.as_view(), name='search-by-phone')
]
