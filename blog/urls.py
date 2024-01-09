from . import views
from django.urls import path
from .feeds import LatestPostsFeed
app_name = 'blog'

urlpatterns = [
        #path('', views.PostListView.as_view(), name='list'),
        path('',views.list,name='list'),
        path('tag/<slug:tag_slug>', views.list, name='list_by_tag'),
        path('<int:year>/<int:month>/<int:day>/<slug:post>', views.detail, name='detail'),
        path('<int:id>/share/',views.share,name='share'),
        path('<int:id>',views.comment,name='comment'),
        path('feed/', LatestPostsFeed(), name='post_feed'),
]