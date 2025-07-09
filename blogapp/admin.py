# Register Category, Comment, and Post models with the Django admin site.
from django.contrib import admin

from .models import Category, Comment, Post

# Register the Category model.
admin.site.register(Category)
# Register the Comment model.
admin.site.register(Comment)
# Register the Post model.
admin.site.register(Post)
