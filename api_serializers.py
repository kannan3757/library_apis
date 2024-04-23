from rest_framework import serializers
from library_details.models import Books,Users,Transaction

class TransactionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Transaction
    fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = Users
    fields = ['name']

class BooksSerializer(serializers.ModelSerializer):
  class Meta:
    model = Books
    fields = '__all__'

class BooksUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Books
    fields = ['quantity']


class BooksGetSerializer(serializers.ModelSerializer):
  class Meta:
    model = Books
    fields = ['name','author']


class BooksIntegrateSerializer(serializers.Serializer):
  search = serializers.CharField()
  page = serializers.IntegerField()
  book_limit = serializers.IntegerField(max_value=32)