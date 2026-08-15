from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from . import views, admin_views, api_views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('katalog/', views.catalog_view, name='catalog'),
    path('paket/', views.packages_view, name='packages'),
    path('booking/', views.booking_view, name='booking'),
    path('booking/success/', views.booking_success_view, name='booking_success'),
    path('cek-booking/', views.check_booking_view, name='check_booking'),
    
    # Custom Admin Panel endpoints
    path('admin-panel/', RedirectView.as_view(url='/admin-panel/login/', permanent=False), name='admin_panel_root'),
    path('admin-panel/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/orders/', admin_views.admin_orders, name='admin_orders'),
    path('admin-panel/orders/<str:order_code>/delete/', admin_views.admin_delete_order, name='admin_delete_order'),
    path('admin-panel/orders/<str:order_code>/edit/', admin_views.admin_edit_order, name='admin_edit_order'),
    path('admin-panel/catalog/', admin_views.admin_catalog, name='admin_catalog'),
    path('admin-panel/catalog/add/', admin_views.admin_add_vendor, name='admin_add_vendor'),
    path('admin-panel/catalog/<int:vendor_id>/edit/', admin_views.admin_edit_vendor, name='admin_edit_vendor'),
    path('admin-panel/catalog/<int:vendor_id>/delete/', admin_views.admin_delete_vendor, name='admin_delete_vendor'),
    path('admin-panel/packages/', admin_views.admin_packages, name='admin_packages'),
    path('admin-panel/packages/<int:package_id>/edit/', admin_views.admin_edit_package, name='admin_edit_package'),
    path('admin-panel/gallery/', admin_views.admin_gallery, name='admin_gallery'),
    path('admin-panel/login/', LoginView.as_view(template_name='admin/login.html', next_page='/admin-panel/dashboard/'), name='admin_login'),
    path('admin-panel/logout/', LogoutView.as_view(next_page='/admin-panel/login/'), name='admin_logout'),
    
    # API endpoints
    path('api/booking/', api_views.api_submit_booking, name='api_submit_booking'),
    path('api/booking/check/', api_views.api_check_booking, name='api_check_booking'),
    path('api/vendors/', api_views.api_list_vendors, name='api_list_vendors'),
    path('api/packages/', api_views.api_list_packages, name='api_list_packages'),
]
