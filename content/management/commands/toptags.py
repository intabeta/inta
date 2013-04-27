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
        
        #empty old toptags dicts
        for tagval in toptags.tagval_set.all():
            tagval.delete()
        for tagval in toptags_d1.tagval_set.all():
            tagval.delete()
        for tagval in toptags_d2.tagval_set.all():
            tagval.delete()
        for tagval in toptags_d3.tagval_set.all():
            tagval.delete()
        for tagval in toptags_d4.tagval_set.all():
            tagval.delete()
        for tagval in toptags_d5.tagval_set.all():
            tagval.delete()
        for tagval in toptags_d6.tagval_set.all():
            tagval.delete()
        for tagval in toptags_d7.tagval_set.all():
            tagval.delete()
        for tagval in toptags_d8.tagval_set.all():
            tagval.delete()

        #calculate new top tags and place in dict
        newtoptags = sorted([[tag.name,sum([a._get_ranking(tag) for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d1 = sorted([[tag.name,sum([ a.decayed_score_1.tagval_set.get(tag__iexact=tag).val for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d2 = sorted([[tag.name,sum([ a.decayed_score_2.tagval_set.get(tag__iexact=tag).val for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d3 = sorted([[tag.name,sum([ a.decayed_score_3.tagval_set.get(tag__iexact=tag).val for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d4 = sorted([[tag.name,sum([ a.decayed_score_4.tagval_set.get(tag__iexact=tag).val for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d5 = sorted([[tag.name,sum([ a.decayed_score_5.tagval_set.get(tag__iexact=tag).val for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d6 = sorted([[tag.name,sum([ a.decayed_score_6.tagval_set.get(tag__iexact=tag).val for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d7 = sorted([[tag.name,sum([ a.decayed_score_7.tagval_set.get(tag__iexact=tag).val for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])
        newtoptags_d8 = sorted([[tag.name,sum([ a.decayed_score_8.tagval_set.get(tag__iexact=tag).val for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])

        for tagval in newtoptags:
            toptags.tagval_set.create(tag=tagval[0], val=tagval[1])
        for tagval in newtoptags_d1:
            toptags_d1.tagval_set.create(tag=tagval[0], val=tagval[1])
        for tagval in newtoptags_d2:
            toptags_d1.tagval_set.create(tag=tagval[0], val=tagval[1])
        for tagval in newtoptags_d3:
            toptags_d1.tagval_set.create(tag=tagval[0], val=tagval[1])
        for tagval in newtoptags_d4:
            toptags_d1.tagval_set.create(tag=tagval[0], val=tagval[1])
        for tagval in newtoptags_d5:
            toptags_d1.tagval_set.create(tag=tagval[0], val=tagval[1])
        for tagval in newtoptags_d6:
            toptags_d1.tagval_set.create(tag=tagval[0], val=tagval[1])
        for tagval in newtoptags_d7:
            toptags_d1.tagval_set.create(tag=tagval[0], val=tagval[1])
        for tagval in newtoptags_d8:
            toptags_d1.tagval_set.create(tag=tagval[0], val=tagval[1])

