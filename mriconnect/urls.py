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
from django.views.generic import TemplateView, RedirectView
from people import urls as people_urls

# from ra.admin.admin import ra_admin_site
# handler500 = 'ra.utils.views.server_error'
# handler404 = 'ra.utils.views.not_found_error'

urlpatterns = [
    path('sw.js',
        TemplateView.as_view(template_name="app/sw.js", content_type='application/javascript'),
        name='sw.js'),
    path('robots.txt',
        TemplateView.as_view(template_name="app/robots.txt", content_type="text/plain"),
        name='robots.txt'),

    # Password management paths
    path('pwd/reset',
        auth_views.PasswordResetView.as_view(template_name='admin/password_reset_form.html'),
        name='password_reset_form'),
    path('pwd/done',
        auth_views.PasswordResetDoneView.as_view(template_name='admin/password_reset_done.html'),
        name='password_reset_done'),
    path('pwd/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='admin/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('pwd/complete',
        auth_views.PasswordResetDoneView.as_view(template_name='admin/password_reset_complete.html'),
        name='password_reset_complete'),

    # Main application path
    path('mri/', admin.site.urls),

    # REST API paths
    path('api/', include(people_urls)),

    # Redirect home page
    path('', RedirectView.as_view(url='https://mountainresearchinitiative.org/find-an-expert', permanent=False),),
]
