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
        tagscores_d6 = defaultdict(int)
        now = datetime.utcnow()
        for entry in entries:
            then = entry.date_added.replace(tzinfo=None)
            lapsed = now - then

            if lapsed.total_seconds() < 3628800: #restrict decay6 to looking at posts under 6 weeks old
                d6 = base ** (lapsed.total_seconds()/2592000)

                entry.score = 0
                entry.d6 = round(d6,4)
                
                for tag in entry.tags.all():
                    score = entry._get_ranking(tag) #posts + 2*double_posts
                    entry.score += score
                    tagscores_d6[tag] += score*d6
                entry.save()

        ls = list(tagscores_d6.items())
        toptags = topn(ls, min(20,len(ls)), lambda i: i[1])
        dl = Dict.objects.get(id=199)
        for tv in dl.tagval_set.all():
            tv.delete()
        for tv in toptags:
            dl.tagval_set.create(tag=tv[0],val=round(tv[1]))
        self.stdout.write('Success\n')
