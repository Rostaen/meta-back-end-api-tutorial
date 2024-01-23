from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from .models import BookItem
from .serializers import BookItemSerializer
# from .throttles import TenCallsPerMinute

@api_view(['GET', 'POST'])
def books(request):
    return Response('list of the books', status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def book_items(request):
    if request.method == 'GET': # GETting from the database
        #variable declarations
        items = BookItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)

        # Filtered view of the database
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price) # lte = less than or equal to
        if search:
            items = items.filter(title__icontains=search) #icontains will find the characters anywhere in the title
        if ordering: # Currently there is a bug where multifield ordering is returning an error. Working on this bug.
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        # Querying the database with supplied or default values
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        # Serializing the view
        serialized_item = BookItemSerializer(items, many=True)
        return Response(serialized_item.data)

    if request.method == 'POST': # Adding to the database
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

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "Some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message": "You are a manager. Only Managers Should See This!"})
    else:
        return Response({"message": "You are not authorized"}, 403)

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "successful"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({"message": "message for the logged in users only"})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({"message": "Ok"})

    return Response({"message": "Error"}, status.HTTP_400_BAD_REQUEST)
