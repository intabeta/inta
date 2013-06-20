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
        tagscores_d2 = defaultdict(int)
        now = datetime.utcnow()
        for entry in entries:
            then = entry.date_added.replace(tzinfo=None)
            lapsed = now - then
            if lapsed.total_seconds() < 43200: #consider only posts less than 12 hours old
                d2 = base ** (lapsed.total_seconds()/10800)

                entry.d2 = round(d2,4)
                entry.score = 0

                for tag in entry.tags.all():
                    total = entry._get_ranking(tag) #posts + 2*double_posts
                    entry.score += total
                    tagscores_d2[tag] += total*d2
                entry.save()

        toptags = topn(list(tagscores_d2.items()), 20, lambda i: i[1])
        dl = Dict.objects.get(id=195)
        for tv in dl.tagval_set.all():
            tv.delete()
        for tv in toptags:
            dl.tagval_set.create(tag=tv[0],val=tv[1])
        self.stdout.write('Success\n')
