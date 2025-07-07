from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CategoryViewSet, ChangePasswordView, CommentViewSet,
                    CreatePostView, LoginFormView, PostDetailView, PostViewSet,
                    RegisterFormView, RegisterView, blog_list, delete_post,
                    like_post, logout_view, profile_view, root_redirect,
                    update_post)

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = [
    path("", root_redirect, name="root_redirect"),
    path("home/", blog_list, name="blog_list"),
    path("create/", CreatePostView.as_view(), name="create_post"),
    path("register/", RegisterView.as_view(), name="register"),  # API registration
    path("register-form/", RegisterFormView.as_view(), name="register_form"),
    path("login/", LoginFormView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("delete-post/<int:pk>/", delete_post, name="delete_post"),
    path("update-post/<int:pk>/", update_post, name="update_post"),
    path("like-post/<int:pk>/", like_post, name="like_post"),
]

urlpatterns += router.urls
