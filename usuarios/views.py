from collections import defaultdict

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import (CustomUsuarioChangeForm, CustomUsuarioCreateForm,
                    DepartamentoForm, DiaDaSemanaForm, EscalaSemanalForm,
                    FilialForm, FolhaDePontoForm, LoginForm, MarcacaoForm)
from .models import (CustomUsuario, Departamento, DiaDaSemana, EscalaSemanal,
                     Filial, FolhaDePonto, Marcacao)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario ou senha incorretos')
    return render(request, 'registration/login.html', {'error': messages.get_messages(request)})


@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')





############################################################################################################################


# Folha de Ponto

class FolhaDePontoListView(ListView):
    model = FolhaDePonto
    template_name = 'ponto/folha_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        folhas = context['object_list']

        for folha in folhas:
            marcacoes_dict = defaultdict(list)

            for marcacao in folha.marcacoes.all().order_by('dia', 'marcacoes'):
                marcacoes_dict[marcacao.dia].append(marcacao)

            folha.marcacoes_dict = dict(marcacoes_dict)

        return context

class FolhaDetailView(DetailView):
    model = FolhaDePonto
    template_name = 'ponto/folha_detail.html'

class FolhaDePontoCreateView(CreateView):
    model = FolhaDePonto
    form_class = FolhaDePontoForm
    template_name = 'ponto/folha_new.html'
    success_url = reverse_lazy('folha_list')
    def form_valid(self, form):
        

        response = super().form_valid(form)
        messages.success(self.request, 'A Folha foi criada com sucesso!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, 'Ocorreu um erro ao criar a Folha. Por favor, tente novamente.')
        return response



class FolhaUpdateView(UpdateView):
    model = FolhaDePonto
    template_name = 'ponto/folha_edit.html'
    fields = ['colaborador', 'mes','ano', 'marcacoes']
    success_url = reverse_lazy('folha_list')

class FolhaDeleteView(DeleteView):
    model = FolhaDePonto
    template_name = 'ponto/folha_delete.html'
    success_url = reverse_lazy('folha_list')



############################################################################################################################


# Colaborador


class ColaboradorListView(ListView):
    model = CustomUsuario
    template_name = 'ponto/colaborador_list.html'

class ColaboradorDetailView(DetailView):
    model = CustomUsuario
    template_name = 'ponto/colaborador_detail.html'

class ColaboradorCreateView(CreateView):
    model = CustomUsuario
    form_class = CustomUsuarioCreateForm
    template_name = 'ponto/colaborador_new.html'
    success_url = reverse_lazy('colaborador_list')

    def form_valid(self, form):

        response = super().form_valid(form)
        messages.success(self.request, 'O colaborador foi criado com sucesso!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, 'Ocorreu um erro ao criar colaborador. Por favor, tente novamente.')
        return response


class ColaboradorUpdateView(UpdateView):
    model = CustomUsuario
    form_class = CustomUsuarioChangeForm
    template_name = 'ponto/colaborador_edit.html'
    success_url = reverse_lazy('colaborador_list')

    def form_valid(self, form):

        response = super().form_valid(form)
        messages.success(self.request, 'O colaborador foi atualizado com sucesso!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, 'Ocorreu um erro ao atualizar o colaborador. Por favor, tente novamente.')
        return response



class ColaboradorDeleteView(DeleteView):
    model = CustomUsuario
    template_name = 'ponto/colaborador_delete.html'
    success_url = reverse_lazy('colaborador_list')



############################################################################################################################



# Escala


class EscalaListView(ListView):
    model = EscalaSemanal
    template_name = 'ponto/escala_list.html'

class EscalaDetailView(DetailView):
    model = EscalaSemanal
    template_name = 'ponto/escala_detail.html'

class EscalaCreateView(CreateView):
    model = EscalaSemanal
    form_class = EscalaSemanalForm
    template_name = 'ponto/escala_new.html'
    success_url = reverse_lazy('escala_list')
    def form_valid(self, form):

        response = super().form_valid(form)
        messages.success(self.request, 'O Ponto foi atualizado com sucesso!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, 'Ocorreu um erro ao atualizar o Ponto. Por favor, tente novamente.')
        return response

class EscalaUpdateView(UpdateView):
    model = EscalaSemanal
    template_name = 'ponto/escala_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('escala_list')
    
    def form_valid(self, form):

        response = super().form_valid(form)
        messages.success(self.request, 'O Ponto foi atualizado com sucesso!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, 'Ocorreu um erro ao atualizar o Ponto. Por favor, tente novamente.')
        return response
    
class EscalaDeleteView(DeleteView):
    model = EscalaSemanal
    template_name = 'ponto/escala_delete.html'
    success_url = reverse_lazy('escala_list')



############################################################################################################################


# Marcação De Ponto





class MarcacaoPontoListView(LoginRequiredMixin, ListView):
    model = Marcacao
    template_name = 'ponto/marcacao_ponto_list.html'


class MarcacaoPontoDetailView(LoginRequiredMixin, DetailView):
    model = Marcacao
    template_name = 'ponto/marcacao_ponto_detail.html'

class MarcacaoPontoCreateView(LoginRequiredMixin, CreateView):
    model = Marcacao
    form_class = MarcacaoForm
    template_name = 'ponto/marcacao_ponto_new.html'
    success_url = reverse_lazy('marcacao_ponto_list')

    def form_valid(self, form):

        response = super().form_valid(form)
        messages.success(self.request, 'O Ponto foi atualizado com sucesso!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, 'Ocorreu um erro ao atualizar o Ponto. Por favor, tente novamente.')
        return response

class MarcacaoPontoUpdateView(LoginRequiredMixin, UpdateView):
    model = Marcacao
    form_class = MarcacaoForm
    template_name = 'ponto/marcacao_ponto_edit.html'
    success_url = reverse_lazy('folha_list')

    def form_valid(self, form):

        response = super().form_valid(form)
        messages.success(self.request, 'O Ponto foi atualizado com sucesso!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, 'Ocorreu um erro ao atualizar o Ponto. Por favor, tente novamente.')
        return response

class MarcacaoPontoDeleteView(LoginRequiredMixin, DeleteView):
    model = Marcacao
    template_name = 'ponto/marcacao_ponto_delete.html'
    success_url = reverse_lazy('marcacao_ponto_list')



############################################################################################################################


# Dia da Semana





class DiaDaSemanaListView(LoginRequiredMixin, ListView):
    model = DiaDaSemana
    template_name = 'ponto/dia_list.html'

class DiaDaSemanaDetailView(LoginRequiredMixin, DetailView):
    model = DiaDaSemana
    template_name = 'ponto/dia_detail.html'

class DiaDaSemanaCreateView(LoginRequiredMixin, CreateView):
    model = DiaDaSemana
    form_class = DiaDaSemanaForm
    template_name = 'ponto/dia_new.html'
    success_url = reverse_lazy('dia_list')

    def form_valid(self, form):

        response = super().form_valid(form)
        messages.success(self.request, 'O Dia foi atualizado com sucesso!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, 'Ocorreu um erro ao atualizar o Dia. Por favor, tente novamente.')
        return response

class DiaDaSemanaUpdateView(LoginRequiredMixin, UpdateView):
    model = DiaDaSemana
    form_class = DiaDaSemanaForm
    template_name = 'ponto/dia_edit.html'
    success_url = reverse_lazy('dia_list')

    def form_valid(self, form):

        response = super().form_valid(form)
        messages.success(self.request, 'O Dia foi atualizado com sucesso!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, 'Ocorreu um erro ao atualizar o Dia. Por favor, tente novamente.')
        return response

class DiaDaSemanaDeleteView(LoginRequiredMixin, DeleteView):
    model = DiaDaSemana
    template_name = 'ponto/dia_delete.html'
    success_url = reverse_lazy('dia_list')





############################################################################################################################

# Filiais


class FilialListView(ListView):
    model = Filial
    template_name = 'ponto/filial_list.html'

class FilialDetailView(DetailView):
    model = Filial
    template_name = 'ponto/filial_detail.html'

class FilialCreateView(CreateView):
    model = Filial
    form_class = FilialForm
    template_name = 'ponto/filial_new.html'
    success_url = reverse_lazy('filial_list')

    def form_valid(self, form):
        

        response = super().form_valid(form)
        messages.success(self.request, 'A filial foi criado com sucesso!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, 'Ocorreu um erro ao criar a filial. Por favor, tente novamente.')
        return response

class FilialUpdateView(UpdateView):
    model = Filial
    template_name = 'ponto/filial_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('filial_list')

class FilialDeleteView(DeleteView):
    model = Filial
    template_name = 'ponto/filial_delete.html'
    success_url = reverse_lazy('filial_list')










############################################################################################################################




# Departamentos

class DepartamentoListView(ListView):
    model = Departamento
    template_name = 'ponto/departamento_list.html'

class DepartamentoDetailView(DetailView):
    model = Departamento
    template_name = 'ponto/departamento_detail.html'

class DepartamentoCreateView(CreateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'ponto/departamento_new.html'
    success_url = reverse_lazy('departamento_list')
    def form_valid(self, form):
        

        response = super().form_valid(form)
        messages.success(self.request, 'O departamento foi criado com sucesso!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, 'Ocorreu um erro ao criar o departamento. Por favor, tente novamente.')
        return response



class DepartamentoUpdateView(UpdateView):
    model = Departamento
    template_name = 'ponto/departamento_edit.html'
    fields = ['nome', 'filial']
    success_url = reverse_lazy('departamento_list')

class DepartamentoDeleteView(DeleteView):
    model = Departamento
    template_name = 'ponto/departamento_delete.html'
    success_url = reverse_lazy('departamento_list')








