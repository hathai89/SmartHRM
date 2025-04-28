from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Tạo router cho API
router = DefaultRouter()
router.register(r'api/factories', views.FactoryViewSet, basename='api-factories')

urlpatterns = [
    # API URLs
    path('', include(router.urls)),
    path('api/factories/tree/', views.get_factory_tree_json, name='factory-tree-json'),
    path('api/factories/update-position/', views.update_factory_position, name='update-factory-position'),

    # Traditional URLs
    path('factories/', views.FactoryListView.as_view(), name='factory-list'),
    path('factories/<int:pk>/', views.FactoryDetailView.as_view(), name='factory-detail'),
    path('factories/create/', views.FactoryCreateView.as_view(), name='factory-create'),
    path('factories/<int:pk>/update/', views.FactoryUpdateView.as_view(), name='factory-update'),
    path('factories/<int:pk>/delete/', views.FactoryDeleteView.as_view(), name='factory-delete'),
]
