from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about_us, name='about'),
    
    # Using Django's built-in views for login and logout
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('players/', views.player_list, name='player_list'),
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),
    path('add-player/', views.add_player, name='add_player'),
    path('edit-player/<int:player_id>/', views.edit_player, name='edit_player'),
    path('delete-player/<int:player_id>/', views.delete_player, name='delete_player'),
    path('compare-players/', views.compare_players, name='compare_players'),

    path('', views.product_list, name='product_list'),
     path('search/', views.search_view, name='search'),
]

