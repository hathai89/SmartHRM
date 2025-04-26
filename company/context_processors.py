from .models import Company

def company_info(request):
    """
    Context processor để cung cấp thông tin công ty cho toàn bộ templates
    """
    company = Company.get_company_info()
    return {
        'COMPANY': company,
        'SITE_NAME': company.name if company else 'SmartHRM',
        'SITE_SHORT_NAME': company.short_name if company and company.short_name else 'HRM',
        'COPYRIGHT_TEXT': f'Bản quyền thuộc về {company.name}' if company else 'Bản quyền thuộc về công ty',
    }
