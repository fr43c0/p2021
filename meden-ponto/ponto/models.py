from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from  datetime import timedelta
import pytz




class Entraram(models.Model):
    entrada     = models.DateTimeField(blank=True, null=True)
    ip_address  = models.GenericIPAddressField(blank=True, null=True)
    colaborador = models.ForeignKey(User, on_delete=models.CASCADE,related_name='entrou')
    observacoes = models.CharField(default='',max_length=300,blank=True, null=True)
    display     = models.CharField(default='',max_length=10,blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Entraram'

    def __str__(self):
            return self.colaborador.username

class Obs(models.Model):
    colaborador = models.ForeignKey(User, on_delete=models.CASCADE,related_name='observou')
    observacoes = models.CharField(default='',max_length=300,blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Obs'   
    
    def __str__(self):
            return self.observacoes

class Filtro(models.Model): 
    colaborador = models.ForeignKey(User, on_delete=models.CASCADE)
    campo= models.CharField(default='',max_length=20,blank=True, null=True)
    def __str__(self):
            return self.colaborador.username
            
class Periodo(models.Model):
    entrada         = models.DateTimeField(blank=True, null=True)
    saida           = models.DateTimeField(blank=True, null=True)
    jornada         = models.DecimalField(max_digits=10,decimal_places=3, blank=True, null=True)
    horas_totais    = models.DecimalField(default=0.0,max_digits=10,decimal_places=3, blank=True, null=True)
    ip_address      = models.GenericIPAddressField(blank=True, null=True)
    ip_saida        = models.GenericIPAddressField(blank=True, null=True)
    colaborador     = models.ForeignKey(User, on_delete=models.CASCADE,related_name='colab')
    data_inicio     = models.DateTimeField(blank=True, null=True)
    dias_corridos   = models.IntegerField(default=0,blank=True, null=True)
    dias_trabalhados= models.IntegerField(blank=True, null=True)
    media_dias_t    = models.DecimalField(max_digits=5,decimal_places=2, blank=True, null=True)
    media_h_d_c     = models.DecimalField(max_digits=5,decimal_places=2, blank=True, null=True)
    media_h_d_t     = models.DecimalField(max_digits=5,decimal_places=2, blank=True, null=True)
    observacoes     = models.CharField(default='',max_length=300,blank=True, null=True)
    desligado       = models.BooleanField(default=False)
    display         = models.CharField(default='',max_length=10,blank=True, null=True)
     
    def entra(self,t):
        # t=t.replace(tzinfo=pytz.utc)
        # tz=pytz.timezone('America/Sao_Paulo')
        # t=t.astimezone(tz)
        # t= timezone.localtime(t,tz)
        self.entrada=t
        self.save()

    def sai(self,t):
        # t=t.replace(tzinfo=pytz.utc)
        # tz=pytz.timezone('America/Sao_Paulo')
        # t=t.astimezone(tz)
        # t= timezone.localtime(t,tz)
        self.saida=t
        self.save()

    def get_h(self,h):
        self.jornada=h
        self.save()


    # def get_data_inicio(self,inicio):
    #         self.data_inicio=inicio
    #         self.save()
    
   
    
        
    def get_horas_totais(self):
        self.horas_totais=self.horas_totais+self.jornada
        self.save()

    def get_ip(self,ip):
        self.ip_address=ip
        self.save()
    

    def delisgar_colaborador(self):
        self.deligado=True
        self.save()
  
   

    def __str__(self):
        return self.colaborador.username

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})