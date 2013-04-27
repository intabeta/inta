from django.core.management.base import BaseCommand, CommandError
from content.models import InterestGroup, IgProposal, IgProposalForm, Entry, Logo
from django.core.mail import send_mail
import os


class Command(BaseCommand):
    args = ''
    help = 'Find domains without logo.'
    def handle(self, *args, **options):
        entries = Entry.objects.all()
        noimage = []
        for entry in entries:
            d = entry.domain
            l = Logo.objects.filter(site=d)
            if not l.exists():
                print l, d
                if not d in noimage:
                    noimage.append(d)
                
        message= "Domains without logos:\n\n"
        for domain in noimage:
            message  = message + "%s\n" % domain
        message = message + "\nTotal %d domains" % len(noimage)
        send_mail('No image domains', message, 'info@intabeta.com', ('bwloeb5@gmail.com',), fail_silently=False)

        self.stdout.write('Success\n')
