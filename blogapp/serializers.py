from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, Comment, Post


# Serializer for Category model objects.
class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model objects."""
    class Meta:
        model = Category
        fields = ["id", "name"]


# Serializer for Comment model objects.
class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model objects."""
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at"]


# Serializer for Post model objects, including related comments and category.
class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model objects, including related comments and category."""
    # Nested serializer for comments (read-only).
    comments = CommentSerializer(many=True, read_only=True)
    # Nested serializer for category (read-only).
    category = CategorySerializer(read_only=True)
    # Field for writing the category by primary key.
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True  # type: ignore
    )
    # String representation of the user (read-only).
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "publication_date",
            "category",
            "category_id",
            "comments",
            "user",
        ]


# Serializer for user registration.
class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    # Password field (write-only).
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email")

    def create(self, validated_data):
        # Create a new user with the provided username, email, and password.
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "publication_date", "category", "comments", "user"]