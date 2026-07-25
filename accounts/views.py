from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import RegisterSerializer, LoginSerializer


def format_errors(errors):
    if isinstance(errors, dict):
        if 'non_field_errors' in errors:
            return {'error': errors['non_field_errors'][0]}
        return {'errors': {k: [str(e) for e in v] if isinstance(v, list) else str(v) for k, v in errors.items()}}
    return {'error': str(errors)}


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
        return Response({
            'message': 'User registered successfully',
            'user': {'id': user.id, 'email': user.email, 'name': user.name},
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)
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
        return Response({
            'message': 'Login successful',
            'user': {'id': user.id, 'email': user.email, 'name': user.name},
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })
    return Response(format_errors(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
