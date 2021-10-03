from django.db.models.expressions import F, OrderBy
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView 
from django.contrib.auth.models import User
from .models import Periodo,Entraram,Obs,Filtro
from users.models import Permitidos ######2021
# from django.http import HttpResponse
from django.utils import timezone
# import datetime
# import json
import pytz
tz=pytz.timezone('America/Sao_Paulo')
u=User.objects.all()
e=Entraram.objects.all()

def total_mes(usuario):
    pass
def total_geral(usuario):
    pass

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
    # u=User.objects.all()
    # for usuario in u:
    #     q=p.filter(colaborador=usuario).last()           
    #     l.append(q)
    # for i in l:
    #     if i in p:
    #         Usuarios.append(i)
    #         #print(Usuarios)
    # print('usando a for para lista',l)
    #retorna lista de  usuario/Periodo salvos
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
    print(1, 'request', r)
    if 'obs' in r:
        obs=r['obs']
    else:
        obs=''
    i=request.user
    if  i.username in r.keys():
        botao=r[i.username]
        print(3,'botao',botao)
    return i,obs,botao


def get_display_status(context):
    if 'entrada' not in context and 'saida' not in context:
        context['display']='reiniciar'
    elif'saida' not in context and 'entrada'in context:
        context['display']='entrou'   
    return context

def get_context(context,request):
    e=Entraram.objects.all().order_by('entrada')
    now=timezone.now()
    ativos={'ativos':[u.colaborador.username for u in usuarios_q_ja_iniciaram()]}
    lista=[u.colaborador for u in e]
    context={'now':now,'ip_conec':get_client_ip(request),'l':lista}
    if len(e)>0:
        context['e']=e.order_by('entrada')
    context2=get_display_status(context)
    return context2,lista


#VERIFICAR UTILIDADE DESSA FUNCAO POIS PARECE QUE NAO ESTA SENDO USADA
# def apaga_objetos_obs(x):# substitui user por x aqui   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#     try:
#         oo=Obs.objects.filter(colaborador__username=x)# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#         print('oooooooooooooo',len(oo), oo)
#         while len(oo)>0:
#             oo[0].delete()#PARA APAGAR TODOS OS OBJETOS OBS!!!       
#     except Exception as e:
#         print('apaga objetos obs ', e)
#         pass

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
        print('d ', d, x)
        if d not in l:
            l.append(d)
    dias_trabalhados=len(l)
    if dias_trabalhados==0:
        dias_trabalhados=1
    print(len(l))
    return dias_trabalhados

def get_horas_totais(x):
    p=Periodo.objects.filter(colaborador=x)
    total=0
    for i in p:
        j=i.jornada
        total=total+j
    return total

def status(request):
    pass


def ordenarQuery(query,param):
    pass

def filtros(request):
    p=Periodo.objects.all().order_by('entrada')
    context={}
    context['p']=p
    context['A']=Periodo.objects.all().values('entrada__year').distinct()
    context['l']=usuarios_q_ja_iniciaram()
    print ("filtros context['l']=usuarios_q_ja_iniciaram()")
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
                    print(f'p.conutn=========>{Q.count()}')
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
                print(f'p.conutn=========>{p.count()}')
                messages.success(request,f'Busca retornou {p.count()} linhas!')

    # ###############################################################################PASSANDO OS EMAILS DOS ESTAGIARIOS PARA O CONTEXT 
    PERM=Permitidos.objects.filter(estagiario=True)
    EMAILS=[perm.email for perm in PERM]
    context['emails']=EMAILS
    # ###############################################################################  
    #print(f'context {context}')
    return render(request,'ponto/filtros.html',context)

def index(request):
    #print('-----------------------------------cabeça da view')
    #x=User.objects.order_by('-last_login')[0]
    context,e,x,obx,botao={},Entraram.objects.all().order_by('entrada'),request.user,'',''
    context={'x':x,'e':e ,'ip_conec':get_client_ip(request),'display':'reiniciar'}
    context2,lista=get_context(context,request)
    context['l']=lista
    context['now']=timezone.now()
    try:
        #print( 'tentando adicionar oxoxoxoxox')
        context['OBS']=Obs.objects.all()    
    except:
        #print( 'deu ruim aqui')
        pass

    if request.method=='POST':
        O=Obs.objects.filter(colaborador=x)
        print('---------------------------------- entrou um post generico ! ! ! !')
        print('len O=====================>',len(O))
        usuario,obs,botao=get_usuario_e_obs(request)
        if 'obs' in request.POST and  len(O)==0 :
            if obs !='':
                print(O)
                o_x=Obs(colaborador=x,observacoes=obs)
                o_x.save()
        if botao.lower()=='início':
            entrada=timezone.now()
            #print('------------------------------------poste de inicio')
            try:
                o_x=Obs.objects.get(colaborador=x)
                observ=o_x.observacoes
            except:
                pass
            x= request.user  
            lista.append(x)
            if  len(Entraram.objects.filter(colaborador=x))==0:
                ep=Entraram(entrada=entrada,ip_address=get_client_ip(request),colaborador=usuario,display='entrou')
                ep.save()
        elif botao.lower()=='término':
            observ=''
            saida=timezone.now()
            display='saiu'
            #print('-------------------------------------post de termino')
            try:
                #tentando apagar as observacoes do usuario ao bater o ponto de saida
                o_x=Obs.objects.get(colaborador=x)
                observ=o_x.observacoes
                o_x.delete()
               # print('observ================>',observ)
    
            except Exception as e:
                print(e)
                pass
        
            if x in lista:
                lista.pop(lista.index(x))
            
            ep=Entraram.objects.get(colaborador=x)
            entrada=ep.entrada
            ip=ep.ip_address
            display_anterior=ep.display
            ep.delete()
            E=Entraram.objects.filter(colaborador=x)
            for i in E:
                i.delete()
            
            #,observacoes,desligado
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
        elif botao.lower()=='reiniciar':
            pass
    elif request.method=='GET':
        #print('--------------------------------------Get no fim da pagina')
        if x not in context['l']:
            context['x']=x
    #for i in context:
        #print('_____________________________________________________________________"')
       # print(5, 'contexto final: ',i,' : ',context[i])
        
    #print('------------------------------------------ultima linha da view')
    # ###############################################################################
    PERM=Permitidos.objects.filter(estagiario=True)
    EMAILS=[p.email for p in PERM]
    context['emails']=EMAILS
    # ###############################################################################
    print(context)
    return render(request,'ponto/index.html',context)