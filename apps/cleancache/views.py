from django.shortcuts import render
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
import requests


# Create your views here.
from .models import *


@csrf_exempt
def searchdomain(requests):
    if requests.method == 'GET':
        return render_to_response('searchdomain.html')
    else:
        domain = requests.POST['domain']
        p = cloudflareinfo.objects.filter(domain__icontains=domain)
        return render_to_response('searchdomain.html', locals())


@csrf_exempt
def cleancache(requests, id):
    if requests.method == 'GET':
        return render_to_response('cleancache.html')
    else:
        info = cloudflareinfo.objects.get(id=id)
        url = requests.POST = ['url']
        zone, auth_email, auth_key = info.zone_id, info.auth_email, info.auth_key
        cleaninfo = clean(url, zone, auth_email, auth_key)
        return render_to_response('cleancache.html', locals())


def clean(url, zone, auth_email, autho_key):
    api_url = "https://api.cloudflare.com/client/v4/zones/%s/purge_cache" %zone
    headers = {'X-Auth-Email': auth_email, 'X-Auth-Key': autho_key, 'Content-Type': 'application/json'}
    data = '{"files":[%s]}'% url
    r = requests.delete(api_url, headers = headers, data = data)
    return r.text