from django.core.management.base import BaseCommand, CommandError
from content.models import InterestGroup, IgProposal, IgProposalForm, Entry
import os


class Command(BaseCommand):
    args = ''
    help = 'Updates the post number of every Interest Group.'
    def handle(self, *args, **options):
        igs = InterestGroup.objects.all()
        for ig in igs:
            posts = ig.entry_set.all().count()
            ig.posts = posts
            ig.save()
            print ig.title, posts
            
            
    

        self.stdout.write('Success\n')
