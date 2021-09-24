from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserRegisterForm
from ponto.models import Periodo
from users.models import Permitidos
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.views.generic import ListView, TemplateView,CreateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.utils import timezone
import datetime
from calendar import monthrange
from django.db.models.functions import TruncDate
#calculo dos dias trabalhados:
#filtra os periodos ja retornados na busca por usuario
#ordena por entrada
#count distinct datas.day de entrada
#count distinct datas.day de saida



def getDiasCorridosPorUser(usuario,anos,meses):
    p=Periodo.objects.all()
    data_inicial=p.filter(colaborador__username=usuario).last().data_inicio.date()
    mes_inicial=data_inicial.month
    ano_inicial=data_inicial.year
    d,m,a=data_inicial,mes_inicial,ano_inicial
    print(d,m,a)
    if anos== [] and meses == []:
        DiasCorridos=p.filter(colaborador__username=usuario).last().dias_corridos
        return DiasCorridos
    
    if len (anos) > 0 and meses == []:
    #calcula os blocos de anos inteiros menos o do ano de entrada que deve ser descontado os dias ate a entrada
    # todos os anos valem 365 menos o ano da data inicial
        DiasCorridos=0
        for ano in anos:
            ano=int(ano)
            trabalhouNesseAno=len(p.filter(colaborador__username=usuario).filter(entrada__year=ano))
            
            # esta trabalhando no ano atual desde o inicio do ano 
            if ano == datetime.datetime.now().year and  ano_inicial != ano and trabalhouNesseAno > 0:
                delta=(datetime.datetime.now()-datetime.datetime(ano,1,1)).days
                DiasCorridos+=delta
            
            # trabalhou um ano ja terminado do inicio ao fim
            if ano != datetime.datetime.now().year and  ano_inicial != ano and trabalhouNesseAno > 0:
                DiasCorridos+=365
            
            #Trabalhou  em ano ja terminado porem começou depois do inicio do ano
            if ano_inicial == ano and ano != datetime.datetime.now().year:
                fim_do_ando=datetime.date(ano_inicial,12,31)
                delta=datetime.date(ano_inicial,12,31) - datetime.date(ano_inicial,mes_inicial,data_inicial.day) 
                DiasCorridos+=delta.days
            
            #iniciou nesse ano atual que ainda nao acabou porem comecou depois do inicio do ano
            if ano_inicial == ano and ano == datetime.datetime.now().year:
                delta=(datetime.datetime.now()-datetime.datetime(ano,mes_inicial,data_inicial.day)).days
                DiasCorridos+=delta.days
         

            
        return DiasCorridos
        
    if len (meses) > 0 and anos == []:
        DiasCorridos=0
        data_ultima= data_inicial=p.filter(colaborador__username=usuario).last().entrada.date()
        data_ultima_mes=data_ultima.month
        data_ultima_ano=data_ultima.year
        for mes in meses:
            conta_ano=0
            while ano_inicial+conta_ano <= data_ultima_ano:
                trabalhouNesseMesEnesseAno = len(p.filter(colaborador__username=usuario).filter(entrada__year=ano_inicial+conta_ano).filter(entrada__month=mes))
                if mes == mes_inicial  and trabalhouNesseMesEnesseAno >0:
                    #conta (e soma) os dias do um mes de um ano e (caso seja o mes de entrada)  diminui do dia de entrada
                    DiasCorridos=(DiasCorridos+monthrange(int(ano_inicial+conta_ano),int(mes))[1])-data_inicial.day
                if mes != mes_inicial  and trabalhouNesseMesEnesseAno >0:
                    DiasCorridos+= monthrange(int(ano_inicial+conta_ano),int(mes))[1]
                conta_ano+=1
        return DiasCorridos
    
    if len (meses) > 0 and  len (anos) > 0 :
        DiasCorridos=0
        data_ultima= data_inicial=p.filter(colaborador__username=usuario).last().entrada.date()
        data_ultima_mes=data_ultima.month
        data_ultima_ano=data_ultima.year
        for ano in anos:
            ano=int(ano)
            if ano >= ano_inicial:
                for mes in meses:
                    trabalhouNesseMesEnesseAno = len(p.filter(colaborador__username=usuario).filter(entrada__year=ano).filter(entrada__month=mes))
                    if mes == mes_inicial  and trabalhouNesseMesEnesseAno > 0:
                        #conta (e soma) os dias do um mes de um ano e (caso seja o mes de entrada)  diminui do dia de entrada
                        DiasCorridos=(DiasCorridos+monthrange(int(ano),int(mes))[1])-data_inicial.day
                    if mes != mes_inicial  and trabalhouNesseMesEnesseAno >0:
                        DiasCorridos+=monthrange(int(ano),int(mes))[1]
                    
        return DiasCorridos    

