import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Booking, Package, Vendor

@csrf_exempt
@require_http_methods(["POST"])
def api_submit_booking(request):
    try:
        data = json.loads(request.body)
        
        name = data.get('name')
        whatsapp = data.get('whatsapp')
        event_date = data.get('event_date')
        venue = data.get('venue', 'TBD')
        guest_count = data.get('guest_count', '')
        package_slug = data.get('package')
        notes = data.get('notes', '')
        
        package = None
        total_amount = 0
        if package_slug:
            try:
                package = Package.objects.get(slug=package_slug)
                total_amount = package.price
            except Package.DoesNotExist:
                pass
                
        booking = Booking.objects.create(
            name=name,
            whatsapp=whatsapp,
            event_date=event_date,
            venue=venue,
            guest_count=guest_count,
            package=package,
            notes=notes,
            total_amount=total_amount,
            status='booking'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Booking submitted successfully',
            'booking_code': booking.code
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_check_booking(request):
    try:
        data = json.loads(request.body)
        whatsapp = data.get('whatsapp')
        code = data.get('code')
        
        booking = Booking.objects.get(whatsapp=whatsapp, code=code)
        
        return JsonResponse({
            'success': True,
            'booking': {
                'code': booking.code,
                'name': booking.name,
                'status': booking.status,
                'status_display': booking.get_status_display(),
                'package': booking.package.name if booking.package else 'Custom',
                'event_date': booking.event_date.strftime('%Y-%m-%d') if booking.event_date else '-',
                'venue': booking.venue,
                'total_amount': float(booking.total_amount) if booking.total_amount else 0,
                'paid_amount': float(booking.paid_amount) if booking.paid_amount else 0,
            }
        })
    except Booking.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Booking not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@require_http_methods(["GET"])
def api_list_vendors(request):
    category = request.GET.get('category')
    vendors = Vendor.objects.filter(is_active=True)
    
    if category and category != 'all':
        vendors = vendors.filter(category=category)
        
    data = []
    for v in vendors:
        data.append({
            'id': v.id,
            'name': v.name,
            'category': v.get_category_display(),
            'rating': float(v.rating),
            'image': v.image.url if v.image else '/static/assets/background/couple.webp'
        })
        
    return JsonResponse({'vendors': data})

@require_http_methods(["GET"])
def api_list_packages(request):
    packages = Package.objects.all()
    data = []
    for p in packages:
        data.append({
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'price': float(p.price) if p.price else None,
            'features': p.features,
            'is_popular': p.is_popular
        })
    return JsonResponse({'packages': data})
