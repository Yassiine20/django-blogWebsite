from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterForm, LoginForm, PostForm, CommentForm
from .models import Post, Category, Comment
from rest_framework import viewsets
from .serializers import PostSerializer, CategorySerializer, CommentSerializer, RegisterSerializer
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

# Blog list (HTML)
@login_required
def blog_list(request):
    posts = Post.objects.all().order_by('-publication_date')  # type: ignore[attr-defined]
    comment_form = CommentForm()
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        if post_id and content:
            post = get_object_or_404(Post, pk=post_id)
            Comment.objects.create(post=post, author=request.user.username, content=content) #type: ignore
            return redirect('blog_list')
    return render(request, 'blogapp/blog_list.html', {'posts': posts, 'comment_form': comment_form})

# Create post (HTML)
@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog_list')
    else:
        form = PostForm()
    return render(request, 'blogapp/create_post.html', {'form': form})

# Register (HTML)
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'blogapp/register.html', {'form': form})

# Login (HTML)
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'blogapp/login.html', {'form': form})

# Logout (HTML)
def logout_view(request):
    logout(request)
    return redirect('login')

# Profile (HTML)
@login_required
def profile_view(request):
    return render(request, 'blogapp/profile.html', {'user': request.user})

# Change password (HTML)
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'blogapp/change_password.html', {'form': form})

# Post detail (HTML)
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blogapp/post_detail.html', {'post': post, 'comments': comments, 'form': form})

# --- API (DRF) ---

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-publication_date')  # type: ignore[attr-defined]
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()  # type: ignore[attr-defined]
    serializer_class = CategorySerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')  # type: ignore[attr-defined]
    serializer_class = CommentSerializer

# API registration
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
