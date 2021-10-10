from django.db.models.expressions import F, OrderBy
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView 
from django.contrib.auth.models import User
from .models import Periodo,Entraram,Obs,Filtro
from users.models import Permitidos ######2021
from django.utils import timezone
from django.contrib.auth.decorators import login_required 
import pytz
tz=pytz.timezone('America/Sao_Paulo')
u=User.objects.all()
e=Entraram.objects.all()

#GET CLIENT IP ADDRESS:
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#usuarios que ja tem periodo registrado no bd
def usuarios_q_ja_iniciaram():
    Usuarios=[]
    l=[]
    p=Periodo.objects.all()
    U=Periodo.objects.all().values("colaborador__username").distinct() 
    Usuarios=[p.filter(colaborador__username=usu['colaborador__username']).last()  for usu in U]
    return Usuarios

#CRIA UMA VARIAVEL DA INSTANCIA DE CADA MODEL - COM NOME DO USUARIO - E NADA MAIS POREM NAO SALVA ESSA INSTANCIA...
def q_set_var(usuario): 
    p=Periodo(colaborador=usuario)
    ep=Entraram(colaborador=usuario)
    op=Obs(colaborador=usuario)
    return p,ep,op

#a partir de uma request retorna a observaçao o usuario 
def get_usuario_e_obs(request): 
    botao='' 
    r=request.POST
    if 'obs' in r:
        obs=r['obs_text']
    else:
        obs=''
    i=request.user
    if  i.username in r.keys():
        botao=r[i.username]
    return i,obs,botao

def get_context():
    e=Entraram.objects.all().order_by('entrada')
    lista_dos_que_entraram=[u.colaborador for u in e]
    return lista_dos_que_entraram

# ESTA HAVENDO UM ERRO NO DIAS CORRIDOS QUANDO ENTRA NO MESMO DIA DA DIVISAO POR ZERO
def get_dias_corridos(inicio):
        hoje=timezone.now()
        delta=hoje-inicio
        if hoje.date()==inicio.date():
            dias_corridos=1  
        
        else:
            dias=delta.days
            dias_corridos=dias
        if dias_corridos == 0:#<<<<<<<<<<<<<<<<<<<<<<Fiz esse bacalhau pra concertar o erro
            dias_corridos=1 # talvez seja o caso em que nao chega a dar 24h portanto nao tem 1 dia  
        return dias_corridos

def get_dias_trabalhados(x):
    p=Periodo.objects.filter(colaborador=x)
    l=[]
    for i in p:
        d=i.entrada.date()
        if d not in l:
            l.append(d)
    dias_trabalhados=len(l)
    if dias_trabalhados==0:
        dias_trabalhados=1
    return dias_trabalhados

def get_horas_totais(x):
    p=Periodo.objects.filter(colaborador=x)
    total=0
    for i in p:
        j=i.jornada
        total=total+j
    return total

def filtros(request):
    p=Periodo.objects.all().order_by('entrada')
    context={}
    context['p']=p
    context['A']=Periodo.objects.all().values('entrada__year').distinct()
    context['l']=usuarios_q_ja_iniciaram()
    if request.method == 'POST':
            r=request.POST
            #cria um queryset vazio do model Periodos
            Q=Periodo.objects.none()
            anos,meses,usuarios=[],[],usuarios_q_ja_iniciaram()
            #caso usuarios tenham sido selecionados
            if "usuario" in r.keys():
                usuarios=r.getlist('usuario')
                context['usuarios']=usuarios      
                if "ano" in r.keys():
                    if "mes" in r.keys() :
                        anos,meses=r.getlist('ano'),r.getlist('mes')
                        X=p.filter(colaborador__username__in=usuarios).filter(entrada__year__in=anos).filter(entrada__month__in=meses)
                    else :
                        anos=r.getlist('ano')
                        X=p.filter(colaborador__username__in=usuarios).filter(entrada__year__in=anos)
                else:
                    if "mes" in r.keys():
                        meses=r.getlist('mes')
                        X=p.filter(colaborador__username__in=usuarios).filter(entrada__month__in=meses)
                    else:
                        X=p.filter(colaborador__username__in=usuarios)              
            #caso usuarios nao tenham sido selecionados
            else:
                if "ano" in r.keys():
                    if "mes" in r.keys() :
                        anos,meses=r.getlist('ano'),r.getlist('mes')
                        X=p.filter(entrada__year__in=anos).filter(entrada__month__in=meses)
                    else:
                        anos=r.getlist('ano')
                        X=p.filter(entrada__year__in=anos)                  
                else:
                    if "mes" in r.keys():
                        meses=r.getlist('mes')
                        X=p.filter(entrada__month__in=meses)
                    else:
                        X=p
                #todos os casos acima retornam um queryset == X, caso nada tenha sido escolhido X=p              
            
            #Havendo algum tipo de filtro que reduza a queryset p:
            if X!=p:
                for u in usuarios:
                    XU=X.filter(colaborador__username=u)
                    if XU.count()>0:
                        for i in XU:
                            #Q|= append os objetos i no queryset Q
                            Q|=Periodo.objects.filter(pk=i.pk)
                #busca retoran algum resultado?
                if Q.count()>0:
                    context['total']= Q.count()
                    #verifica qual campo dever ordenar a resposta  
                    if 'ordenar_por' in r:
                        #e se sera crescente ou decrescente(D)
                        if "fav_order" in r and r['fav_order']=="D":
                            Qp=Q.order_by(f"-{r['ordenar_por']}")
                        else:
                            #crescente
                            Qp=Q.order_by(r['ordenar_por'])
                    else:
                        Qp=Q
                    context['p']=Qp
                    context['total']=Qp.count()
                    messages.success(request, f'Busca retornou {Q.count()} linhas!')
                #busca nao tem resultados
                else:
                    context.pop('p')
                    messages.error(request,'Nenhum resultado encontrado!')
            #Para o caso de nenhum filtro ter sido aplicado ou seja o queryset é "p"
            else:
                #procede o ordenamento como acima
                if 'ordenar_por' in r:
                    if 'fav_order' in r  and r['fav_order']=="D":
                        p=p.order_by(f"-{r['ordenar_por']}")
                    else:
                        p=p.order_by(r['ordenar_por']) 
                else:
                    if 'fav_order' in r  and r['fav_order']=="D":
                        p=p.order_by('-entrada')
                    else:
                        p=p.order_by('entrada')      
                context['p']=p
                messages.success(request,f'Busca retornou {p.count()} linhas!')

    # ###############################################################################PASSANDO OS EMAILS DOS ESTAGIARIOS PARA O CONTEXT 
    PERM=Permitidos.objects.filter(estagiario=True)
    EMAILS=[perm.email for perm in PERM]
    context['emails']=EMAILS
    # ###############################################################################  
    return render(request,'ponto/filtros.html',context)


