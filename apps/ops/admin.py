from django.contrib import admin


from .models import domain_to_server, test_domain_to_server
# Register your models here.

admin.site.register(test_domain_to_server)
admin.site.register(domain_to_server)