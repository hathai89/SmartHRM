class BreadcrumbMiddleware:
    """
    Middleware để cung cấp breadcrumbs cho các view
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Thêm breadcrumbs vào request
        request.breadcrumbs = []
        
        # Xử lý request
        response = self.get_response(request)
        
        return response
