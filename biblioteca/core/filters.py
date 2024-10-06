from django_filters import rest_framework as filters
from .models import Livro
from .models import Categoria
from .models import Autor

class LivroFilter(filters.FilterSet):
    titulo = filters.CharFilter(lookup_expr='istartswith')
    autor = filters.CharFilter(field_name='autor__nome', lookup_expr='icontains')
    categoria = filters.AllValuesFilter(field_name='categoria__nome',lookup_expr='istartswith')
    publicado_em = filters.DateFilter(field_name = 'publicado_em')

    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'categoria', 'publicado_em']

class CategoriaFilter(filters.FilterSet):
    nome = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Categoria
        fields = ['nome']

# Filtro para Autor
class AutorFilter(filters.FilterSet):
    nome = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Autor
        fields = ['nome']