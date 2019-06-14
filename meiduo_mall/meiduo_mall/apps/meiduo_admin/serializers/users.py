import re

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        min_length=5,
        max_length=20,
        error_messages={
            'min_length': '用户名是5到20位数字、字母或下划线',
            'max_length': '用户名是5到20位数字、字母或下划线',
        }
    )
    mobile = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate_username(self,attr):
        if not re.match('^[a-zA-Z0-9_]{5,20}$', attr):
            raise serializers.ValidationError('用户名只能包含数字、字母或下划线')
        if User.objects.filter(username=attr).count()>0:
            raise serializers.ValidationError('用户名重复')
        return attr

    def validate_mobile(self, attr):
        # 格式
        if not re.match(r'^1[3-9]\d{9}$', attr):
            raise serializers.ValidationError('手机号格式错误')

        # 是否重复
        if User.objects.filter(mobile=attr).count() > 0:
            raise serializers.ValidationError('手机号重复')

        return attr

    def validate(self, attrs):
        # 密码格式
        password = attrs.get('password')
        if not re.match(r'^[a-zA-Z0-9_!@#$%^&*]{8,20}$', password):
            raise serializers.ValidationError('密码是8到20位数字、字母或下划线以及特殊!@#$%^&*符号')

        return attrs

    def create(self, validated_data):
        # 创建用户对象
        user = User.objects.create_user(**validated_data)
        return user

