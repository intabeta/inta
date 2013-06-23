from django.core.management.base import BaseCommand, CommandError
from content.models import Entry, Graph
from taggit.models import Tag
from collections import defaultdict
import os

class Command(BaseCommand):
    args = ''
    help = 'Updates universe view'
    def handle(self, *args, **options):
        tags = Tag.objects.all()
        entries = Entry.objects.all()
        tagscores = defaultdict(int)
        for method in ('votes','decay1','decay2','decay3','decay4','decay5','decay6','decay7','decay8'):
            edges=[]
            for entry in entries:
                etags = entry.tags.all()
                ranks = [ entry._get_ranking(tag,method) for tag in etags ]
                for i, tag1 in enumerate(etags):
                    rank1 = ranks[i]
                    tagscores[tag1.id] += rank1
                    for j, tag2 in enumerate(etags[i+1:],i+1):
                        s = int(round(rank1+ranks[j]))
                        if s>0:
                            edges.append([tag1.id,tag2.id,s])

            nztags = [ tag.id for tag in tags if round(tagscores[tag.id]) > 1 ] #nonzero tags (also excludes tags with a score of only 1)
            edges2=[ e for e in edges if e[0] in nztags and e[1] in nztags]
##            for e in edges:
##                if e[0] in nztags and e[1] in nztags: #only consider edges that were connected to two nonzero tags and have nonzero strength
##                    edges2.append(e)
            
            points= [ [tag,int(round(tagscores[tag]))] for tag in nztags ]

            graph = Graph.objects.get(name = method)
            graph.points = points
            graph.edges = edges2
            self.stdout.write(method+': '+str(len(str(points)))+', '+str(len(str(edges2)))+'\n')
            graph.save()
            
