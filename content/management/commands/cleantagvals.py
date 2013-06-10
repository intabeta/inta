from django.core.management.base import BaseCommand, CommandError
from content.models import Entry
from taggit.models import Tag
import os

class Command(BaseCommand):
    args = ''
    help = 'Deletes extraneous TagVals'
    def handle(self, *args, **options):
        entries = Entry.objects.all()

        for entry in entries:
            for tag in entry.tags.all():
                d = entry.posts.tagval_set.filter(tag=tag.name)
                if len(d) > 1: #if there is more than one TagVal with a specific tag, delete the one with the lesser val
                    sorted(d, key=lambda a: a.val)[0].delete()
                d = entry.double_posts.tagval_set.filter(tag=tag.name)
                if len(d) > 1: #if there is more than one TagVal with a specific tag, delete the one with the lesser val
                    sorted(d, key=lambda a: a.val)[0].delete()
                d = entry.decayed_score_1.tagval_set.filter(tag=tag.name)
                if len(d) > 1: #if there is more than one TagVal with a specific tag, delete the one with the lesser val
                    sorted(d, key=lambda a: a.val)[0].delete()
                d = entry.decayed_score_2.tagval_set.filter(tag=tag.name)
                if len(d) > 1: #if there is more than one TagVal with a specific tag, delete the one with the lesser val
                    sorted(d, key=lambda a: a.val)[0].delete()
                d = entry.decayed_score_3.tagval_set.filter(tag=tag.name)
                if len(d) > 1: #if there is more than one TagVal with a specific tag, delete the one with the lesser val
                    sorted(d, key=lambda a: a.val)[0].delete()
                d = entry.decayed_score_4.tagval_set.filter(tag=tag.name)
                if len(d) > 1: #if there is more than one TagVal with a specific tag, delete the one with the lesser val
                    sorted(d, key=lambda a: a.val)[0].delete()
                d = entry.decayed_score_5.tagval_set.filter(tag=tag.name)
                if len(d) > 1: #if there is more than one TagVal with a specific tag, delete the one with the lesser val
                    sorted(d, key=lambda a: a.val)[0].delete()
                d = entry.decayed_score_6.tagval_set.filter(tag=tag.name)
                if len(d) > 1: #if there is more than one TagVal with a specific tag, delete the one with the lesser val
                    sorted(d, key=lambda a: a.val)[0].delete()
                d = entry.decayed_score_7.tagval_set.filter(tag=tag.name)
                if len(d) > 1: #if there is more than one TagVal with a specific tag, delete the one with the lesser val
                    sorted(d, key=lambda a: a.val)[0].delete()
                d = entry.decayed_score_8.tagval_set.filter(tag=tag.name)
                if len(d) > 1: #if there is more than one TagVal with a specific tag, delete the one with the lesser val
                    sorted(d, key=lambda a: a.val)[0].delete()
