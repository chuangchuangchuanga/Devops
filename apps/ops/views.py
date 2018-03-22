import sys, os
import json
import re

from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from models import *
from tools import ssh


# Create your views here.
@login_required
@csrf_exempt
def ops_search_domain(request):
    if request.method == 'GET':
        return render_to_response('opssearchdomain.html')
    else:
        domain = request.POST['domain']
        p = domain_to_server.objects.filter(Domain__icontains=domain)
        return render_to_response('opssearchdomain.html', locals())


@login_required
@csrf_exempt
def ops_operate(request, id):
    info = domain_to_server.objects.get(id=id)
    if request.method == 'GET':
        return render_to_response('opsoperate.html', locals())
    if request.method == 'POST':
        if request.POST['operate'] == 'git':
            command = request.POST['command']
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.tools_git(str(info.Path), command))
            return HttpResponse(info)
        elif request.POST['operate'] == 'deamon':
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.tools_deamon())
            return HttpResponse(info)
        elif request.POST['operate'] == 'php_artisan':
            command = request.POST['command']
            if re.search('rollback', command) is None:
                connect = ssh(str(info.Adderss))
                info = json.dumps(connect.tools_php_artisan(str(info.Path), command))
                return HttpResponse(info)
            else:
                warn = json.dumps("the option is disabled")
                return HttpResponse(warn)