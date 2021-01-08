from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views
from dashboard.dash_apps.finished_apps import simpleexample

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:employee_id>/', views.detail, name='detail'),
    path('register/', views.registerPage, name='register'),
    path('accounts/login/', views.loginPage, name='login'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('account/', views.accountSettings, name='account'),
    
    path('add_stats/<int:employee_id>', views.addStats, name='addStats'),
    path('add_qa/<int:employee_id>', views.addQA, name='addQA'),
    path('add_timeStats/<int:employee_id>', views.addTimeStats, name='addTimeStats'),
    path('add_update/', views.addUpdate, name='addUpdate'),
    path('import_employees/', views.importEmployees, name='importEmployees'),
    path('import_statistics/', views.importStatistics, name='updateStatistics'),
    path('update_employee/<int:employee_id>', views.updateEmployee, name='updateEmployee'),
    path('update_stats/<str:pk>', views.updateStats, name='updateStats'),
    path('delete_stats/<str:pk>', views.deleteStats, name='deleteStats'),
    path('update_qa/<str:pk>', views.updateQA, name='updateQA'),
    path('delete_qa/<str:pk>', views.deleteQA, name='deleteQA'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    
    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name='dashboard/reset_password.html'), 
        name='reset_password'),
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name='dashboard/password_reset_sent.html'), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='dashboard/password_reset_form.html'), 
        name='password_reset_confirm'),
    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='dashboard/password_reset_done.html'), 
        name='password_reset_complete'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# 1. Submit email form //PasswordResetView.as_view()
# 2. Email sent success message //PasswordResetDoneView.as_view()
# 3. Link to Password Reset form in Email //PasswordResetConfirmView.as_view()
# 4. Password successfully changed message //PasswordResetCompleteView.as_view()