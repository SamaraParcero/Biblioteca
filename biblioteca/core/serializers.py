from rest_framework import serializers
from .models import Categoria, Autor, Livro, Colecao
from django.contrib.auth.models import User 


class UserColecaoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Colecao
        fields = (
            'url',
            'name')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    colecoes = UserColecaoSerializer(
        many=True,
        read_only=True)


class CategoriaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Categoria.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nome = validated_data.get("nome", instance.nome)
        instance.save()
        return instance


class AutorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Autor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nome = validated_data.get("nome", instance.nome)
        instance.save()
        return instance


class LivroSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    titulo = serializers.CharField(max_length=200)
    autor = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all())
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    publicado_em = serializers.DateField()

    def create(self, validated_data):
        return Livro.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.titulo = validated_data.get("titulo", instance.titulo)
        instance.autor = validated_data.get("autor", instance.autor)
        instance.categoria = validated_data.get("categoria", instance.categoria)
        instance.publicado_em = validated_data.get(
            "publicado_em", instance.publicado_em
        )
        instance.save()
        return instance
    
class ColecaoSerializer(serializers.HyperlinkedModelSerializer):
    colecionador = serializers.ReadOnlyField(source="colecionador.username")
    livros = serializers.PrimaryKeyRelatedField(many=True, queryset=Livro.objects.all())

    class Meta:
        model = Colecao
        fields = ["id", "nome", "descricao", "livros", "colecionador"]

