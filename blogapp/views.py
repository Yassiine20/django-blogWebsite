from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import permissions, status, viewsets
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CommentForm, LoginForm, PostForm, RegisterForm
from .models import Category, Comment, Post
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    PostSerializer,
    RegisterSerializer,
)


# Blog list (HTML)
@login_required
def blog_list(request):
    category_id = request.GET.get("category")
    search_query = request.GET.get("search", "")
    posts = Post.objects.all().order_by("-publication_date")  # type: ignore[attr-defined]
    if category_id:
        posts = posts.filter(category_id=category_id)
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )
    categories = Category.objects.all()  # type: ignore[attr-defined]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    comment_form = CommentForm()
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        content = request.POST.get("content")
        if post_id and content:
            post = get_object_or_404(Post, pk=post_id)
            Comment.objects.create(post=post, author=request.user.username, content=content)  # type: ignore[attr-defined]
            return redirect("blog_list")
    return render(
        request,
        "blogapp/blog_list.html",
        {
            "posts": page_obj.object_list,
            "page_obj": page_obj,
            "comment_form": comment_form,
            "categories": categories,
            "selected_category": category_id,
            "search_query": search_query,
        },
    )


# Create post (HTML)
class CreatePostView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blogapp/create_post.html"

    def get(self, request, *args, **kwargs):
        form = PostForm()
        return Response({"form": form}, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("blog_list")
        return Response({"form": form}, template_name=self.template_name)


# Register (HTML)
class RegisterFormView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blogapp/register.html"

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return Response({"form": form}, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            auth_login(request, user)
            return redirect("blog_list")
        return Response({"form": form}, template_name=self.template_name)


# Login (HTML)
class LoginFormView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blogapp/login.html"

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return Response({"form": form}, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("blog_list")
        return Response({"form": form}, template_name=self.template_name)


# Logout (HTML)
def logout_view(request):
    logout(request)
    return redirect("login")


# Profile (HTML)
@login_required
def profile_view(request):
    user_posts = Post.objects.filter(user=request.user).order_by("-publication_date")  # type: ignore[attr-defined]
    return render(
        request,
        "blogapp/profile.html",
        {"user": request.user, "user_posts": user_posts},
    )


# Change password (HTML)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blogapp/change_password.html"

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return Response({"form": form}, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("profile")
        return Response({"form": form}, template_name=self.template_name)


# Post detail (HTML)
class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()  # type: ignore[attr-defined]
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blogapp/post_detail.html"

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        comments = post.comments.all().order_by("-created_at")
        form = CommentForm()
        return Response(
            {"post": post, "comments": comments, "form": form},
            template_name=self.template_name,
        )

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("post_detail", pk=post.pk)
        comments = post.comments.all().order_by("-created_at")
        return Response(
            {"post": post, "comments": comments, "form": form},
            template_name=self.template_name,
        )


# --- API (DRF) ---


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-publication_date")  # type: ignore[attr-defined]
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()  # type: ignore[attr-defined]
    serializer_class = CategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")  # type: ignore[attr-defined]
    serializer_class = CommentSerializer


# API registration
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return HttpResponseForbidden(b"You are not allowed to delete this post.")
    post.delete()
    return redirect("profile")


@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return HttpResponseForbidden(b"You are not allowed to edit this post.")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = PostForm(instance=post)
    return render(
        request,
        "blogapp/create_post.html",
        {"form": form, "update": True, "post": post},
    )


# --- Root redirect view ---
def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("blog_list")
    else:
        return redirect("login")


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get("HTTP_REFERER", "blog_list"))
