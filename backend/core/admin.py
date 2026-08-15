from django.contrib import admin
from .models import Package, Vendor, Booking, GalleryImage, SiteSettings

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_popular', 'order')
    list_editable = ('is_popular', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'rating')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'whatsapp', 'event_date', 'status', 'created_at')
    list_filter = ('status', 'event_date')
    search_fields = ('code', 'name', 'whatsapp', 'venue')
    readonly_fields = ('code',)

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'category', 'is_featured', 'order')
    list_editable = ('is_featured', 'order')
    list_filter = ('category', 'is_featured')

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return True
