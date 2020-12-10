from django.urls import path

from .views import Profile, CreateProfile, UpdateProfile, ProjectList, DeleteProject, CreateProject

urlpatterns = [
    path('user/<str:username>/', Profile.as_view(), name='profile'),
    path('create-profile/', CreateProfile.as_view(), name='create-profile'),
    path('update-profile/', UpdateProfile.as_view(), name='update-profile'),
    path('create-project/', CreateProject.as_view(), name='create-project'),
    path('delete-project/<int:pk>/', DeleteProject.as_view(), name='delete-project'),
    path('projects/', ProjectList.as_view(), name='projects')
]
