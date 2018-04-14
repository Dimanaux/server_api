from django.contrib import admin

from .models import Game
from .models import Record

# Register your models here.
admin.site.register(Game)
admin.site.register(Record)
