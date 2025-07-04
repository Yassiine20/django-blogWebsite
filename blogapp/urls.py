from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet, CategoryViewSet, CommentViewSet, RegisterView,
    logout_view, profile_view, CreatePostView,
    blog_list, RegisterFormView, LoginFormView, ChangePasswordView, PostDetailView, delete_post, update_post
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('create/', CreatePostView.as_view(), name='create_post'),
    path('register/', RegisterView.as_view(), name='register'),  # API registration
    path('register-form/', RegisterFormView.as_view(), name='register_form'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('delete-post/<int:pk>/', delete_post, name='delete_post'),
    path('update-post/<int:pk>/', update_post, name='update_post'),
]

urlpatterns += router.urls 