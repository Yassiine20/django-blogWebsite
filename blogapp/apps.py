# App configuration for the blogapp application.
from django.apps import AppConfig

# BlogappConfig sets the default configuration for the blogapp Django app.
class BlogappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blogapp"
