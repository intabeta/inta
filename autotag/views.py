from autotag.keywords import getkeywords
from django.shortcuts import render_to_response
from django.template import RequestContext

def autotag(request):
    "Demo autotag functionality"

    user = request.user
    
    if request.method == 'POST':
        url = request.POST.get('url','')
        n = request.POST.get('num','3')
        keywords = getkeywords(url, int(n))

        template_data = {'keywords':str(keywords)}
        return render_to_response('autotag.html', template_data, context_instance=RequestContext(request))
    else:
        template_data = {'keywords':'none'}
        return render_to_response('autotag.html', template_data, context_instance=RequestContext(request))
