from django.core.management.base import BaseCommand

from orders.poller import poll_updates


class Command(BaseCommand):
    help = "Run the Telegram bot"

    def handle(self, *args, **options):
        self.stdout.write("Starting Telegram bot...")
        poll_updates()
