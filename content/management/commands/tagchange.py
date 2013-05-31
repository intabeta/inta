from django.core.management.base import BaseCommand, CommandError
from content.models import Entry
from taggit.models import Tag
import os

class Command(BaseCommand):
    args = ''
    help = 'Decay for entry scores.'
    def handle(self, *args, **options):
        taginput = raw_input('Which tag do you want to change?  ')
        tagchange = Tag.objects.filter(name = taginput)
        if tagchange:
            tagchange = tagchange[0]
            print('found '+str(tagchange)+'.')
        else:
            print('no tag with the name '+taginput+' exists.')
            return
        newtaginput = raw_input('What would you like to change it to?  ')
        print('Changing tag '+str(taginput)+' to '+str(newtaginput)+'...')
            
        
