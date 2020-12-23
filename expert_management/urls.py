from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),

    # Profile views
    path('profile/', views.MyProfileRedirectView.as_view(), name='my-profile'),
    path('user/<str:username>/', views.Profile.as_view(), name='profile'),
    path('update-profile/', views.UpdateProfile.as_view(), name='update-profile'),

    # Project views
    path('projects/', views.ProjectList.as_view(), name='projects'),
    path('create-project/', views.CreateProject.as_view(), name='create-project'),
    path('update-project/<int:pk>/', views.UpdateProject.as_view(), name='update-project'),
    path('delete-project/<int:pk>/', views.DeleteProject.as_view(), name='delete-project'),

    # Expertise views
    path('create-expertise/', views.CreateExpertise.as_view(), name='create-expertise'),
    path('update-expertise/', views.UpdateExpertise.as_view(), name='update-expertise'),

    path('search/', views.Search.as_view(), name='search'),
    path('advance-search/', views.AdvanceSearch.as_view(), name='advance-search'),
    path('search-result/', views.SearchResultView.as_view(), name='search-result')
]
