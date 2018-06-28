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
        p = domain_to_server.objects.all()
        return render_to_response('opssearchdomain.html', locals())
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
        if request.POST['operate'] == 'git_pull':
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.git_pull(str(info.Path)))
            return HttpResponse(info)

        elif request.POST['operate'] == 'git_reset_hard':
            git_reset_hard_value = request.POST['hard_code']
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.git_reset_hard(str(info.Path), git_reset_hard_value))
            return HttpResponse(info)

        elif request.POST['operate'] == 'php_artisan_option':
            php_artisan_option_value = request.POST['artisan_code']
            allow_list = ["cache:clear"]
            if php_artisan_option_value in allow_list:
                connect = ssh(str(info.Adderss))
                info = json.dumps(connect.php_artisan_option(str(info.Path), php_artisan_option_value))
                return HttpResponse(info)
            else:
                info = json.dumps("the option is disabled")
                return HttpResponse(info)

        elif request.POST['operate'] == 'npm_dev_option':
            npm_dev_option_value = request.POST['npm_code']
            allow_list = ["dev", "production"]
            if npm_dev_option_value in allow_list:
                connect = ssh(str(info.Adderss))
                info = json.dumps(connect.npm_dev_option(str(info.Path), npm_dev_option_value))
                return HttpResponse(info)
            else:
                info = json.dumps("the option is disabled")
                return HttpResponse(info)

        elif request.POST['operate'] == 'deamon_process_restart':
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.deamon_process_restart())
            return HttpResponse(info)