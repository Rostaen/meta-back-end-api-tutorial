from django.urls import path
from . import views

urlpatterns = [
    # path('books/', views.books)
    path('books', views.Booklist.as_view()),
    path('books/<int:pk>', views.Book.as_view()),
    path('book-items/', views.book_items),
    path('book-items/<int:id>', views.single_item)
]
