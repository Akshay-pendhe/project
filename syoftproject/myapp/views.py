from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Product,User
from .serializers import ProductSerializer

# Create your views here.

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    user = authenticate(request, username=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    if request.user.role != 'admin':
        return Response({'error': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.user.role not in ['admin', 'manager']:
        return Response({'error': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.user.role not in ['admin', 'manager']:
        return Response({'error': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.user.role != 'admin':
        return Response({'error': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)

    product.delete()
    return Response({'message': 'Product deleted successfully'}, status=status.HTTP_200_OK)













