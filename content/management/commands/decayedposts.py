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
            base = 0.5
            entry.decayed_score_1 = total * (base ** (lapsed.total_seconds() / 1800)) #
            entry.decayed_score_2 = total * (base ** (lapsed.total_seconds() / 10800)) #
            entry.decayed_score_3 = total * (base ** (lapsed.total_seconds() / 86400)) #
            entry.decayed_score_4 = total * (base ** (lapsed.total_seconds() / 259200)) #
            entry.decayed_score_5 = total * (base ** (lapsed.total_seconds() / 604800)) #
            entry.decayed_score_6 = total * (base ** (lapsed.total_seconds() / 2592000)) #
            entry.decayed_score_7 = total * (base ** (lapsed.total_seconds() / 7776000)) #
            entry.decayed_score_8 = total * (base ** (lapsed.total_seconds() / 31536000)) #
            print total, entry.decayed_score_1
            entry.save()
        self.stdout.write('Success\n')