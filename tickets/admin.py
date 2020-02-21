from django.contrib import admin
from .models import Ticket, Comment
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(Ticket, SimpleHistoryAdmin)
admin.site.register(Comment)
