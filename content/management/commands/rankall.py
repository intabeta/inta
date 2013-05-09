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

        topposts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag) for tag in tags]))
        top = DataList.objects.get(id=2)
        top.data = topposts
        top.save()

        topposts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag,'decay1') for tag in tags]))
        top = DataList.objects.get(id=3)
        top.data = topposts
        top.save()

        topposts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag,'decay2') for tag in tags]))
        top = DataList.objects.get(id=4)
        top.data = topposts
        top.save()

        topposts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag,'decay3') for tag in tags]))
        top = DataList.objects.get(id=5)
        top.data = topposts
        top.save()

        topposts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag,'decay4') for tag in tags]))
        top = DataList.objects.get(id=6)
        top.data = topposts
        top.save()

        topposts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag,'decay5') for tag in tags]))
        top = DataList.objects.get(id=7)
        top.data = topposts
        top.save()

        topposts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag,'decay6') for tag in tags]))
        top = DataList.objects.get(id=8)
        top.data = topposts
        top.save()

        topposts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag,'decay7') for tag in tags]))
        top = DataList.objects.get(id=9)
        top.data = topposts
        top.save()

        topposts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag,'decay8') for tag in tags]))
        top = DataList.objects.get(id=10)
        top.data = topposts
        top.save()
