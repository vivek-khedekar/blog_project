from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer, ProfileSerializer


class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        data.update({
            "username": user.username,
            "email": user.email,
            "role": user.role
        })
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


from .serializers import UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False           # deactivate until verified
        user.save()

        # ✅ Generate verification token (JWT)
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        # ✅ Construct verification URL
        verify_url = f"http://127.0.0.1:8000/api/auth/verify-email/?token={token}"

        # ✅ Send email
        send_mail(
            subject="Verify your email address",
            message=f"Hi {user.username}, click the link to verify your email:\n{verify_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Account created successfully. Check your email to verify your account."},
            status=status.HTTP_201_CREATED
        )



class VerifyEmailView(APIView):
    """
    This view activates a user account when they click the verification link.
    Example:  GET /api/auth/verify-email/?token=<token>
    """
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return Response({"error": "Token missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode the token and get the user id
            access_token = AccessToken(token)
            user_id = access_token['user_id']

            # Get the user and verify them
            user = User.objects.get(id=user_id)
            if user.is_verified:
                return Response({"message": "Email already verified."}, status=status.HTTP_200_OK)

            user.is_verified = True
            user.is_active = True
            user.save()

            return Response({"message": "Email verified successfully! You can now log in."},
                            status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": "Invalid or expired token."},
                            status=status.HTTP_400_BAD_REQUEST)
class LogoutView(APIView):
    """
    This API blacklists the user's refresh token (logout).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # ✅ invalidate the token
            return Response({"message": "Logged out successfully!"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response({"error": "Invalid token or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.soft_delete()
        return Response(
            {"message": "Your account has been deactivated (soft deleted)."},
            status=status.HTTP_200_OK
        )
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "profile_image": request.build_absolute_uri(user.profile_image.url) if user.profile_image else None
        }
        return Response(data)

    def put(self, request):
        user = request.user
        data = request.data

        # username should NOT be changeable
        if "username" in data:
            return Response({"error": "Username cannot be changed!"}, status=400)

        # update allowed fields
        if "email" in data:
            user.email = data["email"]

        if "role" in data:
            user.role = data["role"]

        if "profile_image" in request.FILES:
            user.profile_image = request.FILES["profile_image"]

        user.save()

        return Response({"message": "Profile updated successfully!"})
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=200)

        return Response(serializer.errors, status=400)

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
