from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib import auth
from django.conf import settings
# import misaka

from groups.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()



# class User(auth.models.User, auth.models.PermissionsMixin):

#     def __str__(self):
#         return "@{}".format(self.username)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null = True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(is_approved = True)


    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class PostGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postsgroup')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='postsgroup', null=True, blank='True' )


    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('single', kwargs={'username':self.user.username, 'pk':self.pk}) 
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name= 'comments')
    author = models.CharField(max_length=150)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    def approve(self):
        self.is_approved = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text