from django.core.management.base import BaseCommand, CommandError
from content.models import Entry, Dict
from taggit.models import Tag
import os

class Command(BaseCommand):
    args = ''
    help = 'Updates top tags Dict (id=193, name=PaqubeSTUPhACh8trust62Ex6Ve5am).'
    def handle(self, *args, **options):
        tagsnentries = [ [tag,Entry.objects.filter(tags__name__in=[tag])] for tag in Tag.objects.all() ] #an array of each tag paired with a list of entries with that tag
        
        toptags = Dict.objects.get(id=193)
        newtoptags = sorted([[te[0].name,sum([a._get_ranking(te[0]) for a in te[1]])] for te in tagsnentries], key=lambda a: -a[1])
        for tagval in toptags.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags:
            toptags.tagval_set.create(tag=tagval[0], val=int(tagval[1]))
        del toptags,newtoptags

        toptags_d1 = Dict.objects.get(id=194)
        newtoptags_d1 = [[te[0].name,sum([ a._get_ranking(te[0],'decay1') for a in te[1]])] for te in tagsnentries]
        for tagval in toptags_d1.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d1:
            toptags_d1.tagval_set.create(tag=tagval[0], val=int(tagval[1]))
        del toptags_d1,newtoptags_d1

        toptags_d2 = Dict.objects.get(id=195)
        newtoptags_d2 = [[te[0].name,sum([ a._get_ranking(te[0],'decay2') for a in te[1]])] for te in tagsnentries]
        for tagval in toptags_d2.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d2:
            toptags_d2.tagval_set.create(tag=tagval[0], val=int(tagval[1]))
        del toptags_d2,newtoptags_d2

        toptags_d3 = Dict.objects.get(id=196)
        newtoptags_d3 = [[te[0].name,sum([ a._get_ranking(te[0],'decay3') for a in te[1]])] for te in tagsnentries]
        for tagval in toptags_d3.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d3:
            toptags_d3.tagval_set.create(tag=tagval[0], val=int(tagval[1]))
        del toptags_d3,newtoptags_d3

        toptags_d4 = Dict.objects.get(id=197)
        newtoptags_d4 = [[te[0].name,sum([ a._get_ranking(te[0],'decay4') for a in te[1]])] for te in tagsnentries]
        for tagval in toptags_d4.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d4:
            toptags_d4.tagval_set.create(tag=tagval[0], val=int(tagval[1]))
        del toptags_d4,newtoptags_d4

        toptags_d5 = Dict.objects.get(id=198)
        newtoptags_d5 = [[te[0].name,sum([ a._get_ranking(te[0],'decay5') for a in te[1]])] for te in tagsnentries]
        for tagval in toptags_d5.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d5:
            toptags_d5.tagval_set.create(tag=tagval[0], val=int(tagval[1]))
        del toptags_d5,newtoptags_d5

        toptags_d6 = Dict.objects.get(id=199)
        newtoptags_d6 = [[te[0].name,sum([ a._get_ranking(te[0],'decay6') for a in te[1]])] for te in tagsnentries]
        for tagval in toptags_d6.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d6:
            toptags_d6.tagval_set.create(tag=tagval[0], val=int(tagval[1]))
        del toptags_d6,newtoptags_d6

        toptags_d7 = Dict.objects.get(id=200)
        newtoptags_d7 = [[te[0].name,sum([ a._get_ranking(te[0],'decay7') for a in te[1]])] for te in tagsnentries]
        for tagval in toptags_d7.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d7:
            toptags_d7.tagval_set.create(tag=tagval[0], val=int(tagval[1]))
        del toptags_d7,newtoptags_d7

        toptags_d8 = Dict.objects.get(id=201)
        newtoptags_d8 = [[te[0].name,sum([ a._get_ranking(te[0],'decay8') for a in te[1]])] for te in tagsnentries]
        for tagval in toptags_d8.tagval_set.all():
            tagval.delete()
        for tagval in newtoptags_d8:
            toptags_d8.tagval_set.create(tag=tagval[0], val=int(tagval[1]))
        del toptags_d8,newtoptags_d8

        top_sites = Dict.objects.get(id=322)




