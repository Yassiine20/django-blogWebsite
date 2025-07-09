from django.conf import settings
from django.db import models

# Create your models here.


# Model representing a category for blog posts.
class Category(models.Model):
    """Represents a post category for organizing blog posts."""
    # Name of the category (must be unique).
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        # Add model metadata options here (ordering, verbose_name, etc.)
        pass

    def __str__(self):
        # Return the category name as its string representation.
        return self.name


# Model representing a blog post created by a user.
class Post(models.Model):
    """Represents a blog post created by a user."""
    # Title of the post.
    title = models.CharField(max_length=200)
    # Content of the post.
    content = models.TextField()
    # Date and time when the post was published.
    publication_date = models.DateTimeField(auto_now_add=True)
    # Category to which the post belongs.
    category = models.ForeignKey(
        Category, related_name="posts", on_delete=models.CASCADE
    )
    # User who created the post.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE
    )
    # Optional image for the post.
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    # Users who liked this post.
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True
    )

    class Meta:
        # Add model metadata options here (ordering, verbose_name, etc.)
        pass

    def __str__(self):
        # Return the post title as its string representation.
        return self.title


# Model representing a comment made by a user on a blog post.
class Comment(models.Model):
    """Represents a comment made by a user on a blog post."""
    # The post this comment is associated with.
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    # Author of the comment.
    author = models.CharField(max_length=100)
    # Content of the comment.
    content = models.TextField()
    # Date and time when the comment was created.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Add model metadata options here (ordering, verbose_name, etc.)
        pass

    def __str__(self):
        # Return a string representation of the comment.
        return f"Comment by {self.author} on {self.post.title}"  # type: ignore
