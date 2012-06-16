from django.core.management.base import BaseCommand, CommandError
from content.models import InterestGroup, IgProposal, IgProposalForm, Entry
import os


class Command(BaseCommand):
    args = ''
    help = 'Updates the post number of every Interest Group.'
    def handle(self, *args, **options):
        entries = Entry.objects.all()
        for entry in entries:
            total = entry.posts + entry.double_posts * 2

            entry.last_growth = ((total - entry.last_score)/entry.last_score) * 100
            if entry.last_growth > 0.0:
                print entry, total, entry.last_growth
            entry.last_score = total
            entry.save()
            
            
            
    

        self.stdout.write('Success\n')
