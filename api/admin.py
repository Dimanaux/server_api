from django.contrib import admin

from .models import Game
from .models import Record,Company,Profile

# Register your models here.
admin.site.register(Game)
admin.site.register(Record)
admin.site.register(Company)
admin.site.register(Profile)


