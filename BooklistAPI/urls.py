from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('books/', views.books)
    path('books', views.Booklist.as_view()),
    path('books/<int:pk>', views.Book.as_view()),
    path('book-items/', views.book_items),
    path('book-items/<int:id>', views.single_item),
    path('secret/', views.secret),
    path('api-token-auth/', obtain_auth_token),
    path('manager-view/', views.manager_view),
    path('throttle-check', views.throttle_check),
    path('throttle-check-auth', views.throttle_check_auth),
]
