from ponto.models import Obs
from django.contrib.auth.models import User


def derruba():
    u=User.objects.all()[0]
    print(u)
    obs=Obs.objects.create(colaborador=u,observacoes='fake')
