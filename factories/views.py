from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Factory
from .forms import FactoryForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

# API Views
class FactoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho xí nghiệp
    """
    queryset = Factory.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from .serializers import FactorySerializer, FactoryTreeSerializer

        if self.action == 'tree':
            return FactoryTreeSerializer
        return FactorySerializer

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        Trả về cấu trúc cây xí nghiệp
        """
        # Lấy các xí nghiệp gốc (không có parent)
        root_factories = Factory.objects.filter(parent=None)

        # Sử dụng serializer để chuyển đổi thành JSON
        from .serializers import FactoryTreeSerializer
        serializer = FactoryTreeSerializer(root_factories, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def children(self, request, pk=None):
        """
        Trả về danh sách các xí nghiệp con trực tiếp
        """
        factory = self.get_object()
        children = factory.get_children()

        from .serializers import FactorySerializer
        serializer = FactorySerializer(children, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        """
        Di chuyển xí nghiệp trong cây
        """
        factory = self.get_object()
        parent_id = request.data.get('parent_id')
        position = request.data.get('position', 0)

        try:
            with transaction.atomic():
                if parent_id is None:
                    factory.move_to(None, position)
                else:
                    parent = Factory.objects.get(pk=parent_id)
                    factory.move_to(parent, position)

                factory.save()

                from .serializers import FactorySerializer
                serializer = FactorySerializer(factory)

                return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Traditional Views
class FactoryListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Factory
    template_name = 'factories/factory_list.html'
    context_object_name = 'factories'

    def get_queryset(self):
        return Factory.objects.filter(factory_type='factory')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tree_factories'] = Factory.objects.all()
        return context

class FactoryDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Factory
    template_name = 'factories/factory_detail.html'
    context_object_name = 'factory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        factory = self.get_object()

        # Lấy tất cả các đơn vị con (bao gồm cả các đơn vị con của các đơn vị con)
        descendant_factories = factory.get_descendants(include_self=True)

        # Lấy các đơn vị con trực tiếp
        context['direct_children'] = factory.get_children()

        return context

class FactoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/login/'
    model = Factory
    form_class = FactoryForm
    template_name = 'factories/factory_form.html'
    success_url = reverse_lazy('factory-list')
    permission_required = 'factories.add_factory'

    def form_valid(self, form):
        form.instance.factory_type = 'factory'  # Đảm bảo là xí nghiệp
        messages.success(self.request, f'Xí nghiệp {form.instance.name} đã được tạo thành công!')
        return super().form_valid(form)

class FactoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Factory
    form_class = FactoryForm
    template_name = 'factories/factory_form.html'
    permission_required = 'factories.change_factory'

    def get_success_url(self):
        return reverse_lazy('factory-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Xí nghiệp {form.instance.name} đã được cập nhật thành công!')
        return super().form_valid(form)

class FactoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Factory
    template_name = 'factories/factory_confirm_delete.html'
    success_url = reverse_lazy('factory-list')
    permission_required = 'factories.delete_factory'

    def delete(self, request, *args, **kwargs):
        factory = self.get_object()
        messages.success(request, f'Xí nghiệp {factory.name} đã được xóa thành công!')
        return super().delete(request, *args, **kwargs)

# API để lấy cấu trúc cây xí nghiệp
@require_http_methods(["GET"])
def get_factory_tree_json(request):
    """API để lấy cấu trúc cây xí nghiệp dưới dạng JSON"""
    try:
        # Lấy các xí nghiệp gốc (không có parent)
        root_factories = Factory.objects.filter(parent=None)

        # Hàm đệ quy để xây dựng cây
        def build_tree(factories):
            result = []
            for factory in factories:
                children = factory.get_children()
                factory_dict = {
                    'id': factory.id,
                    'name': factory.name,
                    'code': factory.code,
                    'type': factory.factory_type,
                    'children': build_tree(children) if children else []
                }
                result.append(factory_dict)
            return result

        tree_data = build_tree(root_factories)

        return JsonResponse({
            'success': True,
            'data': tree_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

# API endpoint trực tiếp cho cấu trúc cây
def factory_tree_api(request):
    """API endpoint trực tiếp cho cấu trúc cây xí nghiệp"""
    return get_factory_tree_json(request)

# API để cập nhật vị trí của factory trong cây
@require_http_methods(["POST"])
def update_factory_position(request):
    """API để cập nhật vị trí của factory trong cây xí nghiệp"""
    try:
        data = json.loads(request.body)
        factory_id = data.get('factory_id')
        parent_id = data.get('parent_id')
        position = data.get('position', 0)

        with transaction.atomic():
            factory = get_object_or_404(Factory, pk=factory_id)

            # Nếu parent_id là None, di chuyển đến level cao nhất
            if parent_id is None:
                factory.move_to(None, position)
            else:
                parent = get_object_or_404(Factory, pk=parent_id)
                factory.move_to(parent, position)

            factory.save()

        return JsonResponse({
            'success': True,
            'message': f'Đã cập nhật vị trí cho xí nghiệp {factory.name}'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
