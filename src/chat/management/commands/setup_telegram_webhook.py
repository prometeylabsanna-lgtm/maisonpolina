from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from src.chat.services.telegram_bot import TelegramBotError, delete_webhook, set_webhook


class Command(BaseCommand):
    help = "Register Telegram webhook URL and secret token via Bot API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete the current webhook instead of setting it",
        )
        parser.add_argument(
            "--url",
            default="",
            help="Override TELEGRAM_WEBHOOK_URL for this run",
        )

    def handle(self, *args, **options):
        token = (getattr(settings, "TELEGRAM_BOT_TOKEN", "") or "").strip()
        if not token:
            raise CommandError("TELEGRAM_BOT_TOKEN is not set")

        if options["delete"]:
            try:
                result = delete_webhook()
            except TelegramBotError as exc:
                raise CommandError(str(exc)) from exc
            self.stdout.write(self.style.SUCCESS(f"Webhook deleted: {result}"))
            return

        url = (options["url"] or getattr(settings, "TELEGRAM_WEBHOOK_URL", "") or "").strip()
        secret = (getattr(settings, "TELEGRAM_WEBHOOK_SECRET", "") or "").strip()
        if not url:
            raise CommandError("TELEGRAM_WEBHOOK_URL is not set (or pass --url)")
        if not secret:
            raise CommandError("TELEGRAM_WEBHOOK_SECRET is not set")
        if not url.startswith("https://"):
            raise CommandError("Webhook URL must use HTTPS")

        try:
            result = set_webhook(url, secret)
        except TelegramBotError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(self.style.SUCCESS(f"Webhook set: {url}"))
        self.stdout.write(str(result))
