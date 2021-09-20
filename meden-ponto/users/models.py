from django.db import models
from django.urls import reverse
from django.shortcuts import render, redirect

# Create your models here.
class Permitidos(models.Model):
  email=models.EmailField(unique=True, max_length=254)
  estagiario=models.BooleanField(default=False)

  def get_absolute_url(self):
      return reverse("users:detalhe", kwargs={"pk": self.pk})

  def __str__(self):
      if self.estagiario:
          return f'{self.email} [Estagiário]'
      else:
          return f'{self.email}' 

  class Meta:
      verbose_name_plural = 'Permitidos'
      
      