from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .forms import CustomUsuarioChangeForm, CustomUsuarioCreateForm
from .models import (CustomUsuario, Departamento, DiaDaSemana, EscalaSemanal,
                     Filial, FolhaDePonto, Marcacao)


class CustomUsuarioCreateForm(UserCreationForm):
    class Meta:
        model = CustomUsuario
        fields = ('email', 'username', 'nome', 'password1', 'password2')
        field_order = ['email', 'username', 'nome', 'password1', 'password2']


class CustomUsuarioChangeForm(UserChangeForm):
    class Meta:
        model = CustomUsuario
        fields = UserChangeForm.Meta.fields


@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreateForm
    form = CustomUsuarioChangeForm
    model = CustomUsuario
    list_display = ('nome', 'email', 'celular','cpf', 'matricula', 'rg', 'pis', 'sexo', 'data_admissao', 'data_demissao', 'data_nascimento', 'departamento', 'cargo', 'is_staff')
    fieldsets = (
        (None, {'fields': ('cpf', 'password')}),
        ('Informações Pessoais', {
         'fields': ('nome', 'email', 'celular', 'matricula', 'rg', 'pis', 'sexo', 'data_admissao', 'data_demissao', 'data_nascimento', 'departamento', 'cargo')}),
        ('Permissões', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf', 'username', 'nome', 'password1', 'password2'),
        }),
    )
    search_fields = ('cpf', 'nome')
    ordering = ('cpf',)

@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ['nome']
@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'filial']


@admin.register(DiaDaSemana)
class DiaDaSemanaAdmin(admin.ModelAdmin):
    list_display = ['dia', 'entrada1', 'saida1', 'entrada2', 'saida2', 'folga']

@admin.register(Marcacao)
class MarcacaoAdmin(admin.ModelAdmin):
    list_display = ['colaborador', 'dia', 'marcacoes']


