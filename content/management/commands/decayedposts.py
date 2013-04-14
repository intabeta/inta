from django.core.management.base import BaseCommand, CommandError
from content.models import InterestGroup, IgProposal, IgProposalForm, Entry
import os
from datetime import datetime, timedelta

class Command(BaseCommand):
    args = ''
    help = 'Decay for entry scores.'
    def handle(self, *args, **options):
        entries = Entry.objects.all()
        for entry in entries:
            total = entry.posts + entry.double_posts * 2
            now = datetime.utcnow()
            then = entry.date_added.replace(tzinfo=None)
            lapsed = now - then
            print lapsed.total_seconds()
            entry.decayed_score_1 = total * (1 / 1.15 ** (lapsed.total_seconds() / 28800))
            print total, entry.decayed_score_1
            entry.save()
        self.stdout.write('Success\n')