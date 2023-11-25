from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import uuid
generated_uuid = str(uuid.uuid4())


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(phone_number, password, **extra_fields)

class CUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(unique=True, max_length=10)
    email = models.EmailField(blank=True, null=True)
    is_superuser = models.BooleanField(default= False)
    is_staff = models.BooleanField(default= False)
    
    

    objects = CustomUserManager()
    
    def has_perm(self, perm, obj=None):
        # This method is required by Django's admin
        return self.is_staff

    def has_module_perms(self, app_label):
        # This method is required by Django's admin
        return self.is_staff

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return str(self.id)
    
class PersonalContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    user = models.ForeignKey('CUser', on_delete=models.CASCADE, related_name='personal_contacts')
    
    def __str__(self):
        return self.name
    
class SpamNumber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    spam_likelihood = models.IntegerField(default=0)
    

    def __str__(self):
        return self.phone_number