def ranking_filter(request):
    usuarios,anos,meses=usuarios_q_ja_iniciaram(),[],[]
    context={}
    QF=Periodo.objects.none()
    L=[]
    if request.method == 'POST':
        p=Periodo.objects.all()
        print('P>>>>>>>>>>>>> ',len(p))
        r=request.POST
        print(r)
        anos,meses,usuarios=[],[],usuarios_q_ja_iniciaram()
        if "usuario" in r.keys():
            usuarios=r.getlist('usuario')      
            #p=Periodo.objects.all()
            if "ano" in r.keys() and "mes" in r.keys() :
                anos,meses=r.getlist('ano'),r.getlist('mes')
                X=p.filter(colaborador__username__in=usuarios).filter(entrada__year__in=anos).filter(entrada__month__in=meses)
                
            if "ano" in r.keys() and "mes"  not in r.keys() :
                anos=r.getlist('ano')
                X=p.filter(colaborador__username__in=usuarios).filter(entrada__year__in=anos)
               
            if "mes" in r.keys() and "ano"  not in r.keys() :
                meses=r.getlist('mes')
                X=p.filter(colaborador__username__in=usuarios).filter(entrada__month__in=meses)
                
            if "mes" not in r.keys() and "ano"  not in r.keys() :
                X=p.filter(colaborador__username__in=usuarios)
                
        else:
            p=Periodo.objects.all()
            if "ano" in r.keys() and "mes" in r.keys() :
                anos,meses=r.getlist('ano'),r.getlist('mes')
                X=p.filter(entrada__year__in=anos).filter(entrada__month__in=meses)
                print('anomes')
            if "ano" in r.keys() and "mes"  not in r.keys() :
                anos=r.getlist('ano')
                X=p.filter(entrada__year__in=anos)
                print('so-ano')
            if "mes" in r.keys() and "ano"  not in r.keys() :
                meses=r.getlist('mes')
                X=p.filter(entrada__month__in=meses)
                print('so-mes')
            if "mes" not in r.keys() and "ano"  not in r.keys() :
                X=p
                print('nemanonemmes')    
        dic={}
        LU=[]
        for u in usuarios:
            XU=X.filter(colaborador__username=u)
            if XU.count()>0:
                total_horas=0
                for i in XU:
                    total_horas+=i.jornada
                #https://stackoverflow.com/questions/49586301/django-count-unique-dates-in-queryset
                d_t=XU.annotate(date=TruncDate('entrada')).values('date').distinct().count()
                print(d_t,' ' ,u, '=============================================')
                d_c=getDiasCorridosPorUser(u,anos,meses)
                dic=   { 'colaborador':u,
                        'dias_corridos':d_c,
                        'dias_trabalhados':d_t,
                        'horas_totais':round(total_horas,1),
                        'media_dias_t':round(100*d_t/d_c,1),
                        'media_h_d_c':round(total_horas/d_c,1),
                        'media_h_d_t':round(total_horas/d_t,1) ,
                        }
                LU.append(dic)
        print(80*'-')
        for i in LU:
            print(f'{i}')
        print(80*'-')
        context['LU']=LU
        Usuarios=[]
        l=[]
        if len(anos)==0:
            anos='Todos'
        if len(meses)==0:
            meses='Todos'
        context['anos']=anos
        context['meses']=meses
        PERM=Permitidos.objects.filter(estagiario=True)
        EMAILS=[p.email for p in PERM]
        context['emails']=EMAILS
        # ###############################################################################
        context['U']=Usuarios       
        context['p']=p
    return render(request,'users/ranking_filtrado.html',context) 



#TEM UTILIDADE ESSA FUNCAO?
def seleciona_nome(request):
    if request.method=='POST':
        r=request.POST
        print(r)
        context={}
    return render(request,'accounts/geral.html',context) #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<essa funcao serve pra que ? o context nao foi declarado


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

