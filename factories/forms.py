from django import forms
from .models import Factory

class FactoryForm(forms.ModelForm):
    class Meta:
        model = Factory
        fields = ['name', 'code', 'description', 'factory_type', 'company', 'parent', 'is_active',
                 'manager_name', 'manager_title', 'manager_email', 'manager_phone', 'location',
                 'capacity', 'established_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'established_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Lọc parent chỉ hiển thị các xí nghiệp phù hợp với ràng buộc
        instance = kwargs.get('instance')
        if instance:
            if instance.factory_type == 'division':
                # Bộ phận chỉ có thể thuộc xí nghiệp
                self.fields['parent'].queryset = Factory.objects.filter(factory_type='factory')
            elif instance.factory_type == 'team':
                # Nhóm chỉ có thể thuộc bộ phận
                self.fields['parent'].queryset = Factory.objects.filter(factory_type='division')
            else:
                # Xí nghiệp không có parent
                self.fields['parent'].queryset = Factory.objects.none()
                self.fields['parent'].widget.attrs['disabled'] = True
        
        # Thêm các class Bootstrap cho form
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
