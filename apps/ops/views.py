from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

from models import *


@csrf_exempt
def ops_search_domain(request):
    if request.method == 'GET':
        return render_to_response('opssearchdomain.html')
    else:
        domain = request.POST['domain']
        p = domain_to_server.objects.filter(Domain__icontains=domain)
        return render_to_response('opssearchdomain.html', locals())
