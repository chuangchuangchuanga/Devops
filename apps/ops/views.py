import sys, os
import json

from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


from models import *
from tools import ssh


# Create your views here.
@csrf_exempt
def ops_search_domain(request):
    if request.method == 'GET':
        return render_to_response('opssearchdomain.html')
    else:
        domain = request.POST['domain']
        p = domain_to_server.objects.filter(Domain__icontains=domain)
        return render_to_response('opssearchdomain.html', locals())


@csrf_exempt
def ops_operate(request, id=None):
    info = domain_to_server.objects.get(id=id)
    if request.method == 'GET':
        return render_to_response('opsoperate.html', locals())
    if request.method == 'POST':
        if request.POST['operate'] == 'git':
            command = request.POST['command']
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.tools_git(str(info.Path), command))
            return HttpResponse(info)
        if request.POST['operate'] == 'deamon':
            command = request.POST['command']
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.tools_deamon())
            return HttpResponse(info)