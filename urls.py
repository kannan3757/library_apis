from django.urls import path
from library_details.v1.api_details import (TransactionView,ReturnBooksView,
                                            BooksGetView,BooksUpdateView,BooksView,
                                            UserView,UserUpdateView,IntegrateView)

from . import views

app_name = 'library_details'
urlpatterns = [
    path("/transaction",TransactionView.as_view()),
    path("/return_book/<int:transaction_id>",ReturnBooksView.as_view()),
    path("/books",BooksGetView.as_view()),
    path("/add_books",BooksView.as_view()),
    path("/books/<int:book_id>",BooksUpdateView.as_view()),
    path("/user/<int:user_id>",UserUpdateView.as_view()),
    path("/user",UserView.as_view()),
    path("/integrate_books",IntegrateView.as_view()),
    

]