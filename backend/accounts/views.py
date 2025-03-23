
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from accounts.serializers import CreateUserSerializer, ResendCodeSerializer, UserLoginSerializer, ValidateCodeSerializer, SocialLoginSerializer
from accounts.models import VerificationCode
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView

UserModel = get_user_model()


class UserCreationAPIView(generics.CreateAPIView):
    """
    View for creating users
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer
    queryset = UserModel
    


class LoginAPIView(generics.GenericAPIView):
    """
    View for logging in users
    """
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh", None)
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success":True,"detail": "Token Blacklisted."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        




class ResendCodeView(generics.GenericAPIView):
    permission_classes = [ permissions.AllowAny ]
    serializer_class = ResendCodeSerializer
    queryset = VerificationCode
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ValidateCodeAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ValidateCodeSerializer

    def post(self, request):
        '''
        Validate the verification code
        '''
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    




class RefreshUserTokenAPIView(TokenRefreshView):
    "Custom token refresher to check whether user is active or no before issuing a new token"
    permission_classes = [ permissions.AllowAny ]
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        # Decode the token to get the user ID
        try:
            refresh = RefreshToken(data['refresh'])
            # Attempt to parse the token's user ID
            user_id = refresh['user_id']
            # Retrieve the user and check if they are active
            user = UserModel.objects.get(id=user_id)
            if not user.is_active:
                return Response({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
        except (KeyError, UserModel.DoesNotExist, InvalidToken, TokenError):
            return Response({'error': 'Invalid token or user does not exist.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    



class SocialLoginView(generics.GenericAPIView):
    permission_classes = [ permissions.AllowAny ]
    serializer_class = SocialLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)