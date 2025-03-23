from django.db import models

from DjangoProject.constants import GENDERS
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
import random



class BaseModel(models.Model):
    """
    Abstract base model for all models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """
    Custom user manager for User model.
    """

    def create_user(self, email, first_name, last_name, password=None, password2=None):
        """
        Creates and saves a User with the given email, first_name, last_name and password.
        """
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, first_name, last_name and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_superuser = True
        user.is_verified = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(BaseModel, AbstractUser):

    email = models.EmailField(max_length=255, unique=True, help_text="Email address")
    username = None
    ton_wallet_address = models.TextField(null=True, blank=True)
    
    # Technicall
    is_verified = models.BooleanField(
        default=False, help_text="Whether the user has verified their email address"
    )
    is_onboarded = models.BooleanField(
        default=False, help_text="Whether the user has completed the onboarding process"
    )
    gender = models.CharField(
        max_length=50,
        choices=GENDERS,
        blank=True,
        null=True,
        help_text="Enter your gender",
    )
    
    date_of_birth = models.DateField(
        null=True, blank=True, help_text="Enter your date of birth"
    )
    
    location = models.CharField(
        max_length=100, blank=True, null=True, help_text="Enter your location"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of the User object.
        """
        return self.email

    def get_full_name(self):
        """
        Returns the full name of the User.
        """
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """
        Returns the short name of the User.
        """
        return self.first_name




class UserProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="Select a user",
    )
    bio = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Write a short bio about yourself",
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        help_text="Upload your profile picture",
    )
    country_code = models.CharField(
        max_length=5, blank=True, null=True, help_text="Enter your country code"
    )
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, help_text="Enter your phone number"
    )
    language_preference = models.CharField(
        max_length=50, blank=True, null=True, help_text="Enter your preferred language"
    )
    timezone = models.CharField(
        max_length=50, blank=True, null=True, help_text="Enter your timezone"
    )
    

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "Users Profiles"

    def __str__(self):
        return self.user.get_full_name()




class VerificationCode(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User",
        help_text="The user to whom this verification code belongs.",
    )
    code = models.CharField(
        max_length=99,
        verbose_name="Verification Code",
        help_text="The actual code sent to the user for verification.",
    )
    
    class Meta:
        verbose_name = "Verification Code"
        verbose_name_plural = "Verification Codes"
        
    def generate_code(self):
        code = random.randint(11112, 99999)
        while VerificationCode.objects.filter(code=code).exists():
            code = random.randint(11112, 99999)
        return code
    
    def save(self, *args, **kwargs):
        self.code = self.generate_code()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.code} used to verify for user {self.user.first_name}"