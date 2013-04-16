from django.core.management.base import BaseCommand, CommandError
from content.models import InterestGroup, IgProposal, IgProposalForm, Entry
import os


class Command(BaseCommand):
    args = ''
    help = 'Updates the post number of every Interest Group.'
    def handle(self, *args, **options):
        entries = Entry.objects.all()
        for entry in entries:
            tags = entry.tags.all()
            if tags:
                total = entry._get_ranking(tags[0])

                entry.last_growth = ((total - entry.last_score)/entry.last_score) * 100
                if entry.last_growth > 0.0:
                    print entry, total, entry.last_growth
                entry.last_score = total
                entry.save()
            else:
                entry.last_growth = 0
                entry.last_score = 0
                entry.save
            
    

        self.stdout.write('Success\n')
