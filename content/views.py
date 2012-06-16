from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from content.models import InterestGroup, IgProposal, IgProposalForm, Entry
from content.forms import SubmitForm, SubmitFormPlugin
from bs4 import BeautifulSoup
from urllib import urlopen, quote_plus
import tldextract
from django.template.defaultfilters import slugify
from django.contrib import messages
from datetime import datetime, timedelta

import re

def get_referer_view(request, default=None):
    ''' 
    Return the referer view of the current request

    Example:

        def some_view(request):
            ...
            referer_view = get_referer_view(request)
            return HttpResponseRedirect(referer_view, '/accounts/login/')
    '''

    # if the user typed the url directly in the browser's address bar
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return default

    # remove the protocol and split the url at the slashes
    referer = re.sub('^https?:\/\/', '', referer).split('/')
    if referer[0] != request.META.get('SERVER_NAME'):
        return default

    # add the slash at the relative path's view and finished
    referer = u'/' + u'/'.join(referer[1:])
    return referer


@login_required
def myig(request):
    """
    The main page presenting subscribed IGs.
    """
    user = request.user
    
    subscribed = user.interestgroup_set.all().order_by('-members')
    
    template_data = {
        'subscribed': subscribed,
    }
    return render_to_response('content/myig.html', template_data, context_instance=RequestContext(request))
    
@login_required
def ig(request):
    """
    The main page presenting IGs.
    """
    user = request.user
    
    
    
    if request.method == 'POST':
        action = request.POST.get('action','')
        ig_slug = request.POST.get('ig_slug','')
        if action == 'join':
            ig_change = get_object_or_404(InterestGroup, slug=ig_slug)
            ig_change.subscribers.add(user)
            ig_change.members = ig_change.members + 1
        else:
            ig_change = get_object_or_404(InterestGroup, slug=ig_slug)
            ig_change.subscribers.remove(user)
            ig_change.members = ig_change.members - 1        
        ig_change.save()
    
    interest_groups = InterestGroup.objects.all().order_by('-members')
    subscribed = user.interestgroup_set.all().order_by('-members')
    member = []
    for ig in subscribed:
        member.append(ig.title)
    
    template_data = {
        'interest_groups': interest_groups,
        'subscribed': subscribed,
        'member': member
    }
    return render_to_response('content/ig.html', template_data, context_instance=RequestContext(request))
    
@login_required
def ig_list(request, slug, method):
    user = request.user

    ig = get_object_or_404(InterestGroup, slug=slug)

    
    voted = user.voters.all()
    double_voted = user.double_voters.all()
    voter = []
    double_voter = []
    for post in voted:
        voter.append(post.slug)
    for post in double_voted:
        double_voter.append(post.slug)     
    
    
    if request.method == 'POST':
        action = request.POST.get('action','')
        post_slug = request.POST.get('post_slug','')
        if post_slug not in voter and post_slug not in double_voter:
            if action == 'vote':
                voter.append(post_slug)
                post_change = get_object_or_404(Entry, slug=post_slug)
                post_change.voted_by.add(user)
                post_change.posts = post_change.posts + 1
                post_change.decayed_score = post_change.decayed_score + 1
                post_change.save()
                if request.user.is_authenticated():
                    messages.success(request, "Thanks for contributing! Enjoy.", fail_silently=True)
                
            if action == 'double_vote':
                double_voter.append(post_slug) 
                post_change = get_object_or_404(Entry, slug=post_slug)
                post_change.double_voted_by.add(user)
                post_change.double_posts = post_change.double_posts + 1
                post_change.decayed_score = post_change.decayed_score + 2
                post_change.save()
                if request.user.is_authenticated():
                    messages.success(request, "Thanks for contributing! Enjoy.", fail_silently=True)

    if method == 'votes':
        posts = sorted(ig.entry_set.all(), key=lambda a: -a.ranking)
    if method == 'growth':
        posts = ig.entry_set.all().order_by('-last_growth', '-decayed_score')
        #posts = sorted(ig.entry_set.all().order_by('-last_growth'), key=lambda a: -a.ranking)
    if method == 'decay':
        posts = ig.entry_set.all().order_by('-decayed_score', '-date_added')  
    if method == 'green':
        posts = sorted(ig.entry_set.filter(date_added__range=(datetime.now()-timedelta(days=1),datetime.now())), key=lambda a: -a.ranking)              
    if method == 'orange':
        posts = sorted(ig.entry_set.filter(date_added__range=(datetime.now()-timedelta(days=3),datetime.now()-timedelta(days=1))), key=lambda a: -a.ranking)              
    if method == 'red':
        posts = sorted(ig.entry_set.filter(date_added__range=(datetime.now()-timedelta(days=6),datetime.now()-timedelta(days=3))), key=lambda a: -a.ranking)              
    if method == 'black':
        posts = sorted(ig.entry_set.filter(date_added__range=(datetime.now()-timedelta(days=365),datetime.now()-timedelta(days=6))), key=lambda a: -a.ranking)              
 
   

    
    template_data = {
        'ig': ig,
        'posts': posts,
        'voter': voter,
        'double_voter': double_voter,
        'method': method
    }
    return render_to_response('content/ig_list.html', template_data, context_instance=RequestContext(request))

