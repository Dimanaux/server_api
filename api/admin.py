from django.contrib import admin

from .models import Game
from .models import Record

# Register your models here.
admin.register(Game)
admin.register(Record)
