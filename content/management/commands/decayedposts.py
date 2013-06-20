from django.core.management.base import BaseCommand, CommandError
from content.models import Entry, Dict
from collections import defaultdict
import os
from datetime import datetime, timedelta

def top(ls, key):
	ans=ls[0]
	for item in ls:
		if key(item)>key(ans):
			ans=item
	return ans

def topn(ls, n, key):
	ans=[]
	for i in range(n):
		x=top(ls,key)
		ls.remove(x)
		ans.append(x)
	return ans

class Command(BaseCommand):
    args = ''
    help = 'Decay for entry scores.'
    def handle(self, *args, **options):
        entries = Entry.objects.all()
        base = 0.5
        tagscores = defaultdict(int)
        tagscores_d2 = defaultdict(int)
        tagscores_d3 = defaultdict(int)
        tagscores_d4 = defaultdict(int)
        tagscores_d5 = defaultdict(int)
        tagscores_d6 = defaultdict(int)
        tagscores_d7 = defaultdict(int)
        tagscores_d8 = defaultdict(int)
        for entry in entries:
            now = datetime.utcnow()
            then = entry.date_added.replace(tzinfo=None)
            lapsed = now - then
            entry.score = 0

            d2 = base ** (lapsed.total_seconds()/10800)
            d3 = base ** (lapsed.total_seconds()/86400)
            d4 = base ** (lapsed.total_seconds()/259200)
            d5 = base ** (lapsed.total_seconds()/604800)
            d6 = base ** (lapsed.total_seconds()/2592000)
            d7 = base ** (lapsed.total_seconds()/7776000)
            d8 = base ** (lapsed.total_seconds()/31536000)

            entry.d2 = round(d2,4)
            entry.d3 = round(d3,4)
            entry.d4 = round(d4,4)
            entry.d5 = round(d5,4)
            entry.d6 = round(d6,4)
            entry.d7 = round(d7,4)
            entry.d8 = round(d8,4)
            
            for tag in entry.tags.all():
                total = entry._get_ranking(tag) #posts + 2*double_posts
                entry.score += total
                tagscores[tag] += total
                tagscores_d2[tag] += total*d2
                tagscores_d3[tag] += total*d3
                tagscores_d4[tag] += total*d4
                tagscores_d5[tag] += total*d5
                tagscores_d6[tag] += total*d6
                tagscores_d7[tag] += total*d7
                tagscores_d8[tag] += total*d8
                #print total
                #print(entry.title+'; '+tagnew.name)
            entry.save()
        toptags = topn(list(tagscores.items()), 20, lambda i: i[1])
        dl = Dict.objects.get(id=193)
        for tv in dl.tagval_set.all():
            tv.delete()
        for tv in toptags:
            dl.tagval_set.create(tag=tv[0],val=tv[1])

        toptags = topn(list(tagscores_d2.items()), 20, lambda i: i[1])
        dl = Dict.objects.get(id=195)
        for tv in dl.tagval_set.all():
            tv.delete()
        for tv in toptags:
            dl.tagval_set.create(tag=tv[0],val=tv[1])
        toptags = topn(list(tagscores_d3.items()), 20, lambda i: i[1])
        dl = Dict.objects.get(id=196)
        for tv in dl.tagval_set.all():
            tv.delete()
        for tv in toptags:
            dl.tagval_set.create(tag=tv[0],val=tv[1])
        toptags = topn(list(tagscores_d4.items()), 20, lambda i: i[1])
        dl = Dict.objects.get(id=197)
        for tv in dl.tagval_set.all():
            tv.delete()
        for tv in toptags:
            dl.tagval_set.create(tag=tv[0],val=tv[1])
        toptags = topn(list(tagscores_d5.items()), 20, lambda i: i[1])
        dl = Dict.objects.get(id=198)
        for tv in dl.tagval_set.all():
            tv.delete()
        for tv in toptags:
            dl.tagval_set.create(tag=tv[0],val=tv[1])
        toptags = topn(list(tagscores_d6.items()), 20, lambda i: i[1])
        dl = Dict.objects.get(id=199)
        for tv in dl.tagval_set.all():
            tv.delete()
        for tv in toptags:
            dl.tagval_set.create(tag=tv[0],val=tv[1])
        toptags = topn(list(tagscores_d7.items()), 20, lambda i: i[1])
        dl = Dict.objects.get(id=200)
        for tv in dl.tagval_set.all():
            tv.delete()
        for tv in toptags:
            dl.tagval_set.create(tag=tv[0],val=tv[1])
        toptags = topn(list(tagscores_d8.items()), 20, lambda i: i[1])
        dl = Dict.objects.get(id=201)
        for tv in dl.tagval_set.all():
            tv.delete()
        for tv in toptags:
            dl.tagval_set.create(tag=tv[0],val=tv[1])
        self.stdout.write('Success\n')
