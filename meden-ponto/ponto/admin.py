from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from . models import Periodo,Entraram,Obs
from django.contrib.auth.models import Group
# Register your models here.


admin.site.unregister(Group)

class PeriodoAdmin(admin.ModelAdmin):
    list_display=('colaborador','entrada','saida','jornada','observacoes')
    list_filter=("colaborador","entrada","observacoes")
admin.site.register(Periodo,PeriodoAdmin)
admin.site.register(Entraram)
admin.site.register(Obs)