from django.urls import path


from .views import *

urlpatterns = [
    path('', ShowPostsList.as_view(), name='index'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('create_post/', NewPost.as_view(), name='create_post'),
    path('post/<slug:url>', PostDetail.as_view(), name='post'),
    path('profile/<str:username>', ShowProfileView.as_view(), name='profile'),
    path('profile/<str:username>/update/<slug:slug>', UpdatePostView.as_view(), name='update_post'),
    path('remove/<str:username>/<slug:slug>', remove_post, name='remove_post'),
    path('add_comment/<slug:slug>', AddComment.as_view(), name='add_comment'),
    path('follow/<str:username>/', following, name='follow'),
    path('unfollow/<str:username>/', unfollowing, name='unfollow'),
    path('<str:category>/', ShowPostsList.as_view(), name='category' )
]

