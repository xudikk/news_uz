from django.urls import path


from . import views
from .auth_views import auth, otp, logout

urlpatterns = [
    path('', views.index, name='home'),
    path('category/<slug>/', views.ctg, name='ctg'),
    path('view/<int:pk>/', views.view, name='view'),
    path('srch/', views.search, name='search'),
    path('contact/', views.cnt, name='contact'),

    path('add_to_subs/<path>/', views.add_to_subs, name='subs_add'),

    # login+register
    path("auth/", auth, name='auth'),
    path("otp/", otp, name='otp'),
    path("logout/", logout, name='logout'),

]







