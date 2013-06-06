from django.core.management.base import BaseCommand, CommandError
from content.models import Entry, Dict, DataList
from taggit.models import Tag
import os

class Command(BaseCommand):
    args = ''
    help = 'Updates top tags Dict (id=193, name=top_votes).'
    def handle(self, *args, **options):
        tags = Tag.objects.all()
        entries = Entry.objects.all()

        topposts = sorted(entries, key=lambda a: (-a.score,-a.id))
        top = DataList.objects.get(id=2)
        top.data = [ post.id for post in topposts ]
        top.save()

        topposts = sorted(entries, key=lambda a: (-a.score * a.decay_scalars[0],-a.id))
        top = DataList.objects.get(id=3)
        top.data = [ post.id for post in topposts ]
        top.save()

        topposts = sorted(entries, key=lambda a: (-a.score * a.decay_scalars[1],-a.id))
        top = DataList.objects.get(id=4)
        top.data = [ post.id for post in topposts ]
        top.save()

        topposts = sorted(entries, key=lambda a: (-a.score * a.decay_scalars[2],-a.id))
        top = DataList.objects.get(id=5)
        top.data = [ post.id for post in topposts ]
        top.save()

        topposts = sorted(entries, key=lambda a: (-a.score * a.decay_scalars[3],-a.id))
        top = DataList.objects.get(id=6)
        top.data = [ post.id for post in topposts ]
        top.save()

        topposts = sorted(entries, key=lambda a: (-a.score * a.decay_scalars[4],-a.id))
        top = DataList.objects.get(id=7)
        top.data = [ post.id for post in topposts ]
        top.save()

        topposts = sorted(entries, key=lambda a: (-a.score * a.decay_scalars[5],-a.id))
        top = DataList.objects.get(id=8)
        top.data = [ post.id for post in topposts ]
        top.save()

        topposts = sorted(entries, key=lambda a: (-a.score * a.decay_scalars[6],-a.id))
        top = DataList.objects.get(id=9)
        top.data = [ post.id for post in topposts ]
        top.save()

        topposts = sorted(entries, key=lambda a: (-a.score * a.decay_scalars[7],-a.id))
        top = DataList.objects.get(id=10)
        top.data = [ post.id for post in topposts ]
        top.save()
