from rest_framework import serializers
from .models import Customer, Tests, Booking, Phlabo
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class TestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tests
        fields = ['id', 'testName', 'testCode', 'price']

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password')

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name')


class PhlaboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phlabo
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class TestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tests
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    phlabo = PhlaboSerializer()
    tests = TestsSerializer(many=True)

    class Meta:
        model = Booking
        fields = '__all__'