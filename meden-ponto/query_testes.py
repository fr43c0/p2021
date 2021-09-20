from ponto.models import Periodo
from django.utils import timezone
while len(p) >1:
    #from django.utils import timezone
    data=data+datetime.timedelta(1)
    #from django.utils import timezone
    p2=p.filter(entrada__lt=data)
    #from django.utils import timezone
    p=p.exclude(entrada__lt=data)
    if p2.exists():
        data2=data+datetime.timedelta(-1)
        data2=str(data2)
        d[data2]=p2
print(d)
