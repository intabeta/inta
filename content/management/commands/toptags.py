from django.core.management.base import BaseCommand, CommandError
from content.models import Entry, Dict
from taggit.models import Tag
import os

class Command(BaseCommand):
    args = ''
    help = 'Updates top tags Dict (id=193, name=PaqubeSTUPhACh8trust62Ex6Ve5am).'
    def handle(self, *args, **options):
        #load dicts
        toptags = Dict.objects.get(id=193)
        toptags_d1 = Dict.objects.get(id=194)
        toptags_d2 = Dict.objects.get(id=195)
        toptags_d3 = Dict.objects.get(id=196)
        toptags_d4 = Dict.objects.get(id=197)
        toptags_d5 = Dict.objects.get(id=198)
        toptags_d6 = Dict.objects.get(id=199)
        toptags_d7 = Dict.objects.get(id=200)
        toptags_d8 = Dict.objects.get(id=201)
        top_sites = Dict.objects.get(id=322)

        #calculate new top tags, empty old ones, and put in the new
        newtoptags = sorted([[tag.name,sum([a._get_ranking(tag) for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d1 = sorted([[tag.name,sum([ a._get_ranking(tag,'decay1') for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d2 = sorted([[tag.name,sum([ a._get_ranking(tag,'decay2') for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d3 = sorted([[tag.name,sum([ a._get_ranking(tag,'decay3') for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d4 = sorted([[tag.name,sum([ a._get_ranking(tag,'decay4') for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d5 = sorted([[tag.name,sum([ a._get_ranking(tag,'decay5') for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d6 = sorted([[tag.name,sum([ a._get_ranking(tag,'decay6') for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d7 = sorted([[tag.name,sum([ a._get_ranking(tag,'decay7') for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d8 = sorted([[tag.name,sum([ a._get_ranking(tag,'decay8') for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])

        for tagval in toptags.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags:
            toptags.tagval_set.create(tag=tagval[0], val=int(tagval[1]))
        
        for tagval in toptags_d1.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d1:
            toptags_d1.tagval_set.create(tag=tagval[0], val=int(tagval[1]))
        
        for tagval in toptags_d2.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d2:
            toptags_d2.tagval_set.create(tag=tagval[0], val=int(tagval[1]))

        for tagval in toptags_d3.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d3:
            toptags_d3.tagval_set.create(tag=tagval[0], val=int(tagval[1]))

        for tagval in toptags_d4.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d4:
            toptags_d4.tagval_set.create(tag=tagval[0], val=int(tagval[1]))

        for tagval in toptags_d5.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d5:
            toptags_d5.tagval_set.create(tag=tagval[0], val=int(tagval[1]))

        for tagval in toptags_d6.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d6:
            toptags_d6.tagval_set.create(tag=tagval[0], val=int(tagval[1]))

        for tagval in toptags_d7.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d7:
            toptags_d7.tagval_set.create(tag=tagval[0], val=int(tagval[1]))

        for tagval in toptags_d8.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d8:
            toptags_d8.tagval_set.create(tag=tagval[0], val=int(tagval[1]))

