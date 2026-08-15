import math
import json
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Booking, Package, Vendor, GalleryImage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at')[:5]
    total_rev = sum(b.total_amount for b in Booking.objects.filter(status='completed'))
    context = {
        'recent_bookings': bookings,
        'total_bookings': Booking.objects.count(),
        'total_revenue': total_rev,
    }
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_orders(request):
    bookings = Booking.objects.all().order_by('-created_at')
    orders_data = []
    for b in bookings:
        orders_data.append({
            'id': b.code,
            'name': b.name,
            'date': b.event_date.strftime('%Y-%m-%d'),
            'package': b.package.name if b.package else 'Custom',
            'status': b.status,
            'total': float(b.total_amount) if b.total_amount else 0,
            'paid': float(b.paid_amount) if b.paid_amount else 0,
            'whatsapp': b.whatsapp,
            'venue': b.venue,
            'guest_count': b.guest_count,
            'notes': b.notes
        })
    orders_json = json.dumps(orders_data, cls=DjangoJSONEncoder)
    return render(request, 'admin/orders.html', {'orders_json': orders_json})

@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_catalog(request):
    vendors = Vendor.objects.all().order_by('-id')
    vendors_data = []
    for v in vendors:
        vendors_data.append({
            'id': v.id,
            'name': v.name,
            'category': v.category,
            'description': v.description,
            'price_range': v.price_range,
            'status': 'active' if v.is_active else 'inactive',
            'rating': float(v.rating),
            'image': v.image.url if v.image else '/static/assets/background/couple.webp'
        })
    vendors_json = json.dumps(vendors_data, cls=DjangoJSONEncoder)
    return render(request, 'admin/catalog.html', {'vendors_json': vendors_json})

@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_packages(request):
    packages = Package.objects.all()
    packages_data = []
    for p in packages:
        packages_data.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price) if p.price else 0,
            'features': p.features if p.features else [],
            'is_popular': p.is_popular,
            'icon': p.icon if p.icon else None,
            'status': 'active'
        })
    packages_json = json.dumps(packages_data, cls=DjangoJSONEncoder)
    return render(request, 'admin/packages.html', {'packages': packages, 'packages_json': packages_json})

@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_gallery(request):
    # Fetch images from vendors to integrate with catalog as requested
    vendors_with_images = Vendor.objects.exclude(image='')
    
    gallery_data = []
    for v in vendors_with_images:
        item = {
            'id': v.id,
            'title': v.name,
            'category': v.category,
            'image': v.image.url
        }
        gallery_data.append(item)
        
    gallery_json = json.dumps(gallery_data, cls=DjangoJSONEncoder)
    # We pass 'gallery_json' for Alpine.js and 'images' (as list) for initial or fallback render
    return render(request, 'admin/gallery.html', {
        'images': gallery_data, 
        'gallery_json': gallery_json
    })

@require_http_methods(["POST"])
@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_delete_order(request, order_code):
    try:
        booking = Booking.objects.get(code=order_code)
        booking.delete()
        return JsonResponse({'success': True})
    except Booking.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found'}, status=404)

@require_http_methods(["POST"])
@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_edit_order(request, order_code):
    try:
        booking = Booking.objects.get(code=order_code)
        data = json.loads(request.body)
        
        if 'name' in data: booking.name = data['name']
        if 'whatsapp' in data: booking.whatsapp = data['whatsapp']
        if 'date' in data: booking.event_date = data['date']
        if 'venue' in data: booking.venue = data['venue']
        if 'guest_count' in data: booking.guest_count = data['guest_count']
        if 'notes' in data: booking.notes = data['notes']
        if 'status' in data: booking.status = data['status']
            
        # Process payment recording
        if 'add_payment' in data:
            try:
                payment_amount = float(data['add_payment'])
                if payment_amount > 0:
                    current_paid = float(booking.paid_amount) if booking.paid_amount else 0
                    booking.paid_amount = current_paid + payment_amount
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid payment amount'}, status=400)
                
        booking.save()
        
        # Return updated booking data to refresh UI
        return JsonResponse({
            'success': True, 
            'booking': {
                'id': booking.code,
                'name': booking.name,
                'date': booking.event_date.strftime('%Y-%m-%d'),
                'package': booking.package.name if booking.package else 'Custom',
                'status': booking.status,
                'total': float(booking.total_amount) if booking.total_amount else 0,
                'paid': float(booking.paid_amount) if booking.paid_amount else 0,
                'whatsapp': booking.whatsapp,
                'venue': booking.venue,
                'guest_count': booking.guest_count,
                'notes': booking.notes
            }
        })
    except Booking.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_http_methods(["POST"])
