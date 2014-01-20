import urllib2
from bs4 import BeautifulSoup
import tldextract
from django.template.defaultfilters import slugify
import re
import json
import string
import urlparse

from content.models import Entry, DataList, Dict, Logo
from content.views import linter
from django.contrib.auth.models import User
from taggit.models import Tag
from autotag.keywords import getkeywords

urls = [('http://rss.cnn.com/rss/cnn_topstories.rss',['CNN']),('http://sports.espn.go.com/espn/rss/news',['Sports','ESPN']),('http://feeds.washingtonpost.com/rss/rss_the-fix',['Politics','WP']),('http://online.wsj.com/xml/rss/3_7085.xml',['World News','WSJ'])]

def getlinks(url): #url should be link to rss feed
    url = urllib2.urlopen(url)
    html = ''.join(url.readlines())
    soup = BeautifulSoup(html)

    links = [link.text for link in soup.find_all('link')] #get text from all 'link' tags
    cleaned = [link.split('?')[0] for link in links] #strip off query strings
    return cleaned

def submit_rss(urls=urls):
    for site in urls:
        url = site[0]
        tags = site[1]
        links = getlinks(url)
        print(site,tags)
        for link in links:
            print(link)
            submit(link,tags)

def submit(url,tags2=[]): #submit url with auto-generated tags and possibly pre-specified ones (tags2)
    try:
        post = Entry.objects.get(url=url)
    except Entry.DoesNotExist:
        withurl=Entry.objects.filter(url__iexact=url) #collect all posts with the submitted url (should be only 1)
        tags = [tag for tag in tags2] #make a shallow copy
        tags.extend([tup[0] for tup in getkeywords(url)]) #getkeywords actually returns tuples of (keyword, n); we only want the keywords here
        if not tags: #don't submit if there are no tags to add
            return
        entry = None
        user = User.objects.get(id=43) #submitbot user
        if withurl:
            for tag in tags: #consider each of the specified tags individually
                #load or create the tag
                tagcheck = Tag.objects.filter(name__iexact=tag)
                if tagcheck:
                    newtag = tagcheck[0]
                else:
                    newtag = Tag(name=tag)
                    newtag.save()
                #make tag active so that ranktags knows to look at it
                activetags = eval(DataList.objects.get(id=1).data)
                if newtag.id not in activetags:
                    activetags.append(newtag.id)
                    d = DataList.objects.get(id=1)
                    d.data = activetags
                    d.save()
                    del d
                entry = withurl.filter(tags__name__in=[tag]) #find out if it already has the given tag
                if entry: #add a 'good' vote if it does
                    tagval=entry[0].posts.tagval_set.get(tag__name_iexact=tag)
                    tagval.val += 1
                    tagval.save()
                    entry[0].voted_by.voter_set.create(tag=tag, user=user, val=1, slug=entry[0].slug)

                    entry[0].save()
                else: #otherwise add tag and a 'good' vote
                    post = request.session.get('post', '')
                    withurl[0].tags.add(newtag)
                    withurl[0].posts.tagval_set.create(tag=newtag, val=1)
                    withurl[0].voted_by.voter_set.create(tag=tag, user=user, val=1, slug=withurl[0].slug)

                    withurl[0].save()

        else: #add entry and tags
            results = linter(url)
            ext = tldextract.extract(url)

            #create entry
            entry = Entry()
            entry.url = url
            entry.title = results.get('title', 'Untitled')
            if results.get('description'):
                entry.summary = results.get('description')
            if results.get('image'):
                entry.photo = results.get('image')
            entry.domain = '%s.%s' % (ext.domain, ext.tld)
            entry.submitted_by = user

            #initialize dictionaries for entry
            postsdict = Dict(name=entry.url)
            postsdict.save()
            entry.posts=postsdict

            dblpostsdict = Dict(name=entry.url)
            dblpostsdict.save()
            entry.double_posts = dblpostsdict

            favdict = Dict(name=entry.url)
            favdict.save()
            entry.favorites = favdict

            voterdict = Dict(name=entry.url)
            voterdict.save()
            entry.voted_by = voterdict

            #slugify
            entry.slug = '%s-%s' % (slugify(entry.title), str(entry.id))
            entry.save()
##                action = request.session.get('action','')
            for tagname in tags:
                #if the tag already exists grab it, otherwise create a new one
                tagcheck = Tag.objects.filter(name__iexact=tagname)
                print(tagname)
                if tagcheck:
                    newtag = tagcheck[0]
                else:
                    newtag = Tag(name=tagname)
                    newtag.save()

                #make tag active so that ranktags knows to look at it
                activetags = eval(DataList.objects.get(id=1).data)
                if newtag.id not in activetags:
                    activetags.append(newtag.id)
                    d = DataList.objects.get(id=1)
                    d.data = activetags
                    d.save()
                    del d

                #add 'good' vote
                entry.posts.tagval_set.create(tag=newtag, val=1)
                entry.voted_by.voter_set.create(tag=tagname, user=user, val=1, slug=entry.slug)
                entry.tags.add(newtag)
                entry.save()

            #try to pull in image from twitter, if it exists.
            domains = Logo.objects.filter(site__iexact=entry.domain)
            r = list(domains[:1])
            if not r:
                logo = Logo()
                logo.site = entry.domain
                try:
                    googleResult = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=twitter.com+' + logo.site).read()
                    results = json.loads(googleResult)
                    data = results['responseData']['results']
                    urls = [e['url'] for e in data]

                    for url in urls:
                        if re.search(r"https?://(www\.)?twitter.com/\w+", url):
                            contents = urllib2.urlopen(url).read()
                            start = string.find(contents,"profile-picture")
                            start = string.find(contents,"src=",start)
                            m = re.search(r"src=\"([A-Za-z\.:/_0-9\-]+)\"",contents[start:])
                            if m:
                                image_url = m.group(1)
                                split = urlparse.urlsplit(image_url)
                                localPath = settings.MEDIA_ROOT + "site_logos/" + split.path.split("/")[-1]
                                urlretrieve(image_url, localPath)
                                logo.logo = "site_logos/" + split.path.split("/")[-1]
                                logo.save()
                            break #only first matching
                except:
                    logo = None
    
