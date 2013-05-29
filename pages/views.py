from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from content.models import InterestGroup, IgProposal, IgProposalForm, Entry, Dict, DataList
from taggit.models import Tag
from haystack.query import SearchQuerySet
from content.views import get_referer_view
from content.models import InterestEmail
from content.forms import EmailForm, SignUpForm
from userena.forms import SignupForm, AuthenticationForm
from userena import signals as userena_signals
from userena import settings as userena_settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from time import time
from content.graphtools import Graph
from re import compile as re_compile
from math import cos, sin, pi, log


def homepage(request):
    user = request.user
    
    if user.is_authenticated():
        return redirect('/content/myig/')
    hot = Entry.objects.all().order_by('-decayed_score_1')[:5]
    return render_to_response('homepage.html', {'hot': hot}, context_instance=RequestContext(request))
    
def autoclose(request):
    return render_to_response('autoclose.html', {}, context_instance=RequestContext(request))

def howto(request):
    return render_to_response('howto.html', {}, context_instance=RequestContext(request))

def mission(request):
    return render_to_response('mission.html', {}, context_instance=RequestContext(request))

def privacy(request):
    return render_to_response('privacy.html', {}, context_instance=RequestContext(request))
    
# def search(request):
#     #freetext = ''
#     #posts = []
#     if request.method == 'POST':
#         freetext = request.POST.get('freetext','')
#         if freetext != '':
#             sqs = SearchQuerySet().filter(content=freetext).order_by('-title')
#         
#             p = []    
#             if sqs:
#                 for o in sqs:
#                     p.append((o.object.last_score, o.object))
#             posts = sorted(p, key=lambda a: -a[0])
#             template_data = {
#                 'freetext': freetext,
#                 'posts': posts,
#             }
#         else:
#             template_data = {
#                 'freetext': '',
#                 'empty': True,
#             }           
#     else:
#         template_data = {
#             'freetext': '',
#             'empty': True,
#         }            
#     return render_to_response('search/search.html', template_data, context_instance=RequestContext(request))

def search(request):
    #freetext = ''
    #posts = []
    if request.method == 'POST':
        freetext = request.POST.get('freetext','')
        if freetext != '':
            sqs = SearchQuerySet().filter(content=freetext).order_by('-title')
        
            p = []    
            if sqs:
                for o in sqs:
                    p.append((o.object.last_score, o.object))
            #posts = sorted(p, key=lambda a: -a[0])
            posts = p
            template_data = {
                'freetext': freetext,
                'posts': posts,
            }
        else:
            template_data = {
                'freetext': '',
                'empty': True,
            }           
    else:
        template_data = {
            'freetext': '',
            'empty': True,
        }            
    return render_to_response('search/search.html', template_data, context_instance=RequestContext(request))

@login_required    
def email(request):
    referer = get_referer_view(request)
    
    from_list = referer.find('/content/ig/')
    from_self = referer.find('/email/')
    
    if from_list == -1 and from_self == -1:
        return redirect('/')
    
    if from_list != -1:    
        if request.method == 'POST':
            posts = []
            entries = request.POST.getlist('entries',[])
            for entry in entries:
                posts.append(get_object_or_404(Entry, slug=entry))
            request.session['posts_email'] = posts
        form = EmailForm()        
        template_data = {
            'entries': entries,
            'posts': posts,
            'form': form,
        }        
        return render_to_response('email.html', template_data, context_instance=RequestContext(request))
    else:
        if request.method == 'POST':
            form = EmailForm(request.POST)
            if form.is_valid():
                posts = request.session.get('posts_email',[])
                user = request.user
                subject = "Your friend found something interesting in INTA"
                from_email = user.email 
                to_email = [form.cleaned_data['email']] 
                message = "Your friend, with email %s, found the following interesting article(s) in intabeta.com and thought you might be interested to have a look.\n\n" % from_email
                for post in posts:
                    message = message + post.title + "\n"
                    message = message + post.url + "\n"
                    message = message + "\n\n"
                
                send_mail(subject, message, from_email, to_email, fail_silently=False)
                if request.user.is_authenticated():
                    messages.success(request, "Your email have been sent. You may send to another friend if you want.", fail_silently=True)
                form = EmailForm()
                 
                #if 'posts_email' in request.session:
                    #del request.session['posts_email']
        #form = EmailForm()  
        posts = request.session.get('posts_email',[])      
        template_data = {
            #'entries': entries,
            'posts': posts,
            'form': form,
        }        
        return render_to_response('email.html', template_data, context_instance=RequestContext(request))    
    
    
