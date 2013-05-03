from django.core.management.base import BaseCommand, CommandError
from content.models import Entry, Dict, DataList
from taggit.models import Tag
import os

class Command(BaseCommand):
    args = ''
    help = 'Updates top tags Dict (id=193, name=PaqubeSTUPhACh8trust62Ex6Ve5am).'
    def handle(self, *args, **options):
        activetagids = eval(DataList.objects.get(id=1).data)
        activetags = [ Tag.objects.get(id=val).name for val in activetagids ]

        print('active tags:')
        for tag in activetags:
            print(tag)
            relevantposts = Entry.objects.filter(tags__name__in=[tag])
            relevantposts_votes = sorted(relevantposts, key=lambda a: -a._get_ranking(tag))
            top = DataList.objects.get(name='top_'+tag)
            top.data = [ post.id for post in relevantposts_votes ]
            top.save()

        for entryid in eval(DataList.objects.get(name='top_test').data):
            entry = Entry.objects.get(id=entryid)
            print(entry.title,entry._get_ranking(test))
            

