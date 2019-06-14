from rest_framework import serializers


class Category3Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()