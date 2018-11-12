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
        return render_to_response('opssearchdomain.html', {'p': p, 'user': request.user})
    else:
        domain = request.POST['domain']
        p = domain_to_server.objects.filter(Domain__icontains=domain)
        return render_to_response('opssearchdomain.html', {'p': p, 'user': request.user})



@login_required
@csrf_exempt
def ops_operate(request, id):
    info = domain_to_server.objects.get(id=id)
    if request.method == 'GET':
        return render_to_response('opsoperate.html', {'info': info,  'user': request.user})
    if request.method == 'POST':
        if request.POST['operate'] == 'git_pull':
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.git_pull(str(info.Path)))
            if id == '2':
                connect.pl_queue_git_pull()
            return HttpResponse(info)

        elif request.POST['operate'] == 'git_reset_hard':
            git_reset_hard_value = request.POST['hard_code']
            denyList = ["rm", 'refresh', 'reset', 'rollback']
            for i in denyList:
                if re.search(i, git_reset_hard_value) is not None:
                    info = json.dumps("the option is disabled")
                    return HttpResponse(info)
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.git_reset_hard(str(info.Path), git_reset_hard_value))
            return HttpResponse(info)

        elif request.POST['operate'] == 'php_artisan_option':
            php_artisan_option_value = request.POST['artisan_code']
            denyList = ["rm", 'refresh', 'reset', 'rollback']
            for i in denyList:
                if re.search(i, php_artisan_option_value) is not None:
                    info = json.dumps("the option is disabled")
                    return HttpResponse(info)

            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.php_artisan_option(str(info.Path), php_artisan_option_value))
            return HttpResponse(info)


        elif request.POST['operate'] == 'npm_dev_option':
            npm_dev_option_value = request.POST['npm_code']
            denyList = ["rm", 'refresh', 'reset', 'rollback']
            for i in denyList:
                if re.search(i, npm_dev_option_value) is not None:
                    info = json.dumps("the option is disabled")
                    return HttpResponse(info)

            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.npm_dev_option(str(info.Path), npm_dev_option_value))
            return HttpResponse(info)


        elif request.POST['operate'] == 'deamon_process_restart':
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.deamon_process_restart())
            if id == '2':
                connect.pl_queue_deamon_process_restart()
            return HttpResponse(info)



@login_required
@csrf_exempt
def test_ops_search_domain(request):
    if request.method == 'GET':
        p = test_domain_to_server.objects.all()
        return render_to_response('testopssearchdomain.html', {'p': p, 'user': request.user})
    else:
        domain = request.POST['domain']
        p = test_domain_to_server.objects.filter(Domain__icontains=domain)
        return render_to_response('testopssearchdomain.html', {'p': p, 'user': request.user})


@login_required
@csrf_exempt
def test_ops_operate(request, id):
    info = test_domain_to_server.objects.get(id=id)
    if request.method == 'GET':
        return render_to_response('testopsoperate.html', {'info': info,  'user': request.user})
    if request.method == 'POST':
        if request.POST['operate'] == 'git_pull':
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.git_pull(str(info.Path)))
            return HttpResponse(info)

        elif request.POST['operate'] == 'git_reset_hard':
            git_reset_hard_value = request.POST['hard_code']
            denyList = ["rm", 'refresh', 'reset', 'rollback']
            for i in denyList:
                if re.search(i, git_reset_hard_value) is not None:
                    info = json.dumps("the option is disabled")
                    return HttpResponse(info)
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.git_reset_hard(str(info.Path), git_reset_hard_value))
            return HttpResponse(info)

        elif request.POST['operate'] == 'php_artisan_option':
            php_artisan_option_value = request.POST['artisan_code']
            denyList = ["rm", 'refresh', 'reset', 'rollback']
            for i in denyList:
                if re.search(i, php_artisan_option_value) is not None:
                    info = json.dumps("the option is disabled")
                    return HttpResponse(info)
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.php_artisan_option(str(info.Path), php_artisan_option_value))
            return HttpResponse(info)


        elif request.POST['operate'] == 'npm_dev_option':
            npm_dev_option_value = request.POST['npm_code']
            denyList = ["rm", 'refresh', 'reset', 'rollback']
            for i in denyList:
                if re.search(i, npm_dev_option_value) is not None:
                    info = json.dumps("the option is disabled")
                    return HttpResponse(info)


            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.npm_dev_option(str(info.Path), npm_dev_option_value))
            return HttpResponse(info)

        elif request.POST['operate'] == 'deamon_process_restart':
            connect = ssh(str(info.Adderss))
            info = json.dumps(connect.deamon_process_restart())
            return HttpResponse(info)