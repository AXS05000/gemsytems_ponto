from datetime import date, datetime, timedelta

import pytz
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

tz = pytz.timezone('America/Sao_Paulo')

class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, cpf, password, **extra_fields):
        if not cpf:
            raise ValueError('O CPF é obrigatório')
        user = self.model(cpf=cpf, username=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(cpf, password, **extra_fields)

    def create_superuser(self, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff True')

        return self.create_user(cpf, password, **extra_fields)


class Filial(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'

class Departamento(models.Model):
    nome = models.CharField(max_length=100)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome}'
    

class CustomUsuario(AbstractUser):
    SEXO = [
        ('m', 'Masculino'),
        ('f', 'Feminino'),
        ('outros', 'Outros'),
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField('E-mail', unique=True)
    celular = models.CharField('Celular', max_length=15)
    cpf = models.CharField(max_length=11, unique=True)
    matricula = models.IntegerField(unique=True)
    rg = models.CharField(max_length=18)
    pis = models.DecimalField(null=True, blank=True, max_digits=25, decimal_places=0)
    cargo = models.CharField(max_length=100)
    sexo = models.CharField(max_length=50, choices=SEXO)
    data_admissao = models.DateField(null=True, blank=True)
    data_demissao = models.DateField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
    is_staff = models.BooleanField('Membro da equipe', default=False)
    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome', 'email', 'matricula']

    def __str__(self):
        return f'{self.nome}'

    objects = UsuarioManager()




###################################################################################################

class DiaDaSemana(models.Model):
    DIA_ESCOLHAS = (
        ('Segunda', 'Segunda-feira'),
        ('Terca', 'Terça-feira'),
        ('Quarta', 'Quarta-feira'),
        ('Quinta', 'Quinta-feira'),
        ('Sexta', 'Sexta-feira'),
        ('Sabado', 'Sábado'),
        ('Domingo', 'Domingo'),
    )
    dia = models.CharField(max_length=10, choices=DIA_ESCOLHAS)
    entrada1 = models.TimeField(null=True, blank=True)
    saida1 = models.TimeField(null=True, blank=True)
    entrada2 = models.TimeField(null=True, blank=True)
    saida2 = models.TimeField(null=True, blank=True)
    folga = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.dia} - {self.entrada1} - {self.saida1} - {self.entrada2} - {self.saida2}'

class EscalaSemanal(models.Model):
    nome = models.CharField(max_length=100)
    dias = models.ManyToManyField(DiaDaSemana)


class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    escala_semanal = models.ForeignKey(EscalaSemanal, on_delete=models.CASCADE)


class Marcacao(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    dia = models.DateField()
    marcacoes = models.TimeField()


class FolhaDePonto(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    mes = models.PositiveSmallIntegerField()
    ano = models.PositiveSmallIntegerField()
    marcacoes = models.ManyToManyField(Marcacao)

    def calcular_horas(self, dia):
        marcacoes = self.marcacoes.filter(dia=dia).order_by('marcacoes')
        marcacoes_list = [m.marcacoes for m in marcacoes]
        dia_semana = dia.strftime('%A')
        dia_escala = self.colaborador.escala_semanal.dias.get(dia=dia_semana)

        horas_esperadas = (datetime.combine(datetime.now(tz).date(), dia_escala.saida2 or dia_escala.saida1) - datetime.combine(datetime.now(tz).date(), dia_escala.entrada1)).seconds / 3600
        horas_trabalhadas = 0
        atrasadas = 0
        extras = 0

        if len(marcacoes_list) == 1:
            return {'esperadas': timedelta(hours=horas_esperadas), 'trabalhadas': timedelta(hours=0), 'extras': timedelta(hours=0), 'atrasadas': timedelta(hours=horas_esperadas), 'evento': 'Falta Injustificada'}

        if len(marcacoes_list) >= 2:
            intervalo1 = (datetime.combine(date.today(), marcacoes_list[1]) - datetime.combine(date.today(), marcacoes_list[0])).seconds / 3600
            horas_trabalhadas += intervalo1
            if (datetime.combine(date.today(), marcacoes_list[0]) - datetime.combine(date.today(), dia_escala.entrada1)).seconds / 3600 > 0.083333:
                atrasadas += (datetime.combine(date.today(), marcacoes_list[0]) - datetime.combine(date.today(), dia_escala.entrada1)).seconds / 3600
            if len(marcacoes_list) == 2:
                atrasadas += (dia_escala.saida2 - dia_escala.entrada2).seconds / 3600

        if len(marcacoes_list) == 3:
            intervalo1 = (datetime.combine(date.today(), marcacoes_list[1]) - datetime.combine(date.today(), marcacoes_list[0])).seconds / 3600
            horas_trabalhadas = intervalo1
            if (datetime.combine(date.today(), marcacoes_list[2]) - datetime.combine(date.today(), dia_escala.entrada2)).seconds / 3600 > 0.083333:
                atrasadas += (datetime.combine(date.today(), marcacoes_list[2]) - datetime.combine(date.today(), dia_escala.entrada2)).seconds / 3600
            atrasadas += (dia_escala.saida2 - dia_escala.entrada2).seconds / 3600

        if len(marcacoes_list) >= 4:
            intervalo2 = (datetime.combine(date.today(), marcacoes_list[3]) - datetime.combine(date.today(), marcacoes_list[2])).seconds / 3600
            horas_trabalhadas += intervalo2
            if (datetime.combine(date.today(), marcacoes_list[2]) - datetime.combine(date.today(), dia_escala.entrada2)).seconds / 3600 > 0.083333:
                atrasadas += (datetime.combine(date.today(), marcacoes_list[2]) - datetime.combine(date.today(), dia_escala.entrada2)).seconds / 3600
            elif intervalo2 > (dia_escala.saida2 - dia_escala.entrada2).seconds / 3600:
                extras += intervalo2 - (dia_escala.saida2 - dia_escala.entrada2).seconds / 3600

        return {'esperadas': timedelta(hours=horas_esperadas), 'trabalhadas': timedelta(hours=horas_trabalhadas), 'extras': timedelta(hours=extras), 'atrasadas': timedelta(hours=atrasadas)}


    