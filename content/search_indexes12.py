import datetime
from haystack.indexes import *
from haystack import site
from content.models import Entry



class EntryIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr='title')
    summary = CharField(model_attr='summary', null=True)
    last_score = CharField(model_attr='last_score')


    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Entry.objects.filter(date_added__lte=datetime.datetime.now())
        
site.register(Entry, EntryIndex)