from django.core.management.base import BaseCommand, CommandError
from content.models import Entry, Dict, DataList
from taggit.models import Tag
import os

class Command(BaseCommand):
    args = ''
    help = 'Updates top tags Dict (id=193, name=top_votes).'
    def handle(self, *args, **options):
        activetaglist = DataList.objects.get(id=1)
        activetagids = eval(activetaglist.data)
        activetaglist.data = []
        activetaglist.save()
        activetags = [ Tag.objects.get(id=val).name for val in activetagids ]

        for tag in activetags:
            relevantposts = Entry.objects.filter(tags__name__in=[tag])

            relevantposts_votes = sorted(relevantposts, key=lambda a: -a._get_ranking(tag))
            votes, c = DataList.objects.get_or_create(name='top_'+tag) #this function returns a tuple; the variable c is either True or False depending on whether a new object was created
            votes.data = [ post.id for post in relevantposts_votes ]
            votes.save()
##            score = 0
##            for post in relevantposts:
##                score += post._get_ranking(tag)
##            toptagsdict = Dict.objects.get(id=193)
##            toptags = [ [tagval.tag, tagval.val] for tagval in toptagsdict.tagval_set.all() ]
##            change=False
##            removelist=[]
##            for i, t in enumerate(toptags): #remove tag from toptags if it's there already to avoid duplicates
##                if t[1] <= score:
##                    change=True
##                if t[0] == tag:
##                    removelist.append(i)
##            for i in removelist:
##                toptags.__delitem__(i)
##            if change:
##                toptags.append([tag,score])
##                for tagval in toptagsdict.tagval_set.all():
##                    tagval.delete()
##                for tagval in sorted(toptags, key=lambda a: -a[1])[:20]:
##                    toptagsdict.tagval_set.create(tag=tagval[0], val=int(tagval[1]))

            relevantposts_d1 = sorted(relevantposts, key=lambda a: -a._get_ranking(tag,'decay1'))
            d1, c = DataList.objects.get_or_create(name='top_d1_'+tag)
            d1.data = [ post.id for post in relevantposts_d1 ]
            d1.save()

            relevantposts_d2 = sorted(relevantposts, key=lambda a: -a._get_ranking(tag,'decay2'))
            d2, c = DataList.objects.get_or_create(name='top_d2_'+tag)
            d2.data = [ post.id for post in relevantposts_d2 ]
            d2.save()

            relevantposts_d3 = sorted(relevantposts, key=lambda a: -a._get_ranking(tag,'decay3'))
            d3, c = DataList.objects.get_or_create(name='top_d3_'+tag)
            d3.data = [ post.id for post in relevantposts_d3 ]
            d3.save()

            relevantposts_d4 = sorted(relevantposts, key=lambda a: -a._get_ranking(tag,'decay4'))
            d4, c = DataList.objects.get_or_create(name='top_d4_'+tag)
            d4.data = [ post.id for post in relevantposts_d4 ]
            d4.save()

            relevantposts_d5 = sorted(relevantposts, key=lambda a: -a._get_ranking(tag,'decay5'))
            d5, c = DataList.objects.get_or_create(name='top_d5_'+tag)
            d5.data = [ post.id for post in relevantposts_d5 ]
            d5.save()

            relevantposts_d6 = sorted(relevantposts, key=lambda a: -a._get_ranking(tag,'decay6'))
            d6, c = DataList.objects.get_or_create(name='top_d6_'+tag)
            d6.data = [ post.id for post in relevantposts_d6 ]
            d6.save()

            relevantposts_d7 = sorted(relevantposts, key=lambda a: -a._get_ranking(tag,'decay7'))
            d7, c = DataList.objects.get_or_create(name='top_d7_'+tag)
            d7.data = [ post.id for post in relevantposts_d7 ]
            d7.save()

            relevantposts_d8 = sorted(relevantposts, key=lambda a: -a._get_ranking(tag,'decay8'))
            d8, c = DataList.objects.get_or_create(name='top_d8_'+tag)
            d8.data = [ post.id for post in relevantposts_d8 ]
            d8.save()
