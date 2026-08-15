from django.shortcuts import render
from .models import Package, Vendor, GalleryImage, SiteSettings

def home_view(request):
    settings = SiteSettings.load()
    packages = Package.objects.all()[:3]
    services = [
        {'name': 'Rias Pengantin', 'desc': 'MUA profesional dengan gaya natural hingga glamour.', 'icon': '/static/assets/icon/cosmetics.png', 'url': '/katalog/?category=mua'},
        {'name': 'Dekorasi', 'desc': 'Pelaminan dan dekorasi venue yang memukau.', 'icon': '/static/assets/icon/decoration.png', 'url': '/katalog/?category=decoration'},
        {'name': 'Dokumentasi', 'desc': 'Abadikan momen berharga dengan fotografer handal.', 'icon': '/static/assets/icon/photographer.png', 'url': '/katalog/?category=photographer'},
        {'name': 'Katering', 'desc': 'Hidangan lezat untuk tamu undangan Anda.', 'icon': '/static/assets/icon/buffet.png', 'url': '/katalog/?category=catering'},
    ]
    testimonials = [
        {'quote': 'Rias pengantin saya sempurna! Tim Omah Rias Ika sangat detail dan sabar.', 'name': 'Sari & Budi', 'event': 'Pernikahan Adat Jawa'},
        {'quote': 'WO-nya profesional, semua berjalan lancar tanpa stres. Highly recommended!', 'name': 'Dewi & Ahmad', 'event': 'Pernikahan Modern'},
        {'quote': 'Harga transparan, hasil foto dan dekorasi beyond expectation.', 'name': 'Rina & Fajar', 'event': 'Intimate Wedding'},
    ]
    highlights = [
        'Rias pengantin profesional dengan berbagai gaya',
        'Koordinasi WO dari awal hingga hari H',
        'Vendor terkurasi & harga transparan',
    ]
    return render(request, 'index.html', {
        'settings': settings,
        'packages': packages,
        'services': services,
        'testimonials': testimonials,
        'highlights': highlights,
    })

def catalog_view(request):
    settings = SiteSettings.load()
    vendors = Vendor.objects.filter(is_active=True)
    return render(request, 'catalog.html', {'settings': settings, 'vendors': vendors})

def packages_view(request):
    settings = SiteSettings.load()
    packages = Package.objects.all()
    return render(request, 'packages.html', {'settings': settings, 'packages': packages})

def booking_view(request):
    settings = SiteSettings.load()
    packages = Package.objects.all()
    steps = [
        {'num': 1, 'label': 'Kontak'},
        {'num': 2, 'label': 'Acara'},
        {'num': 3, 'label': 'Paket'},
        {'num': 4, 'label': 'Review'},
    ]
    return render(request, 'booking.html', {'settings': settings, 'packages': packages, 'steps': steps})

def booking_success_view(request):
    settings = SiteSettings.load()
    return render(request, 'booking-success.html', {'settings': settings})

def check_booking_view(request):
    settings = SiteSettings.load()
    return render(request, 'check-booking.html', {'settings': settings})
