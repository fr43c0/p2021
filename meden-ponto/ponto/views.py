from django.shortcuts import render
from django.views.generic import TemplateView 
from django.contrib.auth.models import User
from .models import Periodo,Entraram,Obs,Filtro
from users.models import Permitidos ######2021
from django.http import HttpResponse
from django.utils import timezone
import datetime
import json
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
    u=User.objects.all()
    for usuario in u:
        q=p.filter(colaborador=usuario).last()           
        l.append(q)
    for i in l:
        if i in p:
            Usuarios.append(i)
            #print(Usuarios)
    #retorna lista de  usuario/Periodo salvos 
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
        print(2,'sem observaçoes')
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
def apaga_objetos_obs(x):# substitui user por x aqui   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    try:
        oo=Obs.objects.filter(colaborador__username=x)# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        print('oooooooooooooo',len(oo), oo)
        while len(oo)>0:
            oo[0].delete()#PARA APAGAR TODOS OS OBJETOS OBS!!!       
    except Exception as e:
        print('apaga objetos obs ', e)
        pass
# ESTA HAVENDO UM ERRO NO DIAS CORRIDOS QUANDO ENTRA NO MESMO DIA DA DIVISAO POR ZERO
def get_dias_corridos(inicio):
        hoje=timezone.now()
        delta=hoje-inicio
        if hoje.date()==inicio.date():
            dias_corridos=1  
        else:
            dias=delta.days
            dias_corridos=dias
        if dias_corridos == 0:#<<<<<<<<<<<<<<<<<<<<<<
            dias_corridos=1   #<<<<<<<<<<<<<<<<<<<<<<
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

#\INUTIL
def status(request):
    pass


  
    
def filtros(request):
    context={}
    p=Periodo.objects.all().order_by('entrada')
    A=[]
    #Pega os anos de uso do APP em uso
    for i in p:
        if i.saida.year not in A:
            A.append(i.saida.year) 
    context['A']=A
    context['p']=p
    l=usuarios_q_ja_iniciaram()
    context['l']=l
    filtro=Filtro.objects.all()
    context['f']=filtro
    # if request.method=='POST':
    #     r=request.POST
    #     if 'usuario'in r.keys():
    #         nome=r['usuario']
    #         context['qual']=r['usuario']
    #         if nome!='Todos':
    #             nome=nome.lower()
    #             print(25*"=> ",nome)
    #             p=Periodo.objects.all().filter(colaborador__username__iexact=nome).order_by('entrada')
    #             print(25*"=> ",nome, ' ',len(p))
    #         else:
    #             p=Periodo.objects.all().order_by('entrada')
    #     if "periodo" not in r.keys():
    #         if "qual" in r.keys() and r['qual']!="Todos" and r['qual']!='':
    #             qual=r['qual']
    #             if "ano" in r.keys():  
    #                 anos=r.getlist('ano')
    #                 if "mes" in r.keys():
    #                     meses=r.getlist('mes')
    #                     p=p.filter(saida__year__in=anos).filter(saida__month__in=meses).filter(colaborador__username__iexact=qual.lower())
    #                 else:
    #                     p=p.filter(saida__year__in=anos).filter(colaborador__username__iexact=qual.lower())
    #             elif "mes" in r.keys():
    #                 meses=r.getlist('mes')
    #                 p=p.filter(saida__month__in=meses).filter(colaborador__username__iexact=qual.lower())
    #         else:    
    #             if "ano" in r.keys():  
    #                 anos=r.getlist('ano')
    #                 if "mes" in r.keys():
    #                     meses=r.getlist('mes')
    #                     p=p.filter(saida__year__in=anos).filter(saida__month__in=meses)
    #                 else:
    #                     p=p.filter(saida__year__in=anos)
    #             elif "mes" in r.keys():
    #                 meses=r.getlist('mes')
    #                 p=p.filter(saida__month__in=meses)      
    # u=User.objects.all()
    # context['u']=u
    # context['p']=p
    # #context={'l':l,'u':u,'p':p,'f':filtro,}
    # context['c']=context
    from django.db.models.functions import TruncDate
    if request.method == 'POST':
            p=Periodo.objects.all()
            r=request.POST
            anos,meses,usuarios=[],[],usuarios_q_ja_iniciaram()
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
            else:
                p=Periodo.objects.all()
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
            dic={}
            periodos=[]
            for u in usuarios:
                XU=X.filter(colaborador__username=u)
                if XU.count()>0:
                    for i in XU:
                        print(i,i.ip_address)
                        periodos.append(i)
            
            context['p']=periodos
    # ###############################################################################PASSANDO OS EMAILS DOS ESTAGIARIOS PARA O CONTEXT 
    PERM=Permitidos.objects.filter(estagiario=True)
    EMAILS=[perm.email for perm in PERM]
    context['emails']=EMAILS
    context['A']=A
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
        # print('---------------------------------- entrou um post generico ! ! ! !')
        # print('len O=====================>',len(O))
        usuario,obs,botao=get_usuario_e_obs(request)
        if 'obs' in request.POST and  len(O)==0 :
            if obs !='':
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
                #print('88888888888888888888',ep.entrada)
                ep.save()
        
        elif botao.lower()=='término':
            observ=''
            saida=timezone.now()
            display='saiu'
            #print('-------------------------------------poste de termino')
            try:
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
            #print('9999999999999999999',entrada)
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
            #print('$$$$$$$$$$$$$$$$$$$$$$',x, inicio,dias_corridos,jornada,dias_trabalhados,media_dias_trabalhados,) ######===ok
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
    
    return render(request,'ponto/index.html',context)