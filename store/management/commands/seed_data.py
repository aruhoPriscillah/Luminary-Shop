from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seed the database with sample products'

    def handle(self, *args, **kwargs):
        # Categories
        cats = {}
        for name, slug in [
            ('Electronics', 'electronics'),
            ('Clothing', 'clothing'),
            ('Home & Kitchen', 'home-kitchen'),
            ('Books', 'books'),
        ]:
            c, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
            cats[slug] = c

        products = [
            # Electronics
            dict(category=cats['electronics'], name='Wireless Headphones Pro',
                 description='Premium over-ear headphones with 40-hour battery life and active noise cancellation. Deep bass, crisp highs, and foldable design for travel.',
                 price='8998', original_price='12999', stock=24, is_featured=True),
            dict(category=cats['electronics'], name='USB-C Hub 7-in-1', slug='usb-c-hub-7in1',
                 description='Expand your laptop with HDMI 4K, 3× USB-A, SD card, and 100W PD charging — all in a slim aluminum body.',
                 price='4500', stock=50, is_featured=True),
            dict(category=cats['electronics'], name='Smart LED Desk Lamp', slug='smart-led-desk-lamp',
                 description='Adjustable color temperature (2700K–6500K), touch dimming, USB charging port, and memory function.',
                 price='3800', original_price='5200', stock=18),

            # Clothing
            dict(category=cats['clothing'], name='Classic Merino Crew Sweater', slug='merino-crew-sweater',
                 description='100% fine merino wool. Itch-free, machine washable, and soft enough for all-day wear. Available in 8 colors.',
                 price='7900', stock=35, is_featured=True),
            dict(category=cats['clothing'], name='Lightweight Running Jacket', slug='running-jacket',
                 description='Wind-resistant, water-repellent, and packable into its own pocket. Reflective details for visibility.',
                 price='6400', original_price='9000', stock=12),

            # Home & Kitchen
            dict(category=cats['home-kitchen'], name='Pour-Over Coffee Set', slug='pour-over-coffee-set',
                 description='Borosilicate glass dripper, server, and 100 filters. Makes a clean, bright cup in under 4 minutes.',
                 price='4200', stock=30, is_featured=True),
            dict(category=cats['home-kitchen'], name='Cast Iron Skillet 10"', slug='cast-iron-skillet-10',
                 description='Pre-seasoned with organic flaxseed oil. Oven-safe to 500°F. Goes from stovetop to table.',
                 price='3500', original_price='5000', stock=20),
            dict(category=cats['home-kitchen'], name='Bamboo Cutting Board Set', slug='bamboo-cutting-board-set',
                 description='Set of 3 reversible boards — S, M, L. Juice groove, anti-slip feet, and natural antibacterial surface.',
                 price='2800', stock=0),  # out of stock example

            # Books
            dict(category=cats['books'], name='The Design of Everyday Things', slug='design-everyday-things',
                 description='Don Norman\'s classic on human-centered design. Essential reading for anyone who makes things people use.',
                 price='1899', stock=60),
            dict(category=cats['books'], name='Deep Work', slug='deep-work',
                 description='Cal Newport on the lost art of focused concentration — and how to cultivate it in a distracted world.',
                 price='1499', original_price='2000', stock=45),
        ]

        count = 0
        for p in products:
            _, created = Product.objects.get_or_create(slug=p['slug'], defaults=p)
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'✓ Seeded {count} products across {len(cats)} categories'))
