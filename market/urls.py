from django.urls import path

from market import views
from market.views import CipSoftCommissionView, AuctionsDataView

urlpatterns = [
    path("all_characters_datas", views.CharacterListAPIView.as_view(), name=""),
    path("server", views.ServerListAPIView.as_view(), name=""),
    path("auctions", AuctionsDataView.as_view(), name=""),
    path("commission", CipSoftCommissionView.as_view(), name=""),
]
#     path('', views.xxxxxxx, name='xxxxxx'),
# ]
