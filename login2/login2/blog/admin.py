from django.contrib import admin
from .models import Anthology, Article
# Register your models here.

admin.site.register([Anthology, Article])