#Para editar o cargo do entre estagiario e efetivado
@staff_member_required 
def editar_permitido(request,pk):
    if request.method == 'POST':
        r=request.POST
        if "cargo" in r.keys():
            if r['cargo'] == 'efetivado':
                P=Permitidos.objects.get(pk=pk)
                P.estagiario=False
                P.save()
                print(P.email)
            if r['cargo'] == 'estagiario':
                P=Permitidos.objects.get(pk=pk)
                P.estagiario=True
                P.save()
        LIST=Permitidos.objects.all()
        context={}
        context['permitidos']=LIST
        return redirect('users:permitidos')


@staff_member_required 
def del_user(request,pk): 
    if request.method == 'POST':
        EMAIL=(request.POST)['email']
    try:
        u = User.objects.get(email = EMAIL)
        print(u,User.objects.all())
        u.delete()
        print(User.objects.all())
        p=Permitidos.objects.get(email = EMAIL)
        p.delete()
        messages.success(request, "Usuario Deletado do Banco de Dados")            

    except User.DoesNotExist:
        messages.error(request, "Usuario nao consta no Banco de Dados!")
        print(messages.get_messages(request))
        return redirect('users:permitidos')

    # except Exception as e: 
    #     return render(request, 'front.html',{'err':e.message})
    LIST=Permitidos.objects.all()
    context={}
    context['permitidos']=LIST
    return redirect('users:permitidos')



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        email=(request.POST)['email']
        emails=Permitidos.objects.all()
        emails_permitidos=[e.email for e in emails]
        if email not in emails_permitidos:
            return HttpResponse('<h2>Email não permitido. Entre em contato com o administrador.<h2>')
        else:
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Conta criada com sucesso!')
                return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# class UserListView(ListView): #veio do laptop
#     model = Periodo
#     context_object_name = ''
#     template_name='accounts/perfil.html'

class UserListView(ListView):
    model = Periodo
    context_object_name = ''
    template_name='accounts/perfil.html'
    ordering = ['-entrada']

class GeralListView(ListView):
    model = Periodo
    context_object_name = ''
    template_name='accounts/geral.html'
    ordering = ['-entrada'] 
    def get_context_data(self,**kwargs):
        context=super(GeralListView,self).get_context_data(**kwargs)
        context['u'] = usuarios_q_ja_iniciaram()
        # ###############################################################################
        PERM=Permitidos.objects.filter(estagiario=True)
        EMAILS=[p.email for p in PERM]
        context['emails']=EMAILS
        # ###############################################################################
        return context

class RankingTemplateView(TemplateView):
    template_name='users/ranking.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Usuarios=[]
        l=[]
        p=Periodo.objects.all()
        A=[]
        for i in p:
            if i.entrada.year not in A:
                A.append(i.entrada.year)
        context['A']=A 
        u=User.objects.all().order_by('username')
        for usuario in u:
            print(usuario)
            q=p.filter(colaborador=usuario).last()
            l.append(q)
        for i in l:
            if i in p:
                Usuarios.append(i)
        # ###############################################################################
        PERM=Permitidos.objects.filter(estagiario=True)
        EMAILS=[p.email for p in PERM]
        context['emails']=EMAILS
        # ###############################################################################
        context['U']=Usuarios
        return context
class ParticipantesTemplateView(TemplateView):
    part2=[]
    model=User
    template_name='users/participantes.html'
    part=User.objects.all()
    participantes=[p.username for p in part]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participantes"] = User.objects.all()
        # ###############################################################################
        PERM=Permitidos.objects.filter(estagiario=True)
        EMAILS=[p.email for p in PERM]
        context['emails']=EMAILS
        # ###############################################################################
        return context
    
class EmailCreateView(CreateView):
    fields=('email','estagiario')
    model=Permitidos
    #success_url = 'users:detalhe'
    #template_name='accounts/super'
    
class EmailListView(ListView):
    model=Permitidos
    context_object_name = 'permitidos'
    template_name='accounts/permitidos/'

class EmailDetailView(DetailView):
    model=Permitidos
    context_object_name = 'permitido'
   

class EmailDeleteView(DeleteView):
    model=Permitidos
    success_url =reverse_lazy('users:permitidos')

