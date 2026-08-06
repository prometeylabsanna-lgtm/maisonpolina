from django.core.management.base import BaseCommand

from src.leads.services import resend_pending_notifications


class Command(BaseCommand):
    help = "Resend notifications for leads with empty notified_at"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=50)

    def handle(self, *args, **options):
        count = resend_pending_notifications(limit=options["limit"])
        self.stdout.write(self.style.SUCCESS(f"Notified: {count}"))
