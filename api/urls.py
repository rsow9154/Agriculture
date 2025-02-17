from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateView.as_view(), name='product-list'),
    path('orders/', views.OrderListCreateView.as_view(), name='order-list'),
    path('ai/advice/', views.AIAdviceView.as_view(), name='ai-advice'),  # Nouvelle route pour l'IA
]