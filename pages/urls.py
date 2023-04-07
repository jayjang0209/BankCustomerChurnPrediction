from django.urls import path
from .views import homePageView,  homePost, results, dataView

urlpatterns = [
    path('', homePageView, name='home'),
    path('homePost/', homePost, name='homePost'),
    path('results/<int:age>/<str:active_member>/<str:gender>/<int:bank_balance>/<int:num_products>/', 
        results, name='results'),
    path('data/', dataView, name='data'),
]
