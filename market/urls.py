from django.urls import path

from market import views

urlpatterns = [
    path('character', views.CharacterListAPIView.as_view(), name=''),
    path('server', views.ServerListAPIView.as_view(), name=''),
]
#     path('', views.xxxxxxx, name='xxxxxx'),
# ]




