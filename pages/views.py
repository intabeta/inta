from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from content.models import InterestGroup, IgProposal, IgProposalForm, Entry
from taggit.models import Tag
from haystack.query import SearchQuerySet
from content.views import get_referer_view
from content.models import InterestEmail
from content.forms import EmailForm, SignUpForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
	
def brian(request):
	form = SignUpForm()
        toptags = sorted([[tag.name,sum([a._get_ranking(tag) for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])[:10] #get top ten tags by number of votes over all entries
        toprelevant = sorted([[tag.name,sum([a._get_ranking(tag) for a in Entry.objects.all()])] for tag in Tag.objects.all()], key=lambda a: -a[1])[:10] #get top ten tags by number of votes over all entries
        mytags = [ favtag.tags for favtag in user.favoritetag_set.all() ]
	template_data = {
		'form': form,
                'toprelevant': toprelevant,
                'toptags': toptags,
                'mytags': mytags,
	}
	return render_to_response('brian.html', template_data, context_instance=RequestContext(request))

    
    
        
