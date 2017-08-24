from django.shortcuts import render
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import requests
import re


# Create your views here.
from .models import *


@login_required
@csrf_exempt
def searchdomain(requests):
    if requests.method == 'GET':
        return render_to_response('searchdomain.html')
    else:
        domain = requests.POST['domain']
        p = cloudflareinfo.objects.filter(domain__icontains=domain)
        return render_to_response('searchdomain.html', locals())


@login_required
@csrf_exempt
def cleancache(requests, id):
    info = cloudflareinfo.objects.get(id=id)
    if requests.method == 'GET':
        id = id
        return render_to_response('cleancache.html', locals())
    else:
        url = requests.POST['url']
        zone, auth_email, auth_key = info.zone_id, str(info.auth_email), str(info.auth_key)
        cleaninfo = clean(url, zone, auth_email, auth_key)
        return render_to_response('cleancache.html', locals())


def clean(url, zone, auth_email, autho_key):
    api_url = "https://api.cloudflare.com/client/v4/zones/%s/purge_cache" %zone
    headers = {'X-Auth-Email': '%s' %auth_email, 'X-Auth-Key': '%s' %autho_key, 'Content-Type': 'application/json'}
    data = '{"files":["%s"]}'% url

    r = requests.delete(api_url, headers = headers, data = data)
    return r.text