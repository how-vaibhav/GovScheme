from django.core.management.base import BaseCommand
from django.utils.text import slugify
from schemesapp.models import Scheme


class Command(BaseCommand):
    help = "Backfill SEO-friendly slugs for all existing Scheme objects that have no slug."

    def handle(self, *args, **kwargs):
        schemes = Scheme.objects.filter(slug="")
        total = schemes.count()
        self.stdout.write(f"Found {total} scheme(s) with no slug. Generating...")

        updated = 0
        for scheme in schemes:
            base_slug = slugify(scheme.name)
            slug = base_slug
            counter = 1
            while Scheme.objects.filter(slug=slug).exclude(pk=scheme.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            scheme.slug = slug
            # Use update() to bypass auto_now on updated_at
            Scheme.objects.filter(pk=scheme.pk).update(slug=slug)
            updated += 1
            self.stdout.write(f"  [{scheme.pk}] {scheme.name!r} → {slug!r}")

        self.stdout.write(self.style.SUCCESS(f"\nDone. {updated} slug(s) generated."))
