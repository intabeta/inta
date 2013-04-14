from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

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

class IgProposalForm(ModelForm):
    class Meta:
        model = IgProposal


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

    # user related fields
    submitted_by = models.ForeignKey(User, related_name='submitter', editable=False)
    favorited_by = models.ManyToManyField(User, related_name='favorited', editable=False, blank=True, null=True)
    voted_by = models.ManyToManyField(User, related_name='voters', editable=False, blank=True, null=True)
    double_voted_by = models.ManyToManyField(User, related_name='double_voters', editable=False, blank=True, null=True)
    date_added = models.DateTimeField(editable=False, auto_now_add=True)
    posts = models.IntegerField()
    double_posts = models.IntegerField()
    favorites = models.IntegerField(default=0)
    
    ig = models.ForeignKey(InterestGroup)
    
    #Banned and flagged
    banned = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    
    #Growth
    last_score = models.IntegerField(editable=False, default=1)
    last_growth = models.DecimalField(max_digits=12, decimal_places=6, editable=False,  default=0.0)
    
    # Decay
    decayed_score_1 = models.DecimalField(max_digits=12, decimal_places=6,  default=0.0)

    
    class Meta:
        ordering = ['date_added']
        verbose_name_plural = "Entries"
        
    def __unicode__(self):
        return self.title     
        
    def _get_ranking(self):
        return self.posts + ( self.double_posts * 2 )
    ranking = property(_get_ranking)
    
    def _get_logo(self):
        domain = Logo.objects.get(site=self.domain)
        if domain is None:
            return None
        else:
            return domain.logo
    logo = property(_get_logo)

class InterestEmail(models.Model):
	email = models.EmailField(max_length=1000)