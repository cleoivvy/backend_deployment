from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, api_view
from  django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import *
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django import dispatch
from .models import *
from config.weather import process_weather
from django.utils.text import slugify
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin

# Create your views here.

User = get_user_model()

data_signal = dispatch.Signal()


class UserViewSet(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer
    queryset = User.objects.filter().order_by('-date_joined')
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    serach_fields = ['first_name', 'last_name', 'email', 'role', 'password']
    
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            try:
                User.objects.create_user(**serializer.validated_data)
            except Exception as e:
                return Response({'error': str(e)}, status=400)
            
            data = {
                "message": "User created successfully"
            }   
            
            return Response(data, status=200)
        return Response(serializer.errors) 
    
class LoginView(APIView):
    @swagger_auto_schema(method="post", request_body=LoginSerializer)
    @action(detail=True, methods=['post'])
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, email=serializer.validated_data['email'],
                                password = serializer.validated_data['password'])
            if user:
                try:
                    refresh_token = RefreshToken.for_user(user)
                    
                    data = {}
                    data['id'] = user.pk
                    data['first_name'] = user.first_name
                    data['last_name'] = user.last_name
                    data['access_token'] = str(refresh_token.access_token)
                    data['refresh_token'] = str(refresh_token)
                    
                    
                    return Response(data, status=200)
                except Exception as error:
                    return Response(
                        {
                            "error": f"{error}"
                        },
                        status=400
                    )
            else:
                
                data = {
                    "error": "invalid login credentials"
                }  
                return Response(data, status=401)
        else:
            data = {
                "error": serializer.errors
            }   
            return Response(data, status=400)   
        
class LogoutView(APIView):

        @swagger_auto_schema(method="post", request_body=LogoutSerializer)
        @action(detail=True, methods=['post'])
        def post(self, request):
            serializer = LogoutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            try:
                
                token = RefreshToken(token=serializer._validated_data['refresh_token'])
                token.blacklist()
            
                
                return Response({"message": "logout successful"}, status=200)
            except Exception as error:
                print(error)
                return Response({"error": "failed to blacklist token"}, status=400)
            
            
            
class WeatherUpdateView(APIView):
    
    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        
        query = request.GET.get('query', None)
        
        if query is None:
            all_weather = WeatherUpdate.objects.all().order_by('-created_at')
            return Response(WeatherUpdateSerializer(all_weather, many=True).data, status=200)
        
        data, status = process_weather(query)
        
        if status == True:
            
            slug = slugify(data['location']['name'])
            
            try:
                weather = WeatherUpdate.objects.get(slug=slug)
                weather.location = data['location']
                weather.current = data['current'] 
                weather.save()
                
                return Response(WeatherUpdateSerializer(weather).data, status=200)
            
            except WeatherUpdate.DoesNotExist:
                
                weather = WeatherUpdate.objects.create(
                    country = data['location']['name'],
                    location=data['location'],
                    current=data['current']
                )
                
                return Response(WeatherUpdateSerializer(weather).data, status=200)
            
        else:
            return Response(data, status=400)
                    
                            

