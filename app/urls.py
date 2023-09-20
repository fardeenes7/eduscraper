from django.urls import path, include

from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    path('account/', account, name='account'),
    path('account/saved/', account_saved_programs, name='saved_programs'),
    path('api/save_program/', api_save_program, name='api_save_program'),


    path('programs/', programs_list, name='program_list'),
    path('programs/<int:id>/', program_details, name='program_details'),

    path('universities/', university_list, name='university_list'),
    path('universities/<int:id>/', university_details, name='university_details'),

]