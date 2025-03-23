
from datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.core.mail import send_mail

from jwt import decode as jwt_decode
from DjangoProject.token.custom_token import (
    CustomTokenObtainPairSerializer
)
from rest_framework.exceptions import (
    AuthenticationFailed
)

from accounts.models import VerificationCode

User = get_user_model()



class ResendCodeSerializer(serializers.Serializer):
    """
    Serializer for resending verification codes or password reset emails.
    """
    email = serializers.EmailField()
    FLAG_TYPE = (
        ("email", "Email Verification"),
        ("password", "Forgot Password"),
    )
    flag = serializers.ChoiceField(choices=FLAG_TYPE)

    def validate(self, data):
        """
        Validates the input data and raises appropriate ValidationErrors if there are any issues.
        Raises:
            serializers.ValidationError: If the email or flag field is missing or if the user does not exist.
        """
        email = data.get("email")
        flag = data.get("flag")

        # Check that email is not missing
        if not email:
            raise serializers.ValidationError("Email is required.")

        # Check that flag is not missing
        if not flag:
            raise serializers.ValidationError("Flag is required.")

        # Check that user exists
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")
        
        # remove any other verification codes
        VerificationCode.objects.filter(user=user).delete()
        code = VerificationCode.objects.create(user=user)
        # Handle email verification
        if flag == "email":
            if user.is_verified:
                raise serializers.ValidationError("Email is already verified.")
            # Send verification email
            send_mail(
                "Email Verification",
                f"Your verification code is {code.code}",
                "K5V0V@example.com",
                [email],
                fail_silently=False,
            )
            pass

        # Handle password reset
        elif flag == "password":
            if not user.is_verified:
                raise serializers.ValidationError("Email is not verified.")
            # Send password reset email
            pass

        return data

    def to_representation(self, instance):
        return {"message": "Verification code sent successfully"}



class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True) 
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
            "gender",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }
        
    
    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError("Email is required.")
        email = email.lower()
        return email

    def validate(self, attrs: dict):
        password = attrs.get('password', None)
        password2 = attrs.pop('password2', None)
        email = attrs.get('email', None)
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists.")

        if not password or not password2:
            raise serializers.ValidationError("Password is required.")
        if password != password2:
            raise serializers.ValidationError("Password fields didn't match.")
        
        return attrs

    def create(self, validated_data: dict):
        instance =  super().create(validated_data)
        # TODO : send verification email
        data = {
            "email": instance.email,
            "flag": "email"
        }
        try:
            ResendCodeSerializer(data=data).is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation




class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)

    def validate_email(self, email: str):
        email = email.lower()
        return email
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User with this email does not exist")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect authentication credentials.")

        if not user.is_active:
            raise serializers.ValidationError("Your account is suspended. Please contact support.")

        if not user.is_verified:
            raise serializers.ValidationError("Email is not verified. Please verify your email.")
        
        attrs["user"] = user
        return attrs

    def to_representation(self, instance):
        user = self.validated_data.get("user")
        token = CustomTokenObtainPairSerializer.get_token(user)

        representation = {
            "first_name": user.first_name if user.first_name else "",
            "last_name": user.last_name if user.last_name else "",
            "refresh": str(token),
            "access": str(token.access_token),
            "is_onboarded": user.is_onboarded
        }
        return representation




class ValidateCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
    FLAG_TYPE = (
        ("email", "Email Verification"),
        ("password", "Forgot Password"),
    )
    flag = serializers.ChoiceField(choices=FLAG_TYPE)  # Flag to determin which template and subject to send
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def validate(self, data: dict):
        code = data.get('code')
        flag = data.get('flag')

        if not flag:
            raise serializers.ValidationError("Flag is required.")

        if not code:
            raise serializers.ValidationError("Code is required.")

        verify_code = VerificationCode.objects.filter(code=code).first()

        if not verify_code:
            raise serializers.ValidationError("Incorrect code. Try again please.")


        add_hour = verify_code.created_at + timedelta(hours=1)

        if add_hour.replace(tzinfo=None) < datetime.now():
            raise serializers.ValidationError("Code is expired.")
        user = User.objects.filter(id=verify_code.user.id).first()
        if user:
            if flag == "email":
                # TODO : send welcome email
                pass
            if not user.is_verified:
                # todo : send verification email
                user.is_verified = True
                user.save()
        return data

    def to_representation(self, instance):
        code = instance.get('code')
        verify_code = VerificationCode.objects.filter(code=code).first()
        token = CustomTokenObtainPairSerializer.get_token(verify_code.user)
        verify_code.delete() # delete the code
        return {
            "message": "Code has been validated successfully",
            "refresh": str(token),
            "access": str(token.access_token),
        }




class SocialLoginSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_onboarded = serializers.BooleanField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    def validate(self, data):
        token = data.get('token')
        if not token:
            raise serializers.ValidationError("Token is required.")
        
        decoded_data = self.decode_auth0_token(token)
        
        if not data:
            raise serializers.ValidationError("Invalid token.")

        email = decoded_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            if not user.is_verified:
                user.is_verified = True
                user.save()
        else:
            # create user
            account = {
                "first_name": decoded_data.get('given_name'),
                "last_name": decoded_data.get('family_name'),
                "email": email,
            }
            user = User.objects.create_user(**account)
            user.is_verified = True
            user.save()

        token = CustomTokenObtainPairSerializer.get_token(user)
        return {
            "refresh": str(token),
            "access": str(token.access_token),
            "is_verified": user.is_verified,
            "is_onboarded": user.is_onboarded,
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        
    def decode_auth0_token(self, token):
        try:
            decoded = jwt_decode(token, options={"verify_signature": False})
            return decoded
        except Exception as e:
            print(f"Manual decode failed: {e}")
            return None
        
