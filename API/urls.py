from django.conf.urls import patterns, url

from API import views

urlpatterns = patterns('',
    url(r'login$', views.login, name='login'),
    url(r'logout$', views.logout, name='logout'),
    url(r'user$', views.get_user_by_id, name='get_user_by_id'),
    url(r'user/list/create$', views.create_list_by_user_id, name='create_list_by_user_id'),
    url(r'user/list/delete$', views.delete_list_by_user_id, name='delete_list_by_user_id'),
    url(r'user/lists$', views.get_user_lists, name='get_user_lists'),
    url(r'user/list/add$', views.add_user_to_list, name='add_user_to_list'),
    url(r'user/list/remove$', views.remove_user_from_list, name='remove_user_from_list'),
    url(r'user/tickets$', views.get_ticket_by_user_id_and_bar_id, name='get_ticket_by_user_id_and_bar_id'),

)
