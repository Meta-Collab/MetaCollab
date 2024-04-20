from django.urls import path, re_path
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('api/list_rooms',views.api_list_room, name='api_list_rooms'),
    path('list_rooms',views.list_rooms, name='list_rooms'),
    path('get_room', views.get_room, name='get_room'),
    re_path(r'^get_room/(?P<roomuuid>[0-9a-f-]+)/$', views.get_room, name='get_room'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
