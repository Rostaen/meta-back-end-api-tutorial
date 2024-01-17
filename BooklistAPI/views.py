from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import BookItem
from .serializers import BookItemSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
def books(request):
    return Response('list of the books', status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def book_items(request):
    if request.method == 'GET':
        items = BookItem.objects.select_related('category').all()
        serialized_item = BookItemSerializer(items, many=True)
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = BookItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)

@api_view()
def single_item(request, id):
    item = get_object_or_404(BookItem, pk=id)
    serialized_item = BookItemSerializer(item)
    return Response(serialized_item.data)

class Booklist(APIView):
    def get(self, request):
        author = request.GET.get('author')
        if(author):
            return Response({"message": "list of the books by " + author}, status.HTTP_200_OK)
        return Response({"message": "list of the books"}, status.HTTP_200_OK)

    def post(self, request):
        return Response({"message": "new book created"}, status.HTTP_201_CREATED)

class Book(APIView):
    def get(self, request, pk):
        return Response({"message": "single books with id " + str(pk)}, status.HTTP_200_OK)

    def put(self, request, pk):
        return Response({"title": request.data.get('title')}, status.HTTP_200_OK)
