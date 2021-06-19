from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id',"title",'slug','status')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',"username",'password')


class PostingSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        return {
            'score': obj.id,
            'player_name': obj.title
        }


class InventorySerializer(serializers.ModelSerializer):
    kits = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='count'
        )

    class Meta:
        model = Inventory
        fields = ('name','kits')

class Human:
    def __init__(self,name,age):
        self.name = name
        self.age = age

class HumanSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=18)
    age = serializers.IntegerField(default=0)

