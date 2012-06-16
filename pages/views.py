from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from content.models import InterestGroup, IgProposal, IgProposalForm, Entry




def homepage(request):
    hot = Entry.objects.all().order_by('-date_added', '-decayed_score')[:10]
    return render_to_response('homepage.html', {'hot': hot}, context_instance=RequestContext(request))
    
def autoclose(request):
    return render_to_response('autoclose.html', {}, context_instance=RequestContext(request))

def howto(request):
    return render_to_response('howto.html', {}, context_instance=RequestContext(request))

def mission(request):
    return render_to_response('mission.html', {}, context_instance=RequestContext(request))

def privacy(request):
    return render_to_response('privacy.html', {}, context_instance=RequestContext(request))