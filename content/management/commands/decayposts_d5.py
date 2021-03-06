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
        tagscores_d5 = defaultdict(int)
        now = datetime.utcnow()
        for entry in entries:
            then = entry.date_added.replace(tzinfo=None)
            lapsed = now - then

            if lapsed.total_seconds() < 1209600: #restrict decay5 to looking at posts under 2 weeks old
                d5 = base ** (lapsed.total_seconds()/604800)

                entry.score = 0
                entry.d5 = round(d5,4)
                
                for tag in entry.tags.all():
                    score = entry._get_ranking(tag) #posts + 2*double_posts
                    entry.score += score
                    tagscores_d5[tag] += score*d5
                entry.save()

        ls = list(tagscores_d5.items())
        toptags = topn(ls, min(20,len(ls)), lambda i: i[1])
        dl = Dict.objects.get(id=198)
        for tv in dl.tagval_set.all():
            tv.delete()
        for tv in toptags:
            dl.tagval_set.create(tag=tv[0],val=round(tv[1]))
        self.stdout.write('Success\n')
