from django.shortcuts import render

# Create your views here.
from http.client import HTTPResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Post, Like, Comment, User_info
from .forms import NewPost, SignUpForm, LoginForm, CategoryForm, CommentForm, UpdateProfileForm, UpdateCommentForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required


def home(request):

    if isinstance(request.user, AnonymousUser):
        user_info = ""
    else:
        user_info = User_info.objects.filter(user=request.user)[0]

    category_form = CategoryForm()
    form2 = CommentForm()
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category = category_form.cleaned_data.get('category')
            all_post = Post.objects.filter(category=category)
            if all_post.exists():
                
                context={
                    'all_post':all_post,
                    'category_form':category_form,
                    'user_info': user_info
                }
                return render(request, 'engine/home.html', context)
            else:

                messages.success(request, 'No post yet for the category selected')
                all_post = Post.objects.all()
                context={
                    'all_post':all_post,
                    'category_form':category_form,
                    'user_info': user_info
                }
                return render(request, 'engine/home.html', context)
    else:
        # all_post = Post.objects.all()
        all_post = Post.objects.annotate(total_comments=Count('post_comments'))

        # ------------test code---------------

        # all_post = Post.objects.prefetch_related('post_comments').all()
        # for post in all_post:
        #     print(f"{post.author} is having {post.likes} likes")
            # for comment in post.post_comments.all():

        # ------------end of test code---------------

        context = {
            'all_post': all_post,
            'category_form':category_form,
            'form2':form2,
            'user_info':user_info
        }
        return render(request, 'engine/home.html', context)


def view_full_post(request, id):
    post = Post.objects.get(pk=id)
    all_post_comments = Comment.objects.filter(post=post).order_by('-date')
    comment_form = CommentForm()
    category_form = CategoryForm()

    context = {
        'post':post,
        'form':comment_form,
        'category_form':category_form,
        'all_post_comments': all_post_comments,
    }

    return render(request, 'engine/view-post.html', context)


def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = form.save()

            #saving the info into the customized model
            user_password = form.cleaned_data.get('password1')
            user_img      = form.cleaned_data.get('profile_img')

            User_info.objects.create(
                user=user, 
                user_password=user_password, 
                user_img=user_img
            )

            #authentication
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully signed up')
            return redirect('home')
        else:
            return render(request, 'engine/register.html', context={'form':form})
    else:
        try:
            get_user = User_info.objects.filter(user=request.user)
            if get_user.exists():
                user_info = get_user[0]
                return render(request, 'engine/register.html', context={
                    'form':form,
                    'user_info':user_info
                })
        except TypeError:
            return render(request, 'engine/register.html', context={
                'form':form,
            })
    

@login_required
def update_profile(request):
    if request.method == 'POST':
        update_profile_form = UpdateProfileForm(request.POST, instance=request.user)
        if update_profile_form.is_valid():
            update_profile_form.save()
            messages.success(request, "Profile information successfully updated")
            return redirect('user_info_profile', user=request.user)
        else:
            messages.success(request, "Invalid informations")
            return redirect('update_profile')
    else:
        update_profile_form = UpdateProfileForm(instance=request.user)
        user_info = User_info.objects.get(user__username=request.user.username)
        return render(request, 'engine/update_profile.html', context={
            'update_profile_form':update_profile_form,
            'user_info':user_info
        })



def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(request.POST or None)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'You have been logged in')
                    return redirect('home')
                else:
                    messages.success(request, 'User is not found. Check your details carefully')
                    print(form.errors)
                    return redirect('login_view')
            else:
                messages.success(request, 'User is not found. Check your details carefully')
                return redirect('login_view')
        else:
            return render(request, 'engine/login.html', context={'form':form})
        

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out. Thank you')
    return redirect('login_view')


@login_required
def add_post(request):
    post_form = NewPost()
    if request.method == 'POST':
        post_form = NewPost(request.POST or  None, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            user = User_info.objects.get(user=request.user)
            post.author = user
            post.save()
            return redirect('home')
        else:
            user_info = User_info.objects.get(user__username=request.user.username)
            return render(request, 'engine/create.html', context={'post_form':post_form, 'user_info': user_info})
    else:
        user_info = User_info.objects.get(user__username=request.user.username)
        return render(request, 'engine/create.html', context={
            'post_form':post_form,
            'user_info': user_info,
        })


@login_required
def delete_post(request, id):
    if request.user.is_authenticated:
        post = Post.objects.get(pk=id)
        post.delete()
        messages.success(request, 'You have successfully deleted a post')
        return redirect('profile_page', user = request.user.username)
    else:
        messages.success(request, 'You have to sign up before you can access this page')
        return redirect('home')


@login_required
def update_post(request, id):
    if request.user.is_authenticated:
        current_post = Post.objects.get(pk=id)
        form = NewPost(request.POST or None, instance=current_post)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'You have successfully updated this post')
                return redirect('profile_page', user = request.user.username)
            else:
                messages.success(request, 'Enter valid informations')
                return redirect('update_post', id=id)
        else:
            context = {
                'form':form,
                'current_post':current_post
            }
            return render(request, 'engine/update-post.html', context)
    else:
        messages.success(request, 'You have to sign up before you can access this page')
        return redirect('home')


