from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from .models import Blog, Blogger, Comment
from .forms import SimpleUserCreationForm, BlogForm

# Create your views here.

def custom_logout(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = SimpleUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a Blogger profile for the new user
            Blogger.objects.create(user=user)
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('login')
    else:
        form = SimpleUserCreationForm()
    
    # Add Bootstrap classes to form fields
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    
    return render(request, 'registration/register.html', {'form': form})

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blog_list'
    paginate_by = 5

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.all()
        return context

class BloggerListView(ListView):
    model = Blogger
    template_name = 'blog/blogger_list.html'
    context_object_name = 'blogger_list'

class BloggerDetailView(DetailView):
    model = Blogger
    template_name = 'blog/blogger_detail.html'
    context_object_name = 'blogger'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_list'] = self.object.blog_set.all()
        return context

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']
    template_name = 'blog/comment_form.html'
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return super().form_valid(form)

class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user.blogger
        return super().form_valid(form)

class BlogUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user.blogger
        return super().form_valid(form)

    def test_func(self):
        blog = self.get_object()
        return self.request.user.blogger == blog.author

class BlogDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blogs')
    template_name = 'blog/blog_confirm_delete.html'

    def test_func(self):
        blog = self.get_object()
        return self.request.user.blogger == blog.author

class BloggerUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blogger
    fields = ['bio', 'profile_picture']
    template_name = 'blog/blogger_form.html'

    def test_func(self):
        blogger = self.get_object()
        return self.request.user == blogger.user

    def get_success_url(self):
        return reverse_lazy('blogger-detail', kwargs={'pk': self.object.pk})

class CommentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['text']
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('blog-detail', kwargs={'pk': self.object.blog.pk})

class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('blog-detail', kwargs={'pk': self.object.blog.pk})