@login_required    
def favorites(request):
    user = request.user 
    if request.method == 'POST':
        posts = []
        entries = request.POST.getlist('entries',[])
        for entry in entries:
            posts.append(get_object_or_404(Entry, slug=entry))
        for post in posts:
            if not user in post.favorited_by.all():
                post.favorited_by.add(user)
                post.favorites = post.favorites + 1
                post.save()
    
    posts = user.favorited.order_by('last_score')   
    template_data = {
        'posts': posts,
        #'form': form,
    }        
    return render_to_response('favorites.html', template_data, context_instance=RequestContext(request))

def splash(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			if InterestEmail.objects.filter(email__iexact = email):
				form = SignUpForm()
				template_data = {
					'form': form,
					'failed': True,
					'reason': 'exists',
					'email': email
				}
				return render_to_response('splash.html', template_data, context_instance=RequestContext(request))
			else:
				new = InterestEmail()
				new.email = email
				new.save()
				template_data = {
					'email': email
				}
				return render_to_response('splash_thanks.html', template_data, context_instance=RequestContext(request))
		else:
			email = request.POST.get('email','')
			form = SignUpForm()
			template_data = {
				'form': form,
				'failed': True,
				'reason': 'invalid',
				'email': email
			}
			return render_to_response('splash.html', template_data, context_instance=RequestContext(request))
	else:
		form = SignUpForm()
		template_data = {
			'form': form,
			'failed': False
		}
		return render_to_response('splash.html', template_data, context_instance=RequestContext(request))


def graphtest(request,method='votes'):
    tags = Tag.objects.all()
    tagnames = [ str(t.name) for t in tags ]
    entries = Entry.objects.all()
    edges=[]
    tagscores = dict()
    for tag in tagnames:
        tagscores[tag] = 0
    if method in ('votes','decay1','decay2','decay3','decay4','decay5','decay6','decay7','decay8'):
        for entry in entries:
            etags = entry.tags.all()
            for i, tag1 in enumerate(etags):
                rank1 = entry._get_ranking(tag1, method)
                tagscores[tag1.name] += rank1
                for tag2 in etags[i+1:]:
                    edges.append([tag1.name,tag2.name,rank1+entry._get_ranking(tag2,method)])
    else:
        return render_to_response('404.html')
    
    edges2=[]
    for e in edges:
        edges2.append([tagnames.index(e[0]),tagnames.index(e[1]),e[2]])
    n = len(tags)
    points= [ [200+100*cos(2*pi*i/n),200+100*sin(2*pi*i/n),tagnames[i],tagscores[tagnames[i]]] for i in range(n) ]
            
    template_data = {
        'points': points,
        'edges': edges2,
        'method': method,
    }
    return render_to_response('graphtest.html', template_data)


def listsum(ls): #used in relevanttags below in tagslist() to append lists to eachother
    temp = []
    for seg in ls:
        temp.extend(seg)
    return temp
def nthslice(ls,n,l): #returns the nth slice of ls of length l (n starting with 1)
	return ls[(n-1)*l:n*l]
site_re = re_compile(r'^site:')
def taglist(request, tags='', method='decay3', domain='', page=1,
          signup_form=SignupForm, auth_form=AuthenticationForm):
    
    signupform = signup_form()
    signinform = auth_form()
    user = request.user
    tags = tags
    
    if tags == '':
        taglist = [ tag.name for tag in Tag.objects.all() ]
    else:
        taglist = [ tag for tag in tags.split('+') if not site_re.match(tag) ]
        domainlist = [ tag for tag in tags.split('+') if site_re.match(tag) ]
        tags = '+'.join(taglist)
        taglist = taglist or [ tag.name for tag in Tag.objects.all() ] # if removing all r'^site:' elements has left the list empty, then we want to look at all tags
        domain = domainlist[0][5:] if domainlist else ''
    
    if user.is_authenticated():
        voted = user.voter_set.filter(tag__in=[taglist[0]]) #only dealing with votes on the primary tag
        voter = [ i.slug for i in voted.filter(val__exact=1) ]
        double_voter = [ i.slug for i in voted.filter(val__exact=2) ]

        if request.method == 'POST':
            action = request.POST.get('action', '')
            if action == 'addfavtag':
                favtags = request.POST.get('tags','')
                if user.favoritetag_set.filter(tags=favtags):
                    pass
                else:
                    if favtags == '':
                        user.favoritetag_set.create(tags=favtags,name='All Tags')
                    else:
                        user.favoritetag_set.create(tags=favtags,name=' + '.join(favtags.split('+')))
                        
            elif action == 'delete_mytag':
                mytag = request.POST.get('mytag_x','')
                if user.favoritetag_set.filter(tags=mytag):
                    user.favoritetag_set.get(tags=mytag).delete()
                else:
                    pass
                
            elif action == 'signup':
                signupform = signup_form(request.POST, request.FILES)
                if signupform.is_valid():
                    user = signupform.save()

                    # Send the signup complete signal
                    userena_signals.signup_complete.send(sender=None, user=user)
            elif action == 'signout':
                logout(request)
                    
            else:
                post_slug = request.POST.get('post_slug', '')
                if post_slug not in voter and post_slug not in double_voter:
                    post_change = get_object_or_404(Entry, slug=post_slug)
                    tagnew = Tag.objects.get(name=taglist[0]) if tags else sorted(post_change.tags.all(), key=lambda t: -post_change._get_ranking(t))[0]
                    activetags = eval(DataList.objects.get(id=1).data)
                    if tagnew.id not in activetags: #make tag active so that ranktags knows to look at it
                        activetags.append(tagnew.id)
                        d = DataList.objects.get(id=1)
                        d.data = activetags
                        d.save()
                        del d
                    if action == 'vote':
                        voter.append(post_slug)
                        post_change.voted_by.voter_set.create(tag=tagnew, user=user, val=1, slug=post_slug)
                        try:
                            p=post_change.posts.tagval_set.get(tag=tagnew)
                            p.val += 1
                            p.save()
                        except:
                            post_change.posts.tagval_set.create(tag=tagnew,val=1)
                        tval1=post_change.decayed_score_1.tagval_set.get(tag=tagnew)
                        tval1.val += 1
                        tval1.save()
                        tval2=post_change.decayed_score_2.tagval_set.get(tag=tagnew)
                        tval2.val += 1
                        tval2.save()
                        tval3=post_change.decayed_score_3.tagval_set.get(tag=tagnew)
                        tval3.val += 1
                        tval3.save()
                        tval4=post_change.decayed_score_4.tagval_set.get(tag=tagnew)
                        tval4.val += 1
                        tval4.save()
                        tval5=post_change.decayed_score_5.tagval_set.get(tag=tagnew)
                        tval5.val += 1
                        tval5.save()
                        tval6=post_change.decayed_score_6.tagval_set.get(tag=tagnew)
                        tval6.val += 1
                        tval6.save()
                        tval7=post_change.decayed_score_7.tagval_set.get(tag=tagnew)
                        tval7.val += 1
                        tval7.save()
                        tval8=post_change.decayed_score_8.tagval_set.get(tag=tagnew)
                        tval8.val += 1
                        tval8.save()

                    if action == 'double_vote':
                        double_voter.append(post_slug)
                        post_change.voted_by.voter_set.create(tag=taglist[0], user=user, val=2, slug=post_slug)
                        try:
                            dbp=post_change.double_posts.tagval_set.get(tag=tagnew)
                            dbp.val += 1
                            dbp.save()
                        except:
                            post_change.double_posts.tagval_set.create(tag=tagnew,val=1)
                        tval1=post_change.decayed_score_1.tagval_set.get(tag=tagnew)
                        tval1.val += 2
                        tval1.save()
                        tval2=post_change.decayed_score_2.tagval_set.get(tag=tagnew)
                        tval2.val += 2
                        tval2.save()
                        tval3=post_change.decayed_score_3.tagval_set.get(tag=tagnew)
                        tval3.val += 2
                        tval3.save()
                        tval4=post_change.decayed_score_4.tagval_set.get(tag=tagnew)
                        tval4.val += 2
                        tval4.save()
                        tval5=post_change.decayed_score_5.tagval_set.get(tag=tagnew)
                        tval5.val += 2
                        tval5.save()
                        tval6=post_change.decayed_score_6.tagval_set.get(tag=tagnew)
                        tval6.val += 2
                        tval6.save()
                        tval7=post_change.decayed_score_7.tagval_set.get(tag=tagnew)
                        tval7.val += 2
                        tval7.save()
                        tval8=post_change.decayed_score_8.tagval_set.get(tag=tagnew)
                        tval8.val += 2
                        tval8.save()


        entries = Entry.objects.all()
        if tags:
            for tag in taglist:
                entries = entries.filter(tags__name__in=[tag])
        if domain:
            entries = entries.filter(domain__iexact=domain)
	
        if method == 'votes':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=2).data),page,8) ]
                votecounts = [ entry.score for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [sum([ a._get_ranking(tag) for tag in taglist]) for a in posts]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag) for tag in taglist]))
                votecounts = [sum([ a._get_ranking(tag) for tag in taglist]) for a in posts]
        elif method == 'growth':
            posts = entries.order_by('-last_growth', '-date_added')
            votecounts = [ a.last_growth for a in posts ]
        elif method == 'decay1':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=3).data),page,8) ]
                votecounts = [ entry.score_d1 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d1_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay1') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay1') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay1') for tag in taglist]),1) for a in posts ]
        elif method == 'decay2':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=4).data),page,8) ]
                votecounts = [ entry.score_d2 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d2_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay2') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay2') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay2') for tag in taglist]),1) for a in posts ]
        elif method == 'decay3':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=5).data),page,8) ]
                votecounts = [ entry.score_d3 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d3_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay3') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay3') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay3') for tag in taglist]),1) for a in posts ]
        elif method == 'decay4':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=6).data),page,8) ]
                votecounts = [ entry.score_d4 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d4_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay4') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay4') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay4') for tag in taglist]),1) for a in posts ]
        elif method == 'decay5':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=7).data),page,8) ]
                votecounts = [ entry.score_d5 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d5_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay5') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay5') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay5') for tag in taglist]),1) for a in posts ]
        elif method == 'decay6':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=8).data),page,8) ]
                votecounts = [ entry.score_d6 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d6_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay6') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay6') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay6') for tag in taglist]),1) for a in posts ]
        elif method == 'decay7':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=9).data),page,8) ]
                votecounts = [ entry.score_d7 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d7_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay7') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay7') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay7') for tag in taglist]),1) for a in posts ]
        elif method == 'decay8':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=10).data),page,8) ]
                votecounts = [ entry.score_d8 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d8_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay8') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay8') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay8') for tag in taglist]),1) for a in posts ]
        elif method == 'favorites':
            posts = entries.filter(favorites__gt=0).order_by('-favorites', '-date_added')
        elif method == 'green':
            posts = sorted(entries.filter(date_added__range=(datetime.now() - timedelta(days=1), datetime.now())), key=lambda a: -a._get_ranking(taglist[0]))
        elif method == 'orange':
            posts = sorted(entries.filter(date_added__range=(datetime.now() - timedelta(days=3), datetime.now() - timedelta(days=1))), key=lambda a: -a._get_ranking(taglist[0]))
        elif method == 'red':
            posts = sorted(entries.filter(date_added__range=(datetime.now() - timedelta(days=6), datetime.now() - timedelta(days=3))), key=lambda a: -a._get_ranking(taglist[0]))
        elif method == 'black':
            posts = sorted(entries.filter(date_added__range=(datetime.now() - timedelta(days=365), datetime.now() - timedelta(days=6))), key=lambda a: -a._get_ranking(taglist[0]))
        else:
            return render_to_response('404.html')

        tagscores = [ sorted([ [tag.name, round(post._get_ranking(tag, method),1)] for tag in post.tags.all()], key=lambda a: -a[1]) for post in posts]
        if tags != '':
            relevanttags = listsum([ post.tags.all() for post in posts ])
            toprelevant = sorted([[tag.name,int(sum([a._get_ranking(tag, method) for a in posts]))] for tag in set(relevanttags)], key=lambda a: -a[1])[:10]
        else:
            toprelevant = []
        
        if method=='votes':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=193).tagval_set.all()], key=lambda a: -a[1])
            topsites = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=1463).tagval_set.all()], key=lambda a: -a[1])
        elif method=='decay1':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=194).tagval_set.all()], key=lambda a: -a[1])
            topsites = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=1464).tagval_set.all()], key=lambda a: -a[1])
        elif method=='decay2':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=195).tagval_set.all()], key=lambda a: -a[1])
            topsites = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=1465).tagval_set.all()], key=lambda a: -a[1])
        elif method=='decay3':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=196).tagval_set.all()], key=lambda a: -a[1])
            topsites = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=1466).tagval_set.all()], key=lambda a: -a[1])
        elif method=='decay4':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=197).tagval_set.all()], key=lambda a: -a[1])
            topsites = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=1467).tagval_set.all()], key=lambda a: -a[1])
        elif method=='decay5':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=198).tagval_set.all()], key=lambda a: -a[1])
            topsites = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=1468).tagval_set.all()], key=lambda a: -a[1])
        elif method=='decay6':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=199).tagval_set.all()], key=lambda a: -a[1])
            topsites = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=1469).tagval_set.all()], key=lambda a: -a[1])
        elif method=='decay7':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=200).tagval_set.all()], key=lambda a: -a[1])
            topsites = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=1470).tagval_set.all()], key=lambda a: -a[1])
        elif method=='decay8':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=201).tagval_set.all()], key=lambda a: -a[1])
            topsites = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=1471).tagval_set.all()], key=lambda a: -a[1])
        mytags = zip([ favtag.tags for favtag in user.favoritetag_set.all() ],[ favtag.name for favtag in user.favoritetag_set.all() ])
        if not tags and not domain: #show 'all' instead of a list of every single tag
            taglist=['all']
        if domain:
            if tags:
                taglist += ['site:'+domain]
            else:
                taglist = ['site:'+domain]
        
        template_data = {
            'tags': tags,
            'postdata': zip(posts,votecounts,tagscores),
            'voter': voter,
            'double_voter': double_voter,
            'method': method,
            'taglist': taglist,
            'topsites': topsites,
            'toptags_1': nthslice(toptags,1,10),
            'toptags_2': nthslice(toptags,2,10),
            'toprelevant': toprelevant,
            'mytags': mytags,
            'domain': domain,
            'breadcrumbdata': zip(taglist,['+'.join(taglist[:i]+taglist[i+1:]) for i in range(0,len(taglist))]),
            'signupform': signupform,
            'signinform': dict(), #no reason to have a sign in form if the user is authenticated
            }
    else:
        if request.method == 'POST':
            action = request.POST.get('action', '')
            if action == 'signup':
                signupform = signup_form(request.POST, request.FILES)
                if signupform.is_valid():
                    user = signupform.save()

                    # Send the signup complete signal
                    userena_signals.signup_complete.send(sender=None, user=user)

                    #sign in
                    user = authenticate(identification=request.POST.get('username', ''), password=request.POST.get('password1', ''))
                    login(request, user)
                    
            elif action == 'signin':
                signinform = auth_form(request.POST, request.FILES)
                if signinform.is_valid():
                    identification, password, remember_me = (signinform.cleaned_data['identification'],
                                                             signinform.cleaned_data['password'],
                                                             signinform.cleaned_data['remember_me'])
                    user = authenticate(identification=identification,
                                        password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            if remember_me:
                                request.session.set_expiry(userena_settings.USERENA_REMEMBER_ME_DAYS[1] * 86400)
                            else: request.session.set_expiry(0)
                        else:
                            return redirect(reverse('userena_disabled',
                                                kwargs={'username': user.username}))
                    
        entries = Entry.objects.all()
        if tags:
            for tag in taglist:
                entries = entries.filter(tags__name__in=[tag])
        if domain:
            entries = entries.filter(domain__iexact=domain)
	
        if method == 'votes':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=2).data),page,8) ]
                votecounts = [ entry.score for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [sum([ a._get_ranking(tag) for tag in taglist]) for a in posts]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag) for tag in taglist]))
                votecounts = [sum([ a._get_ranking(tag) for tag in taglist]) for a in posts]
        elif method == 'growth':
            posts = entries.order_by('-last_growth', '-date_added')
            votecounts = [ a.last_growth for a in posts ]
        elif method == 'decay1':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=3).data),page,8) ]
                votecounts = [ entry.score_d1 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d1_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay1') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay1') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay1') for tag in taglist]),1) for a in posts ]
        elif method == 'decay2':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=4).data),page,8) ]
                votecounts = [ entry.score_d2 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d2_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay2') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay2') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay2') for tag in taglist]),1) for a in posts ]
        elif method == 'decay3':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=5).data),page,8) ]
                votecounts = [ entry.score_d3 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d3_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay3') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay3') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay3') for tag in taglist]),1) for a in posts ]
        elif method == 'decay4':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=6).data),page,8) ]
                votecounts = [ entry.score_d4 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d4_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay4') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay4') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay4') for tag in taglist]),1) for a in posts ]
        elif method == 'decay5':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=7).data),page,8) ]
                votecounts = [ entry.score_d5 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d5_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay5') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay5') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay5') for tag in taglist]),1) for a in posts ]
        elif method == 'decay6':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=8).data),page,8) ]
                votecounts = [ entry.score_d6 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d6_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay6') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay6') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay6') for tag in taglist]),1) for a in posts ]
        elif method == 'decay7':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=9).data),page,8) ]
                votecounts = [ entry.score_d7 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d7_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay7') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay7') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay7') for tag in taglist]),1) for a in posts ]
        elif method == 'decay8':
            if not tags and not domain:
                posts = [ Entry.objects.get(id=id) for id in nthslice(eval(DataList.objects.get(id=10).data),page,8) ]
                votecounts = [ entry.score_d8 for entry in posts ]
            elif len(taglist)==1 and not domain:
                try:
                    posts = [ Entry.objects.get(id=id) for id in eval(DataList.objects.get(name='top_d8_'+taglist[0]).data) ]
                except:
                    posts = []
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay8') for tag in taglist]),1) for a in posts ]
            else:
                posts = sorted(entries, key=lambda a: -sum([ a._get_ranking(tag, 'decay8') for tag in taglist]))
                votecounts = [ round(sum([ a._get_ranking(tag, 'decay8') for tag in taglist]),1) for a in posts ]
        elif method == 'favorites':
            posts = entries.filter(favorites__gt=0).order_by('-favorites', '-date_added')
        elif method == 'green':
            posts = sorted(entries.filter(date_added__range=(datetime.now() - timedelta(days=1), datetime.now())), key=lambda a: -a._get_ranking(taglist[0]))
        elif method == 'orange':
            posts = sorted(entries.filter(date_added__range=(datetime.now() - timedelta(days=3), datetime.now() - timedelta(days=1))), key=lambda a: -a._get_ranking(taglist[0]))
        elif method == 'red':
            posts = sorted(entries.filter(date_added__range=(datetime.now() - timedelta(days=6), datetime.now() - timedelta(days=3))), key=lambda a: -a._get_ranking(taglist[0]))
        elif method == 'black':
            posts = sorted(entries.filter(date_added__range=(datetime.now() - timedelta(days=365), datetime.now() - timedelta(days=6))), key=lambda a: -a._get_ranking(taglist[0]))
        else:
            return render_to_response('404.html')
        
        tagscores = [ sorted([ [tag.name, post._get_ranking(tag)] for tag in post.tags.all()], key=lambda a: -a[1]) for post in posts]
        if tags:
            relevanttags = listsum([ post.tags.all() for post in posts ])
            toprelevant = sorted([[tag.name,int(sum([a._get_ranking(tag, method) for a in posts]))] for tag in set(relevanttags)], key=lambda a: -a[1])[:10]
        else:
            toprelevant = []
        
        if method=='votes':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=193).tagval_set.all()], key=lambda a: -a[1])[:10]
        elif method=='decay1':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=194).tagval_set.all()], key=lambda a: -a[1])[:10]
        elif method=='decay2':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=195).tagval_set.all()], key=lambda a: -a[1])[:10]
        elif method=='decay3':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=196).tagval_set.all()], key=lambda a: -a[1])[:10]
        elif method=='decay4':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=197).tagval_set.all()], key=lambda a: -a[1])[:10]
        elif method=='decay5':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=198).tagval_set.all()], key=lambda a: -a[1])[:10]
        elif method=='decay6':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=199).tagval_set.all()], key=lambda a: -a[1])[:10]
        elif method=='decay7':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=200).tagval_set.all()], key=lambda a: -a[1])[:10]
        elif method=='decay8':
            toptags = sorted([ [a.tag, a.val] for a in Dict.objects.get(id=201).tagval_set.all()], key=lambda a: -a[1])[:10]
        if not tags and not domain: #show 'all' instead of a list of every single tag
            taglist=['all']
        if domain:
            if tags:
                taglist += ['site:'+domain]
            else:
                taglist = ['site:'+domain]
        
        template_data = {
            'tags': tags,
            'postdata': zip(posts,votecounts,tagscores),
            'method': method,
            'voter': [],
            'double_voter': [],
            'taglist': taglist,
            'toptags': toptags,
            'toprelevant': toprelevant,
            'mytags': [],
            'domain': domain,
            'breadcrumbdata': zip(taglist,['+'.join(taglist[:i]+taglist[i+1:]) for i in range(0,len(taglist))]),
            'signupform': signupform,
            'signinform': signinform,
            }
    return render_to_response('brian.html', template_data, context_instance=RequestContext(request))

    
    
        