@login_required
def profile_page(request, user):
    user_posts = Post.objects.filter(author__user=request.user)
    user_info = User_info.objects.get(user__username=user)
    context = {
        'user_posts':user_posts,
        'user_info':user_info
    }
    return render(request, 'engine/profile-page.html', context)


@login_required
def user_info_profile(request, user):
    user_info = User_info.objects.get(user__username=user)
    context = {
        'user_info':user_info
    }
    return render(request, 'engine/user-profile.html', context)


@login_required
def user_statistics(request, user_id):
    user = User.objects.get(id=user_id)
    user_info = User_info.objects.get(user=user)
    posts = Post.objects.filter(author__user=user)
    posts_no = Post.objects.filter(author__user=user).count()
    total_comments = Comment.objects.filter(post__in=posts).count()
    like_no = Like.objects.filter(post__in=posts).count()

    context = {
        'user': user,
        'user_info':user_info,
        'posts_no': posts_no,
        'total_comments': total_comments,
        'like_no': like_no
    }

    return render(request, 'engine/user-statistics.html', context)


@login_required
def like_post(request, id):
    user = request.user
    post = Post.objects.get(pk=id)
    current_likes = post.likes
    liked = Like.objects.filter(user=user, post=post).count()

    if not liked:
        liked = Like.objects.create(user=user, post=post)
        current_likes += 1
    else:
        liked = Like.objects.filter(user=user, post=post)
        liked.delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()
    # return HttpResponseRedirect(reverse('view_full_post', kwargs={'id':id}))
    return JsonResponse({'likes':current_likes})



@login_required
def post_comment(request, id):
    post = Post.objects.get(pk=id)
    form = CommentForm()
    
    if request.method == 'POST':
        commented = Comment.objects.filter(post=post, user=request.user)

        if not commented:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()

                return redirect('view_full_post', id=id)
            else:
                return redirect('view_full_post', id=id)
        else:
            messages.success(request, "Already commented")
            return redirect('home')
        

@login_required
def edit_comment(request, id):
    current_comment = Comment.objects.get(pk=id)
    update_comment_form = UpdateCommentForm(request.POST or None, instance=current_comment)
    post = current_comment.post

    category_form   = CategoryForm()

    if request.method == 'POST':
        update_comment_form.save()
        return redirect('home')

    context = {
        'post':post,
        'form':update_comment_form,
        'current_comment':current_comment,
        'category_form':category_form,
    }

    return render(request, 'engine/edit_comment.html', context)


@login_required
def delete_comment(request, id):
    user_comment = Comment.objects.get(pk=id)
    user_comment.delete()
    return redirect('home')


def search_post(request):

    if isinstance(request.user, AnonymousUser):
        user_info = ""
    else:
        user_info = User_info.objects.filter(user=request.user)[0]

    category_form = CategoryForm()
    form2 = CommentForm()

    if request.method == "POST":
        searched = request.POST['search'] 
        search_results = Post.objects.filter(Q(title__icontains=searched) | Q(summary__icontains=searched))
        context = {
            'search_results': search_results,
            'category_form':category_form,
            'form2':form2,
            'user_info':user_info
        }
        return render(request, 'engine/home.html', context)
    
    # Handle the case when the request method is not POST
    return redirect('home')

def review_page(request):

    if isinstance(request.user, AnonymousUser):
        user_info = ""
    else:
        user_info = User_info.objects.filter(user=request.user)[0]

    if request.method == "POST":
        try:
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']
            
            #send the email
            subject = 'New Review from LearnShare'
            email_body = f"Name: {name} \nEmail: {email}\nMessage: {message}"
            sender_email = email
            receiver_email = 'isrealolalere09@gmail.com'

            send_mail(
                subject, 
                email_body, 
                sender_email, 
                [receiver_email],
            )

            messages.success(request, f"Hey {name}!, Thanks for the reivew. \n Together we can make education and learning better")
            return redirect('review_page')
        except TimeoutError as e:
            messages.success(request, f"Sorry, {name}!, We couldn't send your review")
            return redirect('review_page')
    return render(request, 'engine/reviews-page.html', context={
      'user_info':user_info,
    })


def top_posts(request):
    if isinstance(request.user, AnonymousUser):
        user_info = ""
    else:
        user_info = User_info.objects.filter(user=request.user)[0]
        
    all_top_posts = User_info.objects.annotate(
        post_count=Count('post'), 
        total_likes=Sum('post__likes')
    ).filter(post__likes__gte=25)

    context = {
        'all_top_posts':all_top_posts,
        'user_info':user_info
    }
    return render(request, 'engine/top-posts.html', context)


def about_us(request):
    return render(request, 'engine/about.html')