from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse
from config.utils import format_errors, success_response, created_response
from .serializers import RegisterSerializer, LoginSerializer


@extend_schema(
    request=RegisterSerializer,
    responses={201: OpenApiResponse(description='User registered successfully')},
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return created_response('User registered successfully', {
            'user': {'id': user.id, 'email': user.email, 'name': user.name},
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })
    return Response(format_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LoginSerializer,
    responses={200: OpenApiResponse(description='Login successful')},
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return success_response('Login successful', {
            'user': {'id': user.id, 'email': user.email, 'name': user.name},
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })
    return Response(format_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
