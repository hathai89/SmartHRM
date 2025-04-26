from rest_framework import serializers
from documents.models import Document, DocumentCategory, DocumentVersion

class DocumentCategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentCategory
        fields = ['id', 'name', 'code', 'description', 'parent', 'parent_name', 'is_active', 'document_count']
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
    
    def get_document_count(self, obj):
        return obj.documents.count()

class DocumentListSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'document_number', 'category', 'category_name', 
            'document_type', 'version', 'access_level', 'is_active',
            'created_by', 'created_by_name', 'approved_by', 'approved_by_name',
            'approved_at', 'effective_date', 'expiry_date', 'created_at', 'updated_at'
        ]
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None
    
    def get_approved_by_name(self, obj):
        return obj.approved_by.get_full_name() if obj.approved_by else None

class DocumentDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()
    versions = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = '__all__'
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None
    
    def get_approved_by_name(self, obj):
        return obj.approved_by.get_full_name() if obj.approved_by else None
    
    def get_versions(self, obj):
        versions = DocumentVersion.objects.filter(document=obj).order_by('-created_at')
        return DocumentVersionSerializer(versions, many=True).data

class DocumentVersionSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentVersion
        fields = '__all__'
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ['created_by', 'approved_by', 'approved_at']
    
    def create(self, validated_data):
        # Thêm người tạo
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class DocumentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ['created_by', 'document_number']
