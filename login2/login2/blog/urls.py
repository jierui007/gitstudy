from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.do_login, name='login'),
    path('logout/', views.do_logout, name='logout'),
    path('write/',views.write,name='write'),

    path('anthology_create/', views.anthology_create, name='anthology_create'),
    path('anthology_list/', views.anthology_list, name='anthology_list'),
    path('anthology_update/',views.anthology_update,name='anthology_update'),
    path('anthology_delete/',views.anthology_delete,name= 'anthology_delete'),

    path('article/', views.article, name='article'),
    path('article_create/', views.article_create, name='article_create'),
    path('article_post/', views.article_post, name='article_post'),
    path('article_delete/',views.article_delete,name='article_delete'),

    path('upload_ajax/', views.upload_ajax, name='upload_ajax'),
]