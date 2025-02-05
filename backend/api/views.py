from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Item
from .serializers import ItemSerializer

# ViewSets --> Groups together common API actions (CRUD) for a model or resource

class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer