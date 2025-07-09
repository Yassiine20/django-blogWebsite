from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core import paginator
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import ListView

from .forms import CommentForm, LoginForm, PostForm, RegisterForm
from .models import Category, Comment, Post
from .serializers import (
    BlogSerializer,
    CategorySerializer,
    CommentSerializer,
    PostSerializer,
    RegisterSerializer,
)


# Blog list view: displays posts, handles category filter, search, pagination, and comment submission.
@login_required
def blog_list(request):
    # Get filter and search parameters from the request.
    category_id = request.GET.get("category")
    search_query = request.GET.get("search", "")
    # Query all posts, order by publication date descending.
    posts = Post.objects.all().order_by("-publication_date")  # type: ignore[attr-defined]
    if category_id:
        # Filter posts by selected category.
        posts = posts.filter(category_id=category_id)
    if search_query:
        # Filter posts by search query in title or content.
        posts = posts.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )
    # Get all categories for the filter dropdown.
    categories = Category.objects.all()  # type: ignore[attr-defined]
    # Paginate posts (10 per page).
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    comment_form = CommentForm()
    if request.method == "POST":
        # Handle new comment submission.
        post_id = request.POST.get("post_id")
        content = request.POST.get("content")
        if post_id and content:
            post = get_object_or_404(Post, pk=post_id)
            Comment.objects.create(post=post, author=request.user.username, content=content)  # type: ignore[attr-defined]
            return redirect("blog_list")
    # Render the blog list template with context.
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


# View for creating a new blog post (HTML and API).
class CreatePostView(CreateAPIView):
    """View for creating a new blog post (HTML and API)."""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blogapp/create_post.html"

    def get(self, request, *args, **kwargs):
        # Display the empty post creation form.
        form = PostForm()
        return Response({"form": form}, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        # Handle post creation form submission.
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("blog_list")
        return Response({"form": form}, template_name=self.template_name)


# View for user registration via HTML form.
class RegisterFormView(APIView):
    """View for user registration via HTML form."""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blogapp/register.html"

    def get(self, request, *args, **kwargs):
        # Display the empty registration form.
        form = RegisterForm()
        return Response({"form": form}, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        # Handle registration form submission.
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            auth_login(request, user)
            return redirect("blog_list")
        return Response({"form": form}, template_name=self.template_name)


# View for user login via HTML form.
class LoginFormView(APIView):
    """View for user login via HTML form."""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blogapp/login.html"

    def get(self, request, *args, **kwargs):
        # Display the empty login form.
        form = LoginForm()
        return Response({"form": form}, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        # Handle login form submission.
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("blog_list")
        return Response({"form": form}, template_name=self.template_name)


# View for logging out the user.
def logout_view(request):
    logout(request)
    return redirect("login")


# View for displaying the user's profile and their posts.
@login_required
def profile_view(request):
    user_posts = Post.objects.filter(user=request.user).order_by("-publication_date")  # type: ignore[attr-defined]
    return render(
        request,
        "blogapp/profile.html",
        {"user": request.user, "user_posts": user_posts},
    )


# View for changing the user's password via HTML form.
class ChangePasswordView(APIView):
    """View for changing user password via HTML form."""
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blogapp/change_password.html"

    def get(self, request, *args, **kwargs):
        # Display the empty password change form.
        form = PasswordChangeForm(request.user)
        return Response({"form": form}, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        # Handle password change form submission.
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("profile")
        return Response({"form": form}, template_name=self.template_name)


# View for displaying a single blog post and its comments (HTML and API).
class PostDetailView(RetrieveAPIView):
    """View for displaying a single blog post and its comments (HTML and API)."""
    queryset = Post.objects.all()  # type: ignore[attr-defined]
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blogapp/post_detail.html"

    def get(self, request, *args, **kwargs):
        # Display the post detail page with comments and comment form.
        post = self.get_object()
        comments = post.comments.all().order_by("-created_at")
        form = CommentForm()
        return Response(
            {"post": post, "comments": comments, "form": form},
            template_name=self.template_name,
        )

    def post(self, request, *args, **kwargs):
        # Handle new comment submission on the post detail page.
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


# API viewset for CRUD operations on blog posts.
class PostViewSet(viewsets.ModelViewSet):
    """API viewset for CRUD operations on blog posts."""
    queryset = Post.objects.all().order_by("-publication_date")  # type: ignore[attr-defined]
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the user as the creator of the post.
        serializer.save(user=self.request.user)


# API viewset for CRUD operations on categories.
class CategoryViewSet(viewsets.ModelViewSet):
    """API viewset for CRUD operations on categories."""
    queryset = Category.objects.all()  # type: ignore[attr-defined]
    serializer_class = CategorySerializer


# API viewset for CRUD operations on comments.
class CommentViewSet(viewsets.ModelViewSet):
    """API viewset for CRUD operations on comments."""
    queryset = Comment.objects.all().order_by("-created_at")  # type: ignore[attr-defined]
    serializer_class = CommentSerializer


# API view for user registration.
class RegisterView(APIView):
    """API view for user registration."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Handle user registration via API.
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for deleting a post (only by the owner).
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return HttpResponseForbidden(b"You are not allowed to delete this post.")
    post.delete()
    return redirect("profile")


# View for updating a post (only by the owner).
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


# Root redirect view: sends authenticated users to the blog list, others to login.
def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("blog_list")
    else:
        return redirect("login")


# View for liking or unliking a post by the current user.
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get("HTTP_REFERER", "blog_list"))


# API view for paginated list of blogs.
class BlogsPaginatedView(APIView):
    
    def get(self, request):
        
        page_number = request.GET.get("page")
        all_blogs = Post.objects.all().order_by("-publication_date")  # type: ignore[attr-defined]
        paginator = Paginator(all_blogs, 1)
        page_blogs = paginator.get_page(page_number)
        serializer = BlogSerializer(page_blogs, many=True)
        
        return Response({
            'total': paginator.count,
            'blogs': serializer.data,
            'current_page': page_blogs.number,
        })
        