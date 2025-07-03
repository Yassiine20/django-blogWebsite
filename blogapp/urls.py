from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet, CategoryViewSet, CommentViewSet, blog_list, RegisterView,
    register_view, login_view, logout_view, profile_view, create_post_view,
    change_password_view, post_detail
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('create/', create_post_view, name='create_post'),
    path('register/', RegisterView.as_view(), name='register'),  # API registration
    path('register-form/', register_view, name='register_form'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', change_password_view, name='change_password'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
]

urlpatterns += router.urls 