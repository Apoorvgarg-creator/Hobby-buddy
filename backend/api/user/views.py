from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UsersSerializer, LoginSerializer
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status_code'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Request latency in seconds', ['method', 'endpoint'])

def monitor_request(func):
    """Decorator to monitor request count and latency."""
    def wrapper(request, *args, **kwargs):
        start_time = time.time()
        response = func(request, *args, **kwargs)
        duration = time.time() - start_time
        REQUEST_COUNT.labels(method=request.method, endpoint=request.path, status_code=response.status_code).inc()
        REQUEST_LATENCY.labels(method=request.method, endpoint=request.path).observe(duration)
        return response
    return wrapper

class UserCreateAPIView(APIView):
    
    @monitor_request
    def post(self, request, *args, **kwargs):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserLoginAPIView(APIView):

    @monitor_request
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({"message": "Login successful", "username": user.username}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def metrics(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)