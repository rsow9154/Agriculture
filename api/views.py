from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import HttpResponse

def home(request):
    """
    Vue pour la page d'accueil.
    """
    return HttpResponse("Bienvenue sur Agriconnect ! Accédez à la documentation Swagger : <a href='/swagger/'>ici</a>.")

class ProductListCreateView(generics.ListCreateAPIView):
    """
    get:
    Retourne la liste de tous les produits.

    post:
    Crée un nouveau produit.

    Exemple de requête :
    ```json
    {
        "name": "Tomates",
        "quantity": 100,
        "price": 2.5
    }
    ```

    Exemple de réponse :
    ```json
    {
        "id": 1,
        "name": "Tomates",
        "quantity": 100,
        "price": 2.5
    }
    ```
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filtrer les produits par nom.",
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crée un nouveau produit.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, example='Tomates'),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, example=100),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, example=2.5),
            },
        ),
        responses={
            201: openapi.Response('Produit créé', ProductSerializer),
            400: 'Requête invalide',
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OrderListCreateView(generics.ListCreateAPIView):
    """
    get:
    Retourne la liste de toutes les commandes.

    post:
    Crée une nouvelle commande.

    Exemple de requête :
    ```json
    {
        "product": 1,
        "quantity": 10
    }
    ```

    Exemple de réponse :
    ```json
    {
        "id": 1,
        "product": 1,
        "quantity": 10,
        "total_price": 25.0,
        "status": "pending"
    }
    ```
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        operation_description="Crée une nouvelle commande.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
            },
        ),
        responses={
            201: openapi.Response('Commande créée', OrderSerializer),
            400: 'Requête invalide',
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AIAdviceView(APIView):
    """
    post:
    Posez une question à l'IA pour obtenir des conseils agricoles.

    Exemple de requête :
    ```json
    {
        "question": "Comment prévenir les maladies des tomates ?"
    }
    ```

    Exemple de réponse :
    ```json
    {
        "response": "Pour prévenir les maladies des tomates, assurez-vous de..."
    }
    ```
    """

    def post(self, request):
        question = request.data.get('question')

        if not question:
            return Response(
                {"error": "Le champ 'question' est requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Configurez la clé API OpenAI
        openai.api_key = settings.OPENAI_API_KEY

        try:
            # Appel à l'API OpenAI
            response = openai.Completion.create(
                engine="text-davinci-003",  # Modèle GPT-3
                prompt=question,
                max_tokens=150,  # Limite de la longueur de la réponse
                temperature=0.7,  # Contrôle de la créativité (0 = strict, 1 = créatif)
            )

            # Extraire la réponse de l'IA
            advice = response.choices[0].text.strip()

            return Response({"response": advice}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la communication avec l'IA : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )