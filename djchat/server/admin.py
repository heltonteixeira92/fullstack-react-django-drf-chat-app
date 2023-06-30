from django.contrib import admin

from .models import Category, Channel, Server

admin.site.register([Channel, Server, Category])
