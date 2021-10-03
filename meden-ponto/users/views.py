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
# from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin 
import datetime
from calendar import monthrange
from django.db.models.functions import TruncDate

#calculo dos dias trabalhados:
def getDiasCorridosPorUser(usuario,anos,meses):
    p=Periodo.objects.all()
    data_inicial=p.filter(colaborador__username=usuario).last().data_inicio.date()
    mes_inicial=data_inicial.month
    ano_inicial=data_inicial.year
    d,m,a=data_inicial,mes_inicial,ano_inicial
    print(d,m,a)
    #=============================================
    #Anos sao selecionados
    if len(anos)>0:
    #=============================================
        if len(meses)>0:
            #anos e meses sao selecionados
            DiasCorridos=0
            #data_ultima_ano=p.filter(colaborador__username=usuario).last().entrada.date().year
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
        #===============================================
        #(anos sao) selecionados mas nao meses
        else:
        #===============================================
            DiasCorridos=0
            for ano in anos:
                ano=int(ano)
                DiasQueTrabalhouNesseAno=(p.filter(colaborador__username=usuario).filter(entrada__year=ano)).count()
                #contando ano atual
                if DiasQueTrabalhouNesseAno > 0:
                    #contando ano atual
                    if ano == datetime.datetime.now().year:
                        #iniciou no ano atual
                        if ano_inicial ==datetime.datetime.now().year:
                                #diff de data atual e a data de inicio
                                delta=(datetime.datetime.now()-datetime.datetime(ano,mes_inicial,data_inicial.day)).days
                                DiasCorridos+=delta.days
                        #inciou em ano anterior
                        else:
                            #diff do dia 1 de jan ate dia atual
                                delta=(datetime.datetime.now()-datetime.datetime(ano,1,1)).days
                                DiasCorridos+=delta
                    #contando anos anteriores ao atual
                    else:
                        #iniciou no ano em questao?
                        if ano_inicial == ano:
                            fim_do_ando=datetime.datetime(ano_inicial,12,31)
                            #caso positivo conta da data inicial ate o fim do ano
                            delta=datetime.datetime(ano_inicial,12,31) - datetime.datetime(ano_inicial,mes_inicial,data_inicial.day) 
                            DiasCorridos+=delta.days 
                        else:
                            #senao conta o ano inteiro
                            DiasCorridos+=365 
                    return DiasCorridos
                else:
                    #caso em que nao trabalhou nesse ano
                    return 0
    #================================================
    #Caso em que [anos nao sao] selecionados
    else:
    #================================================
        #===========
        #meses sao
        if len(meses)>0:
            DiasCorridos=0
            data_ultima_ano=p.filter(colaborador__username=usuario).last().entrada.date().year
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
        #==============
        #meses nao sao   
        else:
            #caso em que nada é filtrado > retorna o total acumulado no banco de dados
            DiasCorridos=p.filter(colaborador__username=usuario).last().dias_corridos
            return DiasCorridos

@staff_member_required 
def ranking_filter(request):
    usuarios,anos,meses=usuarios_q_ja_iniciaram(),[],[]
    context={}
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
            # p=Periodo.objects.all()
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
                        'data_inicio':i.data_inicio,
                        'dias_corridos':d_c,
                        'dias_trabalhados':d_t,
                        'horas_totais':round(total_horas,1),
                        'media_dias_t':round(100*d_t/d_c,1),
                        'media_h_d_c':round(total_horas/d_c,1),
                        'media_h_d_t':round(total_horas/d_t,1) ,
                        }
                LU.append(dic)
        context['LU']=LU
        if len(anos)==0:
            anos=['Todos']
        if len(meses)==0:
            meses=['Todos']
        context['anos']=anos
        context['meses']=meses
        PERM=Permitidos.objects.filter(estagiario=True)
        EMAILS=[p.email for p in PERM]
        context['emails']=EMAILS
    return render(request,'users/ranking_filtrado.html',context) 


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
                messages.success(request, f"Usuario {P.email}  salvo com cargo de EFETIVADO!")  
            if r['cargo'] == 'estagiario':
                P=Permitidos.objects.get(pk=pk)
                P.estagiario=True
                P.save()               
                messages.success(request, f"Usuario {P.email}  salvo com cargo de  ESTAGIÁRIO!")   

        else:
            messages.warning(request,"Nenhuma alteração foi selecionada!")
            return render(request, 'users/permitidos_detail.html',{'permitido': Permitidos.objects.get(pk=pk) })
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

@login_required
def userProfile(request):
    e=request.user.email
    p=Periodo.objects.filter(colaborador__email=e)
    context={'periodos':p.order_by('-entrada')}
    return render(request, 'users/perfil.html' , context)


# class UserListView(LoginRequiredMixin,ListView):
#     model = Periodo
#     context_object_name = ''
#     template_name='accounts/perfil.html'
#     ordering = ['-entrada']
#     def get_context_data(self,**kwargs):
#         context=super(UserListView,self).get_context_data(**kwargs)
#         for u in usuarios_q_ja_iniciaram():
#             context[u.colaborador.username]=Periodo.objects.filter(colaborador__username =u)
#             print(context)
#             return context
   
class GeralListView(LoginRequiredMixin,ListView):
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

class RankingTemplateView(LoginRequiredMixin,TemplateView):
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
class ParticipantesTemplateView(LoginRequiredMixin,TemplateView):
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
    
class EmailCreateView(LoginRequiredMixin,CreateView):
    fields=('email','estagiario')
    model=Permitidos
    #success_url = 'users:detalhe'
    #template_name='accounts/super'
    
class EmailListView(LoginRequiredMixin,ListView):
    model=Permitidos
    context_object_name = 'permitidos'
    template_name='accounts/permitidos/'

class EmailDetailView(LoginRequiredMixin,DetailView):
    model=Permitidos
    context_object_name = 'permitido'
   
class EmailDeleteView(LoginRequiredMixin,DeleteView):
    model=Permitidos
    success_url =reverse_lazy('users:permitidos')

 # p=Periodo.objects.all()