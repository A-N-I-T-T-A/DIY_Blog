from .models import Blog

def recent_posts(request):
    recent_posts = Blog.objects.all().order_by('-post_date')[:5]
    return {'recent_posts': recent_posts} 