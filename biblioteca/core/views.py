from rest_framework import generics, permissions
from .custom_permissions import IsColecionador
from rest_framework.authentication import TokenAuthentication
from .models import Colecao, Livro, Categoria, Autor
from .serializers import ColecaoSerializer, LivroSerializer, CategoriaSerializer, AutorSerializer
from .filters import LivroFilter, CategoriaFilter, AutorFilter

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
    authentication_classes = [TokenAuthentication]  
    permission_classes = [permissions.IsAuthenticated]  
    ordering_fields = ['nome']

    def perform_create(self, serializer):
        serializer.save(colecionador=self.request.user)

class ColecaoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    name = "colecao-detail"
    authentication_classes = [TokenAuthentication] 
    permission_classes = [permissions.IsAuthenticated, IsColecionador]



    

