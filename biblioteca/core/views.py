from rest_framework import generics
from .models import Livro
from .models import Categoria
from .models import Autor
from .models import Colecao
from .serializers import LivroSerializer
from .serializers import CategoriaSerializer
from .serializers import AutorSerializer
from .serializers import ColecaoSerializer
from .filters import LivroFilter
from .filters import CategoriaFilter
from .filters import AutorFilter
from rest_framework import permissions
from core import custom_permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from drf_spectacular.views import SpectacularAPIView

class LivroList(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    filterset_class = LivroFilter
    name = "livro-list"
    search_fields = ("^titulo", "^categoria__nome",)
    ordering_fields = ['titulo', 'autor', 'categoria', 'publicado_em']
    

class LivroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-detail"
    
class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filterset_class = CategoriaFilter
    name = "categoria-list"
    ordering_fields = ['nome']

class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-detail"

class AutorList(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filterset_class = AutorFilter
    name = "autor-list"
    ordering_fields = ['nome']

class AutorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-detail"
    
    
class ColecaoListCreate(generics.ListCreateAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    name = "colecao-list"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
    )
    ordering_fields = ['nome']


    def perform_create(self, serializer):
        serializer.save(colecionador=self.request.user)

class ColecaoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    name = "colecao-detail"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated)
    



    

