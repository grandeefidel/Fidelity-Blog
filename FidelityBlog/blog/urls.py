from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

# app_name= 'blog'

urlpatterns = [
    path("", views.PostListView.as_view(), name='post_list'),
    path('accounts/login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('about/', views.AboutView.as_view(),name='about'),
    path('test/', views.TestView.as_view(),name='test'),
    path('thanks/', views.ThanksView.as_view(),name='thanks'),
    path("post/<int:pk>", views.PostDetailView.as_view(), name="post_detail"),
    path("createpost/", views.CreatePostView.as_view(), name="create_post"),
    path("updatepost/<int:pk>", views.PostUpdateView.as_view(), name="post_edit"), 
    path("deletepost/<int:pk>", views.PostDeleteView.as_view(), name="delete_post"),
    path("drafts/", views.DraftListView.as_view(), name="post_draft_list"),
    path("comment/<int:pk>", views.add_comment_to_post, name="add_comment_to_post"),
    path("approve_comment/<int:pk>", views.approve_comment, name="approve_comment"),
    path("delete_comment/<int:pk>", views.delete_comment, name="delete_comment"),
    path("publish_post/<int:pk>", views.publish_post, name="publish_post"),
    path("post_group/", views.PostList.as_view(), name="all"),
    path("new_group_post/", views.CreatePost.as_view(), name="create"),
    path("by/<username>", views.UserPosts.as_view(), name="for_user"),
    path("by/<username>/<int:pk>", views.PostDetail.as_view(), name="single"),
    path("delete/<int:pk>", views.DeletePost.as_view(), name="delete"),
]