@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_add_vendor(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            is_active = data.get('is_active', True)
        else:
            data = request.POST
            is_active_str = str(data.get('is_active', 'true')).lower()
            is_active = is_active_str == 'true'

        try:
            rating_val = float(data.get('rating', 5.0)); rating_val = 5.0 if math.isnan(rating_val) else rating_val
        except (TypeError, ValueError):
            rating_val = 5.0

        vendor = Vendor(
            name=data.get('name', ''),
            category=data.get('category', 'mua'),
            description=data.get('description', ''),
            price_range=data.get('price_range', ''),
            rating=rating_val,
            is_active=is_active
        )
        
        if 'image' in request.FILES:
            vendor.image = request.FILES['image']
            
        vendor.save()

        return JsonResponse({
            'success': True,
            'vendor': {
                'id': vendor.id,
                'name': vendor.name,
                'category': vendor.category,
                'description': vendor.description,
                'price_range': vendor.price_range,
                'status': 'active' if vendor.is_active else 'inactive',
                'rating': float(vendor.rating),
                'image': vendor.image.url if vendor.image else '/static/assets/background/couple.webp'
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_http_methods(["POST"])
@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_edit_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            if 'name' in data: vendor.name = data['name']
            if 'category' in data: vendor.category = data['category']
            if 'description' in data: vendor.description = data['description']
            if 'price_range' in data: vendor.price_range = data['price_range']
            if 'rating' in data:
                try:
                    rat = float(data['rating']); vendor.rating = 5.0 if math.isnan(rat) else rat
                except (TypeError, ValueError):
                    pass
            if 'is_active' in data: vendor.is_active = data['is_active']
        else:
            data = request.POST
            if 'name' in data: vendor.name = data['name']
            if 'category' in data: vendor.category = data['category']
            if 'description' in data: vendor.description = data['description']
            if 'price_range' in data: vendor.price_range = data['price_range']
            if 'rating' in data:
                try:
                    rat = float(data['rating']); vendor.rating = 5.0 if math.isnan(rat) else rat
                except (TypeError, ValueError):
                    pass
            if 'is_active' in data:
                vendor.is_active = str(data['is_active']).lower() == 'true'
            
            if 'image' in request.FILES:
                vendor.image = request.FILES['image']
        
        vendor.save()

        return JsonResponse({
            'success': True,
            'vendor': {
                'id': vendor.id,
                'name': vendor.name,
                'category': vendor.category,
                'description': vendor.description,
                'price_range': vendor.price_range,
                'status': 'active' if vendor.is_active else 'inactive',
                'rating': float(vendor.rating),
                'image': vendor.image.url if vendor.image else '/static/assets/background/couple.webp'
            }
        })
    except Vendor.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Vendor not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_http_methods(["POST"])
@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_delete_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
        vendor.delete()
        return JsonResponse({'success': True})
    except Vendor.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Vendor not found'}, status=404)

@require_http_methods(["POST"])
@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_edit_package(request, package_id):
    try:
        package = Package.objects.get(id=package_id)
        data = json.loads(request.body)
        
        if 'name' in data: package.name = data['name']
        if 'price' in data: package.price = data['price']
        if 'is_popular' in data: package.is_popular = data['is_popular']
        if 'features' in data: package.features = data['features']
        
        package.save()
        
        return JsonResponse({
            'success': True,
            'package': {
                'id': package.id,
                'name': package.name,
                'price': float(package.price) if package.price else 0,
                'features': package.features if package.features else [],
                'is_popular': package.is_popular,
                'icon': package.icon if package.icon else None,
                'status': 'active'
            }
        })
    except Package.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Package not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
