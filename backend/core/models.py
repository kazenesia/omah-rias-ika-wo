from django.db import models
from django.utils.translation import gettext_lazy as _

class Package(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    features = models.JSONField(default=list, help_text="List of included features")
    not_included = models.JSONField(default=list, help_text="List of not included features", blank=True)
    icon = models.CharField(max_length=100, help_text="Path to icon or font class")
    is_popular = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'price']

    def __str__(self):
        return self.name

class Vendor(models.Model):
    CATEGORY_CHOICES = [
        ('mua', 'MUA'),
        ('decoration', 'Decoration'),
        ('tent', 'Tent'),
        ('catering', 'Catering'),
        ('photographer', 'Photographer'),
        ('music', 'Music'),
        ('invitation', 'Invitation'),
        ('gift', 'Gift'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    price_range = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='vendors/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('booking', 'Booking'),
        ('dp', 'Down Payment'),
        ('technical_meeting', 'Technical Meeting'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    code = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=200)
    whatsapp = models.CharField(max_length=20)
    event_date = models.DateField()
    venue = models.CharField(max_length=255)
    guest_count = models.CharField(max_length=50)

    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, related_name='bookings')
    add_ons = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='booking')
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.code:
            import random
            import string
            # Generate a random 6 character alphanumeric code
            chars = string.ascii_uppercase + string.digits
            code = "WO-" + ''.join(random.choice(chars) for _ in range(6))
            # Just retry if it somehow exists
            while Booking.objects.filter(code=code).exists():
                code = "WO-" + ''.join(random.choice(chars) for _ in range(6))
            self.code = code
        super().save(*args, **kwargs)

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.caption or f"Image {self.id}"

class SiteSettings(models.Model):
    phone = models.CharField(max_length=20, default='+62 812-3456-7890')
    address = models.TextField(default='Jl. Dusun Mlaten Gg. II, Gempol, Pasuruan, Jawa Timur')
    email = models.EmailField(default='hello@omahriasika.com')
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SiteSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Site Settings"
