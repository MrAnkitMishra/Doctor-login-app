from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Blog
from .forms import BlogForm

# List all published blogs (for patients)
def blog_list(request):
    category = request.GET.get("category")
    if category:
        blogs = Blog.objects.filter(is_draft=False, category=category).order_by("-created_at")
    else:
        blogs = Blog.objects.filter(is_draft=False).order_by("-created_at")
    return render(request, "blog/blog_list.html", {"blogs": blogs, "category": category})


# Create blog (only doctors)
@login_required
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.doctor = request.user
            blog.save()
            return redirect("my_blogs")
    else:
        form = BlogForm()
    return render(request, "blog/blog_form.html", {"form": form})


# Doctor can see their own blogs
@login_required
def my_blogs(request):
    blogs = Blog.objects.filter(doctor=request.user).order_by("-created_at")
    return render(request, "blog/my_blogs.html", {"blogs": blogs})
