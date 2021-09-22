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

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Conta criada com sucesso!')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})


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

def seleciona_nome(request):
    if request.method=='POST':
        r=request.POST
        print(r)
    return render(request,'accounts/geral.html',context) #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<essa funcao serve pra que ? o context nao foi declarado

class RankingTemplateView(TemplateView):
    template_name='users/ranking.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #p=Periodo.objects.order_by('-entrada')
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