@login_required(login_url='/login/')
def index(request):
    context,x,botao={},request.user,''   
     #PASSA O USUARIO, O IP, O QUERYSET DOS QUE ENTRARAM(PODE SER VAZIO),E UM DISPLAY SETADO PARA REINICIAR(COMO SE TIVESSE ABRINDO AGORA A BAGAÇA)
    context={'x':x,'ip_conec':get_client_ip(request)} 
    #HORARIO ATUALIZADO
    context['now']=timezone.now()
    if request.method=='POST':
        #queryset de observacoes do usuario em questao
        O=Obs.objects.filter(colaborador=x)
        ja_observado=[i.observacoes for i in O]
        usuario,obs,botao=get_usuario_e_obs(request)
        #deleta obs que forem solicitadas pelo usuario
        if 'del_obs' in request.POST:
            d_o= request.POST['del_obs']
            O.filter(observacoes=d_o).delete()
            messages.warning(request,"Sua observação anotada para registro foi deletada!")         
        if 'obs' in request.POST  and obs not in ja_observado :
            if obs !='':
                o_x=Obs(colaborador=x,observacoes=obs)
                o_x.save()
                messages.success(request,"Observações anotadas. Serão salvas no final no expediente.")
        else:
            if  obs  in ja_observado:
                messages.warning(request,"Observação já salva anteriormente.")
        context['OBS']=Obs.objects.filter(colaborador=x)
        if botao.lower()=='início':
            entrada=timezone.now()
            x= request.user  
            if  Entraram.objects.filter(colaborador=x).count()==0:
                ep=Entraram(entrada=entrada,ip_address=get_client_ip(request),colaborador=usuario,display='entrou')
                ep.save()
                messages.success(request,f"Bom dia, {x.username.capitalize()}! Seu ponto de entrada iniciado! Mão à obra!")
        elif botao.lower()=='término' :
            if Entraram.objects.filter(colaborador=x).count()== 0:
                messages.warning(request,"Voce ja bateu o ponto de saida!")
            else:
                observ=''
                saida=timezone.now()
                try:
                    o_x=Obs.objects.filter(colaborador=x)
                    for i in o_x:
                        observ+=i.observacoes+'; ' 
                        i.delete()
                except Exception as e:
                   messages.error(request,"Houve um erro ao deletar as observações postadas hoje! Informe ao administrador.")
                ep=Entraram.objects.get(colaborador=x)
                entrada=ep.entrada
                ip=ep.ip_address
                ep.delete()
                E=Entraram.objects.filter(colaborador=x)
                for i in E:
                    i.delete()
                u_i=[u.colaborador for u in usuarios_q_ja_iniciaram()]
                if x not in u_i:
                    inicio=entrada
                else:
                    inicio=Periodo.objects.filter(colaborador=usuario).first().entrada
                dias_corridos=get_dias_corridos(inicio)
                casas_decimais_jornada=3 #########################################################Numero de casas decimais que apareceram na jornada!
                jornada= round((((saida-entrada).total_seconds()//1)//3600), casas_decimais_jornada)
                dias_trabalhados=get_dias_trabalhados(x)
                media_dias_trabalhados=round((dias_trabalhados*100/dias_corridos),2)
                horas_totais=get_horas_totais(x)
                media_h_d_c=horas_totais/dias_corridos
                media_h_d_t=horas_totais/dias_trabalhados
                P=Periodo(entrada=entrada,
                        jornada=jornada,
                        saida=saida,
                        horas_totais=horas_totais,
                        ip_address=ip,
                        colaborador=x,
                        data_inicio=inicio,
                        dias_corridos=dias_corridos,
                        dias_trabalhados=dias_trabalhados,
                        media_dias_t=media_dias_trabalhados,
                        media_h_d_c=media_h_d_c,
                        media_h_d_t=media_h_d_t,
                        observacoes=observ,
                        display='saiu')
                P.save()
                messages.success(request,f"Jornada finalizada! Bom descanso {x.username.capitalize()}!")
    # ###############################################################################
    PERM=Permitidos.objects.filter(estagiario=True)
    EMAILS=[p.email for p in PERM]
    context['emails']=EMAILS
    context['e']=Entraram.objects.all()
    context['l']=[u.colaborador for u in context['e']]
    ################################################################################
    return render(request,'ponto/index.html',context)
