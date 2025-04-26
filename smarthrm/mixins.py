class BreadcrumbMixin:
    """
    Mixin để thêm breadcrumbs vào class-based views
    """
    breadcrumbs = []
    
    def get_breadcrumbs(self):
        """
        Phương thức để lấy breadcrumbs, có thể được ghi đè trong các lớp con
        """
        return self.breadcrumbs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Thêm breadcrumbs vào context
        self.request.breadcrumbs = self.get_breadcrumbs()
        context['breadcrumbs'] = self.request.breadcrumbs
        return context