@login_required
def ig_proposal(request):
    if request.method == 'POST':
        form = IgProposalForm(request.POST)
        if form.is_valid():
            form.save()
            redirect_to = reverse('content_ig_proposal_done')
            return redirect(redirect_to)
    else:
        form = IgProposalForm()
        
    template_data = {
        'form': form,
    }
    return render_to_response('content/ig_proposal.html', template_data, context_instance=RequestContext(request))    

@login_required
def ig_proposal_done(request):
    template_data = {
    }
    return render_to_response('content/ig_proposal_done.html', template_data, context_instance=RequestContext(request)) 

@login_required
def submit(request):
    user = request.user
    if request.method == 'POST':
        form = SubmitForm(user, request.POST.get('url',''), request.POST)
        
        if form.is_valid():
            ig = get_object_or_404(InterestGroup, slug=form.cleaned_data['ig'])
            entry = Entry.objects.filter(url__iexact = form.cleaned_data['url']).filter(ig=ig)
            if entry:
                form.errors['url'] = ['This link has already been submitted in this Interest Group.']           
            else:
                if '_post' in request.POST:
                    request.session['action'] = 'post'
                if '_double_post' in request.POST:
                    request.session['action'] = 'double_post'
                    
                request.session['url']=form.cleaned_data['url']
                request.session['ig']=form.cleaned_data['ig']

                redirect_to = reverse('content_submit_details')
                return redirect(redirect_to)
    else:
        bkmk = request.GET.get('bkmk','')
        form = SubmitForm(user, bkmk)
    template_data = {
        'form': form
    }
    return render_to_response('content/submit.html', template_data, context_instance=RequestContext(request)) 

@login_required
def submit_plugin(request):
    user = request.user
    if request.method == 'POST':
        form = SubmitFormPlugin(user, request.POST.get('url',''), request.POST)
        
        if form.is_valid():
            ig = get_object_or_404(InterestGroup, slug=form.cleaned_data['ig'])
            entry = Entry.objects.filter(url__iexact = form.cleaned_data['url']).filter(ig=ig)
            if entry:
                form.errors['url'] = ['This link has already been submitted in this Interest Group, and you have voted for it.']
                
                if entry[0] not in user.voters.all() and entry[0] not in user.double_voters.all():
                    if request.user.is_authenticated():
                        messages.success(request, "This link was already submitted in this Interest Group, but we kept your votes for it.", fail_silently=True)
                    action = request.session.get('action','')
                    if action == "post":
                        entry[0].posts = entry[0].posts + 1
                        entry[0].save()
                        entry[0].voted_by.add(user)
                    else:
                        entry[0].double_posts = entry[0].double_posts + 1
                        entry[0].save()
                        entry[0].double_voted_by.add(user)
                    
                    entry[0].save()
                    ig.posts = ig.posts + 1
                    ig.save()
    
                    if 'url' in request.session:
                        del request.session['url']
                    if 'ig' in request.session:
                        del request.session['ig']
                    if 'action' in request.session:
                        del request.session['action']
                    return redirect('/content/ig/%s/votes/' % ig.slug)
                   
            else:
                if '_post' in request.POST:
                    request.session['action'] = 'post'
                if '_double_post' in request.POST:
                    request.session['action'] = 'double_post'
                    
                request.session['url']=form.cleaned_data['url']
                request.session['ig']=form.cleaned_data['ig']

                redirect_to = reverse('content_submit_details')
                return redirect(redirect_to)
    else:
        bkmk = request.GET.get('bkmk','')
        form = SubmitFormPlugin(user, bkmk)
    template_data = {
        'form': form
    }
    return render_to_response('content/submit_plugin.html', template_data, context_instance=RequestContext(request)) 
    
    
