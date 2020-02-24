from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Post, Comment,PostGroup
from django.urls import reverse_lazy
from .forms import PostForm, CommentForm, UserForm, GroupPostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView,CreateView, UpdateView, DeleteView, ListView)
from django.http import Http404
from braces.views import SelectRelatedMixin
from django.contrib import messages
from . import forms
# from . import models 


User = get_user_model()

class SignUp(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class TestView(TemplateView):
    template_name = 'test.html'

class ThanksView(TemplateView):
    template_name = 'thanks.html'

class IndexView(TemplateView):
    template_name = 'post_list.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    template_name = 'post_list.html'

class PostDetailView(DetailView):
    model = Post
    
class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('created_date')

    # template_name = 'post_draft_list.html'

@login_required
def publish_post(request, pk):
    print(f"pk: {pk}")
    post =get_object_or_404(Post,pk = pk)
    post.publish()
    return redirect('post_detail', pk= pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = CommentForm()
        return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def approve_comment(request, pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk = comment.post.pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    redirect('post_detail', pk=post_pk)



class PostList(SelectRelatedMixin, ListView):
    model = PostGroup
    select_related = ("user", "group")
    template_name = "blog/group_post_list.html"

class UserPosts(ListView):
    model = PostGroup
    template_name = "blog/group_user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("postsgroup").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin,DetailView):
    model = PostGroup
    select_related = ("user", "group")
    template_name = "blog/group_post_detail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, CreateView):
    fields = ('message', 'group')
    model = PostGroup
    # form_class = GroupPostForm
    template_name = "blog/group_post_form.html"


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, DeleteView):
    model = PostGroup
    select_related = ("user", "group")
    success_url = reverse_lazy("all")
    template_name = "blog/group_post_confirm_delete.html"


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)