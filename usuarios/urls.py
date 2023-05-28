from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('usuario/', include('django.contrib.auth.urls')),
    path('login/', views.login_view, name='login'),

    path('filial/', views.FilialListView.as_view(), name='filial_list'),
    path('filial/<int:pk>/', views.FilialDetailView.as_view(), name='filial_detail'),
    path('filial/new/', views.FilialCreateView.as_view(), name='filial_new'),
    path('filial/<int:pk>/edit/', views.FilialUpdateView.as_view(), name='filial_edit'),
    path('filial/<int:pk>/delete/', views.FilialDeleteView.as_view(), name='filial_delete'),

    path('departamento/', views.DepartamentoListView.as_view(), name='departamento_list'),
    path('departamento/<int:pk>/', views.DepartamentoDetailView.as_view(), name='departamento_detail'),
    path('departamento/new/', views.DepartamentoCreateView.as_view(), name='departamento_new'),
    path('departamento/<int:pk>/edit/', views.DepartamentoUpdateView.as_view(), name='departamento_edit'),
    path('departamento/<int:pk>/delete/', views.DepartamentoDeleteView.as_view(), name='departamento_delete'),

    path('colaborador/', views.ColaboradorListView.as_view(), name='colaborador_list'),
    path('colaborador/<int:pk>/', views.ColaboradorDetailView.as_view(), name='colaborador_detail'),
    path('colaborador/new/', views.ColaboradorCreateView.as_view(), name='colaborador_new'),
    path('colaborador/<int:pk>/edit/', views.ColaboradorUpdateView.as_view(), name='colaborador_edit'),
    path('colaborador/<int:pk>/delete/', views.ColaboradorDeleteView.as_view(), name='colaborador_delete'),

    path('escala/', views.EscalaListView.as_view(), name='escala_list'),
    path('escala/<int:pk>/', views.EscalaDetailView.as_view(), name='escala_detail'),
    path('escala/new/', views.EscalaCreateView.as_view(), name='escala_create'),
    path('escala/<int:pk>/edit/', views.EscalaUpdateView.as_view(), name='escala_update'),
    path('escala/<int:pk>/delete/', views.EscalaDeleteView.as_view(), name='escala_delete'),

    path('marcacao_ponto/', views.MarcacaoPontoListView.as_view(), name='marcacao_ponto_list'),
    path('marcacao_ponto/<int:pk>/', views.MarcacaoPontoDetailView.as_view(), name='marcacao_ponto_detail'),
    path('marcacao_ponto/new/', views.MarcacaoPontoCreateView.as_view(), name='marcacao_ponto_create'),
    path('marcacao_ponto/<int:pk>/edit/', views.MarcacaoPontoUpdateView.as_view(), name='marcacao_ponto_update'),
    path('marcacao_ponto/<int:pk>/delete/', views.MarcacaoPontoDeleteView.as_view(), name='marcacao_ponto_delete'),


    path('dia/', views.DiaDaSemanaListView.as_view(), name='dia_list'),
    path('dia/<int:pk>/', views.DiaDaSemanaDetailView.as_view(), name='dia_detail'),
    path('dia/new/', views.DiaDaSemanaCreateView.as_view(), name='dia_create'),
    path('dia/<int:pk>/edit/', views.DiaDaSemanaUpdateView.as_view(), name='dia_edit'),
    path('dia/<int:pk>/delete/', views.DiaDaSemanaDeleteView.as_view(), name='dia_delete'),


    path('folha/', views.FolhaDePontoListView.as_view(), name='folha_list'),
    path('folha/<int:pk>/', views.FolhaDetailView.as_view(), name='folha_detail'),
    path('folha/new/', views.FolhaDePontoCreateView.as_view(), name='folha_create'),
    path('folha/<int:pk>/edit/', views.FolhaUpdateView.as_view(), name='folha_update'),
    path('folha/<int:pk>/delete/', views.FolhaDeleteView.as_view(), name='folha_delete'),
]
