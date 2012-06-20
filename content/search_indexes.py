import datetime
from haystack import indexes
from content.models import Entry



class EntryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    summary = indexes.CharField(model_attr='summary', null=True)
    #last_score = indexes.CharField(model_attr='last_score')

    def get_model(self):
        return Entry
        
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
        
