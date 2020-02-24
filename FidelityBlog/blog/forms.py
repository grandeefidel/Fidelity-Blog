from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from blog.models import Post, Comment, PostGroup
from . import models



class UserForm(UserCreationForm):

    class meta():
        fields = ('username', 'email', 'password', 'password2',)
        model = get_user_model()

    email = forms.EmailField(required=True, label = 'Email Address')


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email Address'
    


class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text' )

        widgets ={
            'author': forms.Select(attrs= {'class': 'textinputclass custom-select rounded-0'}),
            'title': forms.TextInput(attrs= {'class': 'textinputclass form-control  rounded-0'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea post-content'})
        }


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets={
            'author': forms.TextInput(attrs={'class': 'textinputclass form-control rounded-0'}),
            'text':forms.Textarea(attrs={'class': 'editable medium-editor-textarea comment-content'})
        }


class GroupPostForm(forms.ModelForm):
    class Meta:
        fields = ("message", "group")
        model = PostGroup

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["group"].queryset = (
                models.Group.objects.filter(
                    pk__in=user.groups.values_list("group__pk")
                )
            )

