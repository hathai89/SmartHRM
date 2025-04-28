from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'dept_type', 'company', 'parent', 'is_active',
                 'manager_name', 'manager_title', 'manager_email', 'manager_phone', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Lọc parent chỉ hiển thị các phòng ban phù hợp với ràng buộc
        instance = kwargs.get('instance')
        if instance:
            if instance.dept_type == 'division':
                # Bộ phận chỉ có thể thuộc phòng ban
                self.fields['parent'].queryset = Department.objects.filter(dept_type='department')
            elif instance.dept_type == 'team':
                # Nhóm chỉ có thể thuộc bộ phận
                self.fields['parent'].queryset = Department.objects.filter(dept_type='division')
            else:
                # Phòng ban không có parent
                self.fields['parent'].queryset = Department.objects.none()
                self.fields['parent'].widget.attrs['disabled'] = True
        
        # Thêm các class Bootstrap cho form
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
