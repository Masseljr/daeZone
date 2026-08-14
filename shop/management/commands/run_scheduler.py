"""
Django management command to run APScheduler for order status updates
Usage: python manage.py run_scheduler
"""
from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
import logging

from shop.tasks import update_order_statuses

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run APScheduler to automatically update order statuses'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        
        # Update order statuses every 60 seconds
        scheduler.add_job(
            update_order_statuses,
            trigger=IntervalTrigger(seconds=60),
            id='update_order_statuses',
            name='Update order statuses automatically',
            replace_existing=True,
        )
        
        self.stdout.write(self.style.SUCCESS('Starting order status scheduler...'))
        self.stdout.write(self.style.SUCCESS('Checking orders every 60 seconds'))
        self.stdout.write(self.style.SUCCESS('Press Ctrl+C to exit'))
        
        try:
            scheduler.start()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nScheduler stopped'))
            scheduler.shutdown()
