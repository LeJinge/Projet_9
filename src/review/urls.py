from django.urls import path
from .views import (user_feed_view,
                    user_posts_view,
                    create_review_response_view,
                    create_ticket_view,
                    create_review_view,
                    edit_ticket_view,
                    edit_review_view,
                    delete_post_view)

urlpatterns = [
    path('user_feed/', user_feed_view, name='user_feed'),
    path('post/', user_posts_view, name='post'),
    path('create_ticket/', create_ticket_view, name='create_ticket'),
    path('create_review/', create_review_view, name='create_review'),
    path('respond_to_ticket/<int:ticket_id>/', create_review_response_view, name='respond_to_ticket'),
    path('edit_ticket/<int:ticket_id>/', edit_ticket_view, name='edit_ticket'),
    path('edit_review/<int:review_id>/', edit_review_view, name='edit_review'),
    path('delete_post/<int:post_id>/<str:post_type>/', delete_post_view, name='delete_post'),
]
