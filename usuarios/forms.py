from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from .models import (Colaborador, CustomUsuario, Departamento, DiaDaSemana,
                     EscalaSemanal, Filial, FolhaDePonto, Marcacao)


class CustomUsuarioCreateForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu primeiro nome'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu sobrenome'}))
    celular = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu Celular'}))
    cpf = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu CPF'}))
    matricula = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira sua Matricula'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu E-mail'}))
    password1 = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira sua senha'}))
    password2 = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Confirme sua senha'}))

    class Meta:
        model = CustomUsuario
        fields = ('cpf','email', 'matricula', 'username', 'first_name',
                  'last_name', 'password1', 'password2')

    def clean_email(self):
        cpf = self.cleaned_data.get('cpf')
        if CustomUsuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError(
                "Este cpf já está registrado. Tente outro.")
        return cpf

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUsuario.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Este nome de usuário já está em uso. Tente outro.")
        return username

    def save(self, commit=True):
        user = super(CustomUsuarioCreateForm, self).save(commit=False)
        user.cpf = self.cleaned_data['cpf']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class CustomUsuarioChangeForm(UserChangeForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'celular')


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

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'escala_semanal']

class MarcacaoForm(forms.ModelForm):
    class Meta:
        model = Marcacao
        fields = ['colaborador', 'dia', 'marcacoes']

class FolhaDePontoForm(forms.ModelForm):
    class Meta:
        model = FolhaDePonto
        fields = ['colaborador', 'mes', 'ano', 'marcacoes']
