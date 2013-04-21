from django.core.management.base import BaseCommand, CommandError
from content.models import Entry, Dict
from taggit.models import Tag
import os

class Command(BaseCommand):
    args = ''
    help = 'Updates top tags Dict (id=193, name=PaqubeSTUPhACh8trust62Ex6Ve5am).'
    def handle(self, *args, **options):
        toptags = Dict.objects.get(id=193)
        #empty old toptags dict
        for tagval in toptags.tagval_set.all():
            tagval.delete()

        #calculate new top tags and place in dict
        newtoptags = sorted([[tag.name,sum([a._get_ranking(tag) for a in Entry.objects.all()])]for tag in Tag.objects.all()], key=lambda a: -a[1])
        for tagval in newtoptags:
            toptags.tagval_set.create(tag=tagval[0], val=tagval[1])

        print('New top tags:\n'+sum([ a[0]+': '+str(a[1])+'\n'] for a in newtoptags))
