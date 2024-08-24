from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm, UserSetPasswordForm

urlpatterns = [
    path('admin/', admin.site.urls),
    # URL pattern for user registration page
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    
    path('logout/',views.Logout,name='Logout'),
    # URL patterns for changing the user password in case of forgot password
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='legalSupport/password_reset_form.html', 
        form_class=UserPasswordResetForm,
        email_template_name='legalSupport/password_reset_email.html',
        subject_template_name='legalSupport/password_reset_subject.txt'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='legalSupport/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='legalSupport/password_reset_confirm.html', form_class=UserSetPasswordForm), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='legalSupport/password_reset_complete.html'), name='password_reset_complete'),
    path('', include('researchEngine.urls')),
]
