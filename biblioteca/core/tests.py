from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Colecao, Livro, Categoria, Autor

class ColecaoAPITestCase(APITestCase):
    def setUp(self):
        # Criando usuários
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        # Gerando tokens para os usuários
        self.token_user1 = Token.objects.create(user=self.user1)
        self.token_user2 = Token.objects.create(user=self.user2)

        # Criando dados para os testes
        self.categoria = Categoria.objects.create(nome="Ficção")
        self.autor = Autor.objects.create(nome="Autor Teste")
        self.livro = Livro.objects.create(
            titulo="Livro Teste",
            autor=self.autor,
            categoria=self.categoria,
            publicado_em="2023-01-01"
        )

        # Coleção associada ao user1
        self.colecao = Colecao.objects.create(
            nome="Coleção Teste",
            descricao="Descrição de teste",
            colecionador=self.user1,
        )
        self.colecao.livros.add(self.livro)

        # Endpoints
        self.colecoes_url = "/colecao/"

    def autenticar(self, token):
        """Adiciona o token no cabeçalho da requisição para autenticar o usuário."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def test_criar_colecao(self):
        """Teste de criação de uma nova coleção associada ao usuário autenticado."""
        self.autenticar(self.token_user1.key)
        data = {
            "nome": "Nova Coleção",
            "descricao": "Descrição nova",
            "livros": [self.livro.id],
        }
        response = self.client.post(self.colecoes_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["colecionador"], self.user1.id)
        self.assertEqual(Colecao.objects.filter(nome="Nova Coleção").count(), 1)

    def test_apenas_colecionador_pode_editar(self):
        """Teste para garantir que apenas o colecionador pode editar sua coleção."""
        colecao = Colecao.objects.get(nome="Coleção Teste")

        self.autenticar(self.token_user2.key)
        data = {"nome": "Coleção Editada"}
        response = self.client.patch(f"{self.colecoes_url}{colecao.pk}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.autenticar(self.token_user1.key)
        response = self.client.patch(f"{self.colecoes_url}{colecao.pk}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        colecao.refresh_from_db()
        self.assertEqual(colecao.nome, "Coleção Editada")

    def test_apenas_colecionador_pode_deletar(self):
        """Teste para garantir que apenas o colecionador pode deletar sua coleção."""
        colecao = Colecao.objects.get(nome="Coleção Teste")

        self.autenticar(self.token_user2.key)
        response = self.client.delete(f"{self.colecoes_url}{colecao.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.autenticar(self.token_user1.key)
        response = self.client.delete(f"{self.colecoes_url}{colecao.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Colecao.objects.filter(nome="Coleção Teste").count(), 0)

    def test_usuarios_nao_autenticados_nao_podem_criar_colecao(self):
        """Teste para garantir que usuários não autenticados não podem criar coleções."""
        data = {
            "nome": "Nova Coleção",
            "descricao": "Descrição nova",
            "livros": [self.livro.id],
        }
        response = self.client.post(self.colecoes_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listagem_de_colecoes_visiveis(self):
        """Teste para verificar que coleções são listadas corretamente para usuários autenticados."""
        self.autenticar(self.token_user1.key)
        response = self.client.get(self.colecoes_url)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Response data:", response.data)
        self.assertIsInstance(response.data.get('results', []), list)
        self.assertTrue(
        any(colecao.get("nome") == "Coleção Teste" for colecao in response.data.get('results', [])),
        "Coleção Teste não encontrada na resposta."
    )

