import requests
import json
from rest_framework import generics
from rest_framework import status,exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from library_details.models import Books,Users,Transaction
from datetime import datetime
from library_details.v1.api_serializers import (TransactionSerializer,
									UserSerializer,BooksSerializer,BooksUpdateSerializer,BooksGetSerializer,
									BooksIntegrateSerializer)

class TransactionView(generics.GenericAPIView):
	def post(self,request):
		try:
			serializer = TransactionSerializer(data = request.data)
			if serializer.is_valid():
				user = Users.objects.get(id = request.data.get('users'))
				if user.outstanding_amount > 500:
					return Response({"message":"User outstanding amount is more and not eligible to take a book"},status = status.HTTP_400_BAD_REQUEST)
				else:
					serializer.save()
					return Response({"message":"Books issued successfully"},status = status.HTTP_201_CREATED)
			else:
				result = serializer.errors
				return Response({"message":result},status = status.HTTP_400_BAD_REQUEST)
		except Exception as ex:
			return Response({"message":str(ex)},status = status.HTTP_400_BAD_REQUEST)
		
class TransactionGETView(generics.GenericAPIView):
		
	def get(self,request,user_id):
		try:
			transactions = Transaction.objects.filter(users_id = user_id).values()
			return Response(transactions,status = status.HTTP_200_OK)
			
		except Exception as ex:
			return Response({"message":str(ex)},status = status.HTTP_400_BAD_REQUEST)

class ReturnBooksView(generics.GenericAPIView):
	def put(self,request,transaction_id):
		try:
			transaction_obj = Transaction.objects.get(id = transaction_id)
			transaction_obj.return_on = datetime.today()
			transaction_obj.save()
			return Response({"message":"Books returned successfully"},status = status.HTTP_200_OK)
		except Transaction.DoesNotExist:
			return Response({"message":"No record found"},status = status.HTTP_404_NOT_FOUND)


class BooksGetView(generics.GenericAPIView):

	serializer_class = BooksGetSerializer
	def get(self,request):
		try:
			name = request.data.get('name')
			author = request.data.get('author')
			books = Books.objects.filter()
			if name:
				books = books.filter(name = name).values()
			if author:
				books = books.filter(author=author).values()
			return Response(books,status = status.HTTP_200_OK)
		except Exception as ex:
			return Response({"message":str(ex)},status = status.HTTP_400_BAD_REQUEST)
		
class BooksView(generics.GenericAPIView):

	def post(self,request):
		try:
			serializer = BooksSerializer(data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response({"message":"Book created successfully"},status = status.HTTP_200_OK)
			else:
				result = serializer.errors
				return Response({"message":result},status = status.HTTP_400_BAD_REQUEST)

		except Exception as ex:
			return Response({"message":str(ex)},status = status.HTTP_400_BAD_REQUEST)

class BooksUpdateView(generics.APIView):
	serializer_class = BooksUpdateSerializer
	def put(self,request,book_id):
		try:
			serializer = BooksUpdateSerializer(data = request.data)
			if serializer.is_valid():
				books_obj = Books.objects.get(id = book_id)
				books_obj.quantity = request.data.get('quantity')
				books_obj.save()
				return Response({"message":"Quantity updated successfully"},status = status.HTTP_200_OK)
			else:
				result = serializer.errors
				return Response({"message":result},status = status.HTTP_400_BAD_REQUEST)

		except Exception as ex:
			return Response({"message":str(ex)},status = status.HTTP_400_BAD_REQUEST)
		
	def delete(self,request,book_id):
		try:
				books_obj = Books.objects.get(id = book_id)
				books_obj.delete()
				return Response({"message":"Book deleted successfully"},status = status.HTTP_200_OK)

		except Exception as ex:
			return Response({"message":str(ex)},status = status.HTTP_400_BAD_REQUEST)
		

class UserView(generics.GenericAPIView):

	def post(self,request):
		try:
			serializer = UserSerializer(data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response({"message":"Member created successfully"},status = status.HTTP_200_OK)
			else:
				result = serializer.errors
				return Response({"message":result},status = status.HTTP_400_BAD_REQUEST)

		except Exception as ex:
			return Response({"message":str(ex)},status = status.HTTP_400_BAD_REQUEST)
		
	def get(self,request):
		try:
			user = Users.objects.filter().values
			return Response(user,status = status.HTTP_200_OK)
		except Exception as ex:
			return Response({"message":str(ex)},status = status.HTTP_400_BAD_REQUEST)
		

class UserUpdateView(generics.GenericAPIView):

	def put(self,request,user_id):
		try:
			user_obj = Users.objects.get(id = user_id)
			serializer = UserSerializer(data = request.data,instance = user_obj)
			if serializer.is_valid():
				serializer.save()
				return Response({"message":"User updated successfully"},status = status.HTTP_200_OK)
			else:
				result = serializer.errors
				return Response({"message":result},status = status.HTTP_400_BAD_REQUEST)
			
		except Users.DoesNotExist:
			return Response({"message":"User not found"},status = status.HTTP_400_BAD_REQUEST)

		except Exception as ex:
			return Response({"message":str(ex)},status = status.HTTP_400_BAD_REQUEST)
		
	def delete(self,request,user_id):
		try:
				books_obj = Users.objects.get(id = user_id)
				books_obj.delete()
				return Response({"message":"User deleted successfully"},status = status.HTTP_200_OK)

		except Users.DoesNotExist:
			return Response({"message":"User not found"},status = status.HTTP_400_BAD_REQUEST)

		except Exception as ex:
			return Response({"message":str(ex)},status = status.HTTP_400_BAD_REQUEST)
		

class IntegrateView(generics.APIView):

	serializer_class = BooksIntegrateSerializer

	def post(self,request):
		try:
			search = request.data.get('author')
			page = request.data.get('page')
			if page and search:
				url = "https://gutendex.com/books/?page="+page+"&search="+search
			elif page:
				url = "https://gutendex.com/books/?page="+page
			elif search:
				url = "https://gutendex.com/books/?search="+search
			else:
				url = "https://gutendex.com/books"
			header = {
				"content-type": "application/json"
			}
			response = requests.get(url,headers=header)
			if response.ok:
				books = json.loads(response.content)


		except Exception as ex:
			return Response({"message":str(ex)},status = status.HTTP_400_BAD_REQUEST)
		
