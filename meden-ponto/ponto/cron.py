from ponto.models import Obs



def derruba():
    obs=Obs.objects.create(colaborador='franco',observacoes='fake')
    obs.save()
derruba()