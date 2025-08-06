from django.contrib import admin
from AttandanceData.models import AttandanceData
# Register your models here.

class AttandanceInfo(admin.ModelAdmin):
    list_display = ('lecture','faculty','lecture_notes','file','enrollment','timestamp')

admin.site.register(AttandanceData,AttandanceInfo)