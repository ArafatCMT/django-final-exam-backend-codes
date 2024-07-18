from rest_framework import serializers
from posts.models import Post
class PostSerializer(serializers.ModelSerializer):
    # account = serializers.StringRelatedField(many=False)
    class Meta:
        model = Post
        fields = ['id', 'account', 'image_url', 'description', 'created_on']
        read_only_fields = ["account",]