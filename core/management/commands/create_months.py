from django.core.management.base import BaseCommand
from datetime import datetime
from core.models import Month   

class Command(BaseCommand):
    help = 'Create Month entries for the current year'

    def handle(self, *args, **kwargs):
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        current_year = datetime.now().year

        created = 0
        skipped = 0

        for month_name in month_names:
            slug = month_name.lower().replace(" ", "-")
            obj, was_created = Month.objects.get_or_create(
                name=month_name,
                year=current_year,
                defaults={'slug': slug}
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'Months created successfully! Created: {created}, Skipped (already exist): {skipped}'
        ))
