from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Dict(models.Model): #collection of TagVals or Voters (associated by ForeignKeys)
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name

class TagVal(models.Model): #holds a tag and associated value, like posts, double posts, favorites, etc.
    container = models.ForeignKey(Dict, db_index=True)
    tag = models.CharField(max_length=100, db_index=True)
    val = models.FloatField(null=True, db_index=True)

    def __unicode__(self):
        return self.tag+', '+str(self.val)

class Voter(models.Model): #used to keep track of who has voted for which posts under which tags
    container = models.ForeignKey(Dict, db_index=True)
    tag = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    val = models.IntegerField() #1 or 2 for post/double post
    slug = models.SlugField(max_length=200)

    def __unicode__(self):
        return str(self.val)+' votes on '+str(self.slug)+', tag '+self.tag

class InterestGroup(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    members = models.IntegerField(default=0, editable=False)
    posts = models.IntegerField(default=0, editable=False)
    description = models.TextField(blank=True, null=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True)
    
    class Meta:
        ordering = ['title']
        
    def __unicode__(self):
        return self.title
        
class IgProposal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    #private_group = models.BooleanField(default=False)
    #username = models.CharField(max_length=50, blank=True, null=True)
    date_submitted = models.DateField(editable=False, auto_now_add=True)
    
    class Meta:
        ordering = ['date_submitted']
        
    def __unicode__(self):
        return self.title

class DataList(models.Model): #used for storing ordered data like ids of top tags or entries
    name = models.CharField(max_length=100)
    data = models.CommaSeparatedIntegerField(max_length=15000, null=True)

    def __unicode__(self):
        return self.name

class IgProposalForm(ModelForm):
    class Meta:
        model = IgProposal

class Graph(models.Model):
    name = models.CharField(max_length=20)
    edges = models.CharField(max_length=50000)
    points = models.CharField(max_length=50000)

    def __unicode__(self):
        return self.name


class Logo(models.Model):
    site = models.CharField(max_length=100, unique = True)
    logo = models.ImageField(upload_to='site_logos')

    def __unicode__(self):
        return self.site       

class Entry(models.Model):
    url = models.URLField(max_length=1000)

    # content related fields
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    photo = models.URLField(max_length=1000, blank=True)
    #photo = models.ImageField(upload_to='entry_photos', blank=True)
    domain = models.CharField(max_length=200)
    summary = models.TextField(blank=True, null=True)
    score = models.IntegerField(default=0)
    score_d1 = models.IntegerField(default=0)
    score_d2 = models.IntegerField(default=0)
    score_d3 = models.IntegerField(default=0)
    score_d4 = models.IntegerField(default=0)
    score_d5 = models.IntegerField(default=0)
    score_d6 = models.IntegerField(default=0)
    score_d7 = models.IntegerField(default=0)
    score_d8 = models.IntegerField(default=0)

    # user related fields
    submitted_by = models.ForeignKey(User, related_name='submitter', editable=False)
    favorited_by = models.ManyToManyField(User, related_name='favorited', editable=False, blank=True, null=True) #could use a ForeignKey to Dict of Voters if you want to keep track of under what tag it was favorited
    voted_by = models.ForeignKey(Dict, related_name='+', editable=False, blank=True, null=True) #reference a Dict of Voters
    date_added = models.DateTimeField(editable=False, auto_now_add=True)
    posts = models.ForeignKey(Dict, related_name='+') #reference a Dict containing tags and associated post counts
    double_posts = models.ForeignKey(Dict, related_name='+')
    favorites = models.ForeignKey(Dict, related_name='+')
        
    tags = TaggableManager()
    
    #Banned and flagged
    banned = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    
    #Growth
    last_score = models.IntegerField(editable=False, default=1) #still need to be updated for tags
    last_growth = models.DecimalField(max_digits=12, decimal_places=6, editable=False,  default=0.0)
    
    # Decay
    decayed_score_1 = models.ForeignKey(Dict, related_name='+') #each of these references a Dict which keeps track of decayed scores for each tag
    decayed_score_2 = models.ForeignKey(Dict, related_name='+')
    decayed_score_3 = models.ForeignKey(Dict, related_name='+')
    decayed_score_4 = models.ForeignKey(Dict, related_name='+')
    decayed_score_5 = models.ForeignKey(Dict, related_name='+')
    decayed_score_6 = models.ForeignKey(Dict, related_name='+')
    decayed_score_7 = models.ForeignKey(Dict, related_name='+')
    decayed_score_8 = models.ForeignKey(Dict, related_name='+')


    
    class Meta:
        ordering = ['date_added']
        verbose_name_plural = "Entries"
        
    def __unicode__(self):
        return self.title     
        
    def _get_ranking(self, tag, method='votes'):
        if method=='votes':
            try: #these try-except clauses are to deal with errors arising if a post has either no posts or no double posts
                posts = self.posts.tagval_set.get(tag=tag).val
            except:
                posts = 0
            try:
                dbposts = self.double_posts.tagval_set.get(tag=tag).val
            except:
                dbposts = 0
            return posts + 2*dbposts
        if method=='decay1':
            try:
                return self.decayed_score_1.tagval_set.get(tag=tag).val
            except:
                return 0
        if method=='decay2':
            try:
                return self.decayed_score_2.tagval_set.get(tag=tag).val
            except:
                return 0
        if method=='decay3':
            try:
                return self.decayed_score_3.tagval_set.get(tag=tag).val
            except:
                return 0
        if method=='decay4':
            try:
                return self.decayed_score_4.tagval_set.get(tag=tag).val
            except:
                return 0
        if method=='decay5':
            try:
                return self.decayed_score_5.tagval_set.get(tag=tag).val
            except:
                return 0
        if method=='decay6':
            try:
                return self.decayed_score_6.tagval_set.get(tag=tag).val
            except:
                return 0
        if method=='decay7':
            try:
                return self.decayed_score_7.tagval_set.get(tag=tag).val
            except:
                return 0
        if method=='decay8':
            try:
                return self.decayed_score_8.tagval_set.get(tag=tag).val
            except:
                return 0
        
    ranking = property(_get_ranking)
    
    def _get_logo(self):
        domain = Logo.objects.get(site=self.domain)
        if domain is None:
            return None
        else:
            return domain.logo
    logo = property(_get_logo)

class FavoriteTag(models.Model):
    user = models.ForeignKey(User)
    tags = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.tags

class FavoriteEntry(models.Model):
    user = models.ForeignKey(User)
    entry = models.ForeignKey(Entry)

    def __unicode__(self):
        return self.entry.title

class InterestEmail(models.Model):
    email = models.EmailField(max_length=1000)
