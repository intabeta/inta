from autotag.keywords import getkeywords

def autotag(request):
    "Demo autotag functionality"

    user = request.user
    
    if request.method == 'POST':
        url = request.POST.get('url','')
        keywords = getkeywords(url)

        template_data = {'keywords':str(keywords)}
        return render_to_response('autotag.html', template_data)
    else:
        template_data = {'keywords':'none'}
        return render_to_response('autotag.html', template_data)
