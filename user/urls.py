from django.urls import path
from user.views import UserList
from rest_framework.routers import DefaultRouter


# Define our routes manually (could be done using DefaultRouter, alternatively)
root_view = UserList.as_view({'get': 'get',
                              'post': 'post'})
delete_view = UserList.as_view({'get': 'get',
                                'delete': 'delete'})
update_view = UserList.as_view({'get': 'get',
                                'put': 'update',
                                'patch': 'partial_update'})
# For POST requests made by the Google API (calendar updates)
hook_view = UserList.as_view({'get': 'get',
                              'post': 'post_calendar'})

urlpatterns = [
    path('', root_view, name='root'),
    path('delete/<pk>/', delete_view, name='delete-user'),
    path('update/<pk>/', update_view, name='update-user'),
    path('<pk>', hook_view, name='user-home')
]
