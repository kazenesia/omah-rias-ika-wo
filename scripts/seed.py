import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent / 'backend'
sys.path.insert(0, str(BACKEND_DIR))
os.chdir(BACKEND_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from core.models import Package, Vendor

def seed():
    if not Package.objects.exists():
        packages = [
            {
                'name': 'Basic',
                'slug': 'basic',
                'price': 25000000,
                'description': 'Paket dasar untuk pernikahan intimate',
                'features': ['Dekorasi Pelaminan Standar', 'MUA untuk Bride', 'Dokumentasi Foto (1 Fotografer)', 'Catering 100 pax', 'Sound System Basic'],
                'icon': '/static/assets/icon/leaf.png',
                'is_popular': False,
                'order': 1
            },
            {
                'name': 'Medium',
                'slug': 'medium',
                'price': 50000000,
                'description': 'Paket lengkap untuk pernikahan menengah',
                'features': ['Dekorasi Pelaminan Premium', 'MUA untuk Bride & Groom', 'Dokumentasi Foto (2 Fotografer)', 'Dokumentasi Video', 'Catering 200 pax', 'Sound System + MC', 'Tenda 10x10m'],
                'icon': '/static/assets/icon/diamond.png',
                'is_popular': False,
                'order': 2
            },
            {
                'name': 'Extra',
                'slug': 'extra',
                'price': 75000000,
                'description': 'Paket premium untuk pernikahan impian',
                'features': ['Dekorasi Pelaminan Mewah', 'MUA Premium (Bride, Groom, Keluarga)', 'Dokumentasi Foto (3 Fotografer)', 'Dokumentasi Video Cinematic', 'Catering 300 pax', 'Sound System Premium + MC Pro', 'Tenda 15x15m dengan AC', 'Live Acoustic Band', 'Photo Booth'],
                'icon': '/static/assets/icon/crown.png',
                'is_popular': True,
                'order': 3
            },
            {
                'name': 'Custom',
                'slug': 'custom',
                'price': None,
                'description': 'Sesuaikan paket dengan kebutuhan Anda',
                'features': ['Konsultasi Gratis', 'Pilih Vendor Sendiri', 'Fleksibel Budget', 'Personal Wedding Planner', 'Negosiasi Langsung'],
                'icon': '/static/assets/icon/star.png',
                'is_popular': False,
                'order': 4
            }
        ]
        for pkg_data in packages:
            Package.objects.create(**pkg_data)
        print("Successfully seeded Packages")
    else:
        print("Packages already exist")

    if not Vendor.objects.exists():
        vendors = [
            {'name': 'Diana Beauty', 'category': 'mua', 'price_range': '3.5 Jt', 'rating': 4.9},
            {'name': 'Rias Kebaya Jenggolo', 'category': 'mua', 'price_range': '5 Jt', 'rating': 4.8},
            {'name': 'Luxury Decor Sidoarjo', 'category': 'decoration', 'price_range': '15 Jt', 'rating': 4.9},
            {'name': 'Rustika Tent', 'category': 'tent', 'price_range': '8 Jt', 'rating': 4.7},
            {'name': 'Rasa Nusantara Catering', 'category': 'catering', 'price_range': '20 Jt', 'rating': 5.0},
            {'name': 'Lensa Kisah Photography', 'category': 'photographer', 'price_range': '6 Jt', 'rating': 4.9},
            {'name': 'Acoustic Melody', 'category': 'music', 'price_range': '4 Jt', 'rating': 4.8},
            {'name': 'Cantik Gift', 'category': 'gift', 'price_range': '2 Jt', 'rating': 4.7},
            {'name': 'Elegant Invites', 'category': 'invitation', 'price_range': '1.5 Jt', 'rating': 4.9},
        ]
        for v_data in vendors:
            Vendor.objects.create(**v_data)
        print("Successfully seeded Vendors")
    else:
        print("Vendors already exist")

if __name__ == '__main__':
    seed()
