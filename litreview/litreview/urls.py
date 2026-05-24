"""
URL configuration for litreview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from AppCritique.views import (
    home,
    signup,
    CustomLoginView,
    logout_view,
    feed,
    create_ticket,
    create_review,
    create_ticket_review,
    posts,
    update_ticket,
    update_review,
    delete_ticket,
    delete_review,
    subscriptions,
    unfollow_user
)

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('signup/', signup, name='signup'),

    path('login/', CustomLoginView.as_view(), name='login'),

    path('logout/', logout_view, name='logout'),

    path('feed/', feed, name='feed'),

    path('ticket/create/', create_ticket, name='create_ticket'),

    path('review/create/<int:ticket_id>/', create_review, 
         name='create_review_from_ticket'),

    path('ticket-review/create/', create_ticket_review, 
         name='create_ticket_review'),

    path('posts/', posts, name='posts'),

    path('ticket/update/<int:ticket_id>/', update_ticket, 
         name='update_ticket'),

    path('review/update/<int:review_id>/', update_review, 
         name='update_review'),

    path('ticket/delete/<int:ticket_id>/', delete_ticket, 
         name='delete_ticket'),

    path('review/delete/<int:review_id>/',  delete_review, 
         name='delete_review'),

    path('subscriptions/', subscriptions, name='subscriptions'),

    path('unfollow/<int:follow_id>/', unfollow_user, name='unfollow_user'),
]

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )