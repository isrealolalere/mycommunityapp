from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search_post, name='search'),
    path('signup', views.register, name='signup'),
    path('login', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout_view'),
    path('new', views.add_post, name='add_post'),
    path('delete/<int:id>', views.delete_post, name='delete_post'),
    path('edit/<int:id>', views.update_post, name='update_post'),
    path('post/<int:id>', views.view_full_post, name='view_full_post'),
    path('profile/<str:user>', views.profile_page, name='profile_page'),
    path('profile-info/<str:user>', views.user_info_profile, name='user_info_profile'),
    path('profile-stats/<int:user_id>', views.user_statistics, name='user_statistics'),
    path('update-profile', views.update_profile, name='update_profile'),
    # path('like/<int:id>', views.like_post, name='like_post'),
    path('like_post/<int:id>/', views.like_post, name='like_post'),
    path('post_comment/<int:id>/', views.post_comment, name='post_comment'),
    path('edit_comment/<int:id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),


    path('reviews', views.review_page, name='review_page'),
    path('top-posts', views.top_posts, name='top_posts'),
    path('about-us', views.about_us, name='about_us'),
]