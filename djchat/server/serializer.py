from rest_framework import serializers

from .models import Server, Channel, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ChannelSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    channel_server = ChannelSerialiazer(many=True)

    class Meta:
        model = Server
        fields = "__all__"
