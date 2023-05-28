from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from .models import (CustomUsuario, Departamento, DiaDaSemana, EscalaSemanal,
                     Filial, FolhaDePonto, Marcacao)


class CustomUsuarioCreateForm(UserCreationForm):
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu nome'}))
    celular = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu Celular'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu E-mail'}))
    cpf = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu CPF'}), required=True)
    matricula = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira sua Matricula'}))
    password1 = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira sua senha'}))
    password2 = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Confirme sua senha'}))
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=True)
    escala_semanal = forms.ModelChoiceField(queryset=EscalaSemanal.objects.all(), required=True)


    class Meta:
        model = CustomUsuario
        fields = ( 'nome','celular','email','cpf','matricula','password1','password2', 'rg', 'pis', 'cargo', 'sexo', 'data_admissao', 'data_demissao', 'data_nascimento', 'escala_semanal', 'departamento')

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if CustomUsuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError(
                "Este cpf já está registrado. Tente outro.")
        return cpf

    def save(self, commit=True):
        user = super(CustomUsuarioCreateForm, self).save(commit=False)
        user.cpf = self.cleaned_data['cpf']
        if commit:
            user.save()
        return user


class CustomUsuarioChangeForm(UserChangeForm):
    password = None  

    class Meta:
        model = CustomUsuario
        fields = ['nome', 'email','celular', 'cpf', 'matricula', 'rg', 'pis', 'cargo', 'sexo', 'data_admissao', 'data_demissao', 'data_nascimento', 'escala_semanal', 'departamento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name not in ['nome', 'email','celular', 'cpf', 'matricula', 'rg', 'pis', 'cargo', 'sexo', 'data_admissao', 'data_nascimento', 'escala_semanal', 'departamento']:
                self.fields[field_name].required = False


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'CPF', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Senha', 'class': 'form-control'}))
    



class FilialForm(forms.ModelForm):
    class Meta:
        model = Filial
        fields = ['nome']

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['nome', 'filial']

class DiaDaSemanaForm(forms.ModelForm):
    class Meta:
        model = DiaDaSemana
        fields = ['dia', 'entrada1', 'saida1', 'entrada2', 'saida2', 'folga']

class EscalaSemanalForm(forms.ModelForm):
    class Meta:
        model = EscalaSemanal
        fields = ['nome', 'dias']

class MarcacaoForm(forms.ModelForm):
    class Meta:
        model = Marcacao
        fields = ['colaborador', 'dia', 'marcacoes']

class FolhaDePontoForm(forms.ModelForm):
    class Meta:
        model = FolhaDePonto
        fields = ['colaborador', 'mes', 'ano', 'marcacoes']
