from django.contrib import admin

from researchEngine.models import LegalDocument, CaseOutcome

class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'court', 'case_number', 'date',)
    search_fields = ('title', 'content', 'court', 'case_number')
    list_filter = ('title', 'content', 'court', 'case_number', 'date',)

    def has_delete_permission(self, request, obj=None):
        return False

    def delete_model(self, request, obj):
        raise PermissionDenied("Deletion is not allowed.")

    def delete_queryset(self, request, queryset):
        raise PermissionDenied("Bulk deletion is not allowed.")

class CaseOutcomeAdmin(admin.ModelAdmin):
    list_display = ('case__title', 'predicted_outcome', 'actual_outcome')
    search_fields = ('predicted_outcome', 'actual_outcome')
    list_filter = ('case__title', 'predicted_outcome', 'actual_outcome')

# Register your models here.
admin.site.register(LegalDocument, LegalDocumentAdmin)
admin.site.register(CaseOutcome, CaseOutcomeAdmin)
