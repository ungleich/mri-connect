"""mriconnect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from people import urls as people_urls

# from ra.admin.admin import ra_admin_site
# handler500 = 'ra.utils.views.server_error'
# handler404 = 'ra.utils.views.not_found_error'

urlpatterns = [
    path('sw.js', (TemplateView.as_view(template_name="app/sw.js", content_type='application/javascript', )), name='sw.js'),
    # password reset views
    path('mri/password_reset/',  auth_views.PasswordResetView.as_view(),  name='admin_password_reset',
    ),
    path('mri/password_reset/done/',  auth_views.PasswordResetDoneView.as_view(),  name='password_reset_done',
    ),
    path('reset/<uidb64>/<token>/',  auth_views.PasswordResetConfirmView.as_view(),  name='password_reset_confirm',
    ),
    path('reset/done/',  auth_views.PasswordResetCompleteView.as_view(),  name='password_reset_complete',
    ),
    # path('', ra_admin_site.urls),
    path('mri/', admin.site.urls),
    path('api/', include(people_urls)),
]
