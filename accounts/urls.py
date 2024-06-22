from django.urls import path
from .views import (
    dashboard_view,
    CustomUserCreationView,
    CustomUserChangeView,
    admin_page_view,
    user_info_view,
    comment_delete_view,
    toggle_comment_status_view,
    toggle_user_status_view,
    )
# from .forms import CustomLoginForm

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('signup/', CustomUserCreationView.as_view(), name='signup'),
    path('dashboard/edit/', CustomUserChangeView.as_view(), name='user_change'),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('adminpage/user_info/<int:user_id>/', user_info_view, name='view_user_dashboard'),
    path('comment_delete/<int:comment_id>/', comment_delete_view, name='comment_delete'),
    path('admin/toggle_comment_status/<int:comment_id>/', toggle_comment_status_view, name='toggle_comment_status'),
    path('admin/toggle_user_status/<int:user_id>/', toggle_user_status_view, name='toggle_user_status'),
    # path('login/', user_login, name='login'), # funksiya orqali qilingan custom login view url
    # path('login/', LoginView.as_view(template_name="registration/login.html",             # Bu 'LoginView'ni qayta
    #                                  authentication_form=CustomLoginForm), name='login'), # yozganda qo'llaniladigan url
    # path('signup/', custom_signup_view, name='signup'), # funksiya orqali qilingan custom signup view url
]
