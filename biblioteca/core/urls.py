from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.LivroList.as_view(), 
    name='livro-list'),
    path('livros/<int:pk>/', views.LivroDetail.as_view(), name='livro-detail'),
    path('categorias/', views.CategoriaList.as_view(), name='categoria-list'),
    path('categorias/<int:pk>/', views.CategoriaDetail.as_view(), name='categoria-detail'),
    path('autores/', views.AutorList.as_view(),
    name='autores-list'),
    path('autores/<int:pk>/', views.AutorDetail.as_view(), name='autor-detail'),
    path('colecao/', views.ColecaoListCreate.as_view(), name='colecao-list'),
    path('colecao/<int:pk>/', views.ColecaoDetail.as_view(), name='colecao-detail'),
    
]
