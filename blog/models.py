from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, help_text="Enter your bio details here.", blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', blank=True)

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])

    def __str__(self):
        return self.user.username

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Blogger, on_delete=models.CASCADE)
    content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-post_date']

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    post_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['post_date']

    def __str__(self):
        len_title = 75
        if len(self.text) > len_title:
            string_val = self.text[:len_title] + '...'
        else:
            string_val = self.text
        return string_val
