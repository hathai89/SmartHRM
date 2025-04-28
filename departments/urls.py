from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Tạo router cho API
router = DefaultRouter()
router.register(r'api/departments', views.DepartmentViewSet, basename='api-departments')

urlpatterns = [
    # API URLs
    path('', include(router.urls)),
    path('api/departments/tree/', views.get_department_tree_json, name='department-tree-json'),
    path('api/departments/update-position/', views.update_department_position, name='update-department-position'),

    # Traditional URLs
    path('departments/', views.DepartmentListView.as_view(), name='department-list'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    path('departments/create/', views.DepartmentCreateView.as_view(), name='department-create'),
    path('departments/<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='department-update'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department-delete'),
    path('departments/tree/', views.department_tree_view, name='department-tree'),
    path('departments/overview/', views.department_overview, name='department-overview'),
]
