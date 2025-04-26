from django import forms
from .models import Employee, JobTitle
from departments.models import Department
from factories.models import Factory

class EmployeeForm(forms.ModelForm):
    """
    Form cho nhân viên
    """
    class Meta:
        model = Employee
        fields = [
            'first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'phone_number',
            'avatar', 'job_title', 'join_date', 'workplace_type', 'department', 'factory',
            'permanent_address', 'current_address', 'id_card_number', 'id_card_issue_date',
            'id_card_issue_place', 'id_card_front_image', 'id_card_back_image'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'join_date': forms.DateInput(attrs={'type': 'date'}),
            'id_card_issue_date': forms.DateInput(attrs={'type': 'date'}),
            'permanent_address': forms.Textarea(attrs={'rows': 3}),
            'current_address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Thêm class Bootstrap cho các trường
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Lọc các phòng ban và xí nghiệp đang hoạt động
        self.fields['department'].queryset = Department.objects.filter(is_active=True)
        self.fields['factory'].queryset = Factory.objects.filter(is_active=True)
        
        # Lọc các chức danh đang hoạt động
        self.fields['job_title'].queryset = JobTitle.objects.filter(is_active=True)
        
        # Thêm JavaScript để hiển thị/ẩn phòng ban hoặc xí nghiệp dựa trên workplace_type
        self.fields['workplace_type'].widget.attrs['onchange'] = 'toggleWorkplaceFields()'
    
    def clean(self):
        cleaned_data = super().clean()
        workplace_type = cleaned_data.get('workplace_type')
        department = cleaned_data.get('department')
        factory = cleaned_data.get('factory')
        
        # Kiểm tra ràng buộc: Nếu workplace_type là department thì phải chọn department
        if workplace_type == 'department' and not department:
            self.add_error('department', 'Vui lòng chọn phòng ban.')
        
        # Kiểm tra ràng buộc: Nếu workplace_type là factory thì phải chọn factory
        if workplace_type == 'factory' and not factory:
            self.add_error('factory', 'Vui lòng chọn xí nghiệp.')
        
        return cleaned_data
