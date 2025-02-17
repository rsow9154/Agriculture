from rest_framework import serializers
from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(help_text="Nom du produit, par exemple : Tomates")
    quantity = serializers.IntegerField(help_text="Quantité disponible, par exemple : 100")
    price = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Prix unitaire, par exemple : 2.5")

    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), help_text="ID du produit commandé, par exemple : 1")
    quantity = serializers.IntegerField(help_text="Quantité commandée, par exemple : 10")
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, help_text="Prix total calculé automatiquement")
    status = serializers.CharField(read_only=True, help_text="Statut de la commande, par exemple : pending")

    class Meta:
        model = Order
        fields = '__all__'