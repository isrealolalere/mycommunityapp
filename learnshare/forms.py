from django import forms
from .models import Post, CATEGORY_CHOICES, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class CategoryForm(forms.Form):
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        label='',
        widget=forms.Select(attrs={
        'class': 'form-control custom-select cat-form w-50',
        'placeholder': 'Filter by'
        })
    )

class NewPost(forms.ModelForm):
    # summary = forms.CharField(widget=forms.Textarea(attrs={
    #     'class': 'summary-field'
    # }))


    # def __init__(self, *args, **kwargs):
    #     super(NewPost, self).__init__(*args, **kwargs)
    #     self.fields['summary'].widget.attrs['class'] = 'summary-field'

    class Meta:
        model = Post
        fields = ['image', 'title', 'category', 'summary', 'content']
        widgets = {
            'summary': forms.Textarea(attrs={
                'class': 'sum',
                'rows': '4',
            })
        }

class SignUpForm(UserCreationForm):
    profile_img = forms.ImageField()

    class Meta:
        model = User
        fields = ['profile_img', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UpdateProfileForm(UserChangeForm):
    profile_img = forms.ImageField()

    class Meta:
        model = User
        fields = ['profile_img', 'username', 'first_name', 'last_name', 'email',]


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
        'placeholder': 'Username',
        'class': 'mb-2 border border-rounded border-primary',
        }
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
        'placeholder': 'Password',
        'class': 'mt-2 border border-rounded border-primary',
        }
    ))
    

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter comment', 'id': 'comment'}), required= True, label='')

    class Meta:
        model = Comment
        fields = ['body']


class UpdateCommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter comment', 'id': 'comment'}), required= True, label='')

    class Meta:
        model = Comment
        fields = ['body']