@login_required
def submit_details(request):
    referer = get_referer_view(request)
    
    from_site = referer.find('/content/submit/')
    from_plugin = referer.find('/content/submit_plugin/')
    
    if from_site == -1 and from_plugin == -1:
        return redirect('/')
        
    
    user = request.user
    url = request.session.get('url','')
    ig_slug = request.session.get('ig','')
    action = request.session.get('action','')
    
    
    if request.method == 'POST':
        pass
    else:
        results = linter(url)
        ext = tldextract.extract(url)
        
        entry = Entry()
        entry.url = url
        entry.title = results.get('title','Untitled')
        if results.get('description'):
            entry.summary = results.get('description')
        if results.get('image'):
            entry.photo = results.get('image')
        entry.domain = "%s.%s" % (ext.domain, ext.tld)
        entry.submitted_by = user
        
        ig = get_object_or_404(InterestGroup, slug=ig_slug)
        entry.ig = ig
        
        if action == "post":
            entry.posts = 1
            entry.last_score = 1
            entry.decayed_score =  1
            entry.double_posts = 0
            entry.save()
            entry.voted_by.add(user)
        else:
            entry.posts = 0
            entry.double_posts = 1
            entry.last_score = 2
            entry.decayed_score =  2
            entry.save()
            entry.double_voted_by.add(user)
        
        entry.save()
        entry.slug = "%s-%s" % (slugify(entry.title), str(entry.id))
        entry.save()
        ig.posts = ig.posts + 1
        ig.save()
        

        
        if 'url' in request.session:
            del request.session['url']
        if 'ig' in request.session:
            del request.session['ig']
        if 'action' in request.session:
            del request.session['action']

        if request.user.is_authenticated():
            messages.success(request, "Keep it up! You are making the lists stronger.", fail_silently=True)
        
        if from_site != -1:            
            redirect_to = reverse('content_myig')
        else:
            redirect_to = '/autoclose/'
        return redirect(redirect_to)  
#         html5 = urlopen(url).read()
#         soup = BeautifulSoup(html5)
#         title = soup.title.string
#         h1 = soup.find_all('h1')
#         headings = [h.string for h in h1]
#         p1 = soup.find_all('p')
#         paragraphs = [p.string for p in p1 if p.string and len(p.string) > 40]            
#         text = get_text(soup)
#         headings2 = soup.find_all('h2')
#         headings3 = soup.find_all('h3')
        #intros = find_intro(soup)
        
    template_data = {
        'url': url,
        'ig': ig,
        'results': results
        #'title': title,
        #'intros': intros,
        #'headings': headings,
        #'paragraphs': paragraphs,
        #'text': text

    }
    return render_to_response('content/submit_details.html', template_data, context_instance=RequestContext(request)) 


def find_intro(soup):
    headings = soup.find_all('h1')
    intros = []
    for h1 in headings:
        s = []
        s.append(h1.next_simbling)
        s.append(s[0].next_simbling)
        s.append(s[1].next_simbling)
        intro = ''
        for tag in s:
            intro = intro + "%s: %s\n" % (tag.tag, tag.stripped_strings)
            
        intros.append(intro)
        
    return intros
            
def get_text(soup):
    paragraphs = soup.find_all('p')
    text = []
    for p in paragraphs:
        for s in p.stripped_strings:
            if len(s) > 70:
                text.append(s)
    
    return text
    
def linter(url):
    encurl = quote_plus(url)
    html5 = urlopen("http://developers.facebook.com/tools/debug/og/object?q=" + encurl).read()
    #html5 = urlopen("https://developers.facebook.com/tools/lint/?url=" + encurl + "&format=json").read()
    soup = BeautifulSoup(html5)
    data = soup.find_all('td')
    prev = [x.previous_element for x in data]
    results = {}
    for cell in data:
        if cell.previous_element  == u'og:title:':
            results["title"] = cell.string
        if cell.previous_element  == u'og:description:':
            results["description"] = cell.string
        if cell.previous_element  == u'og:image:':
            href = cell.span.img['src']
            results["image"] = href
    return results
    
