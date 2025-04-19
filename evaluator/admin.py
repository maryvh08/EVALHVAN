from django.contrib import admin
from .models import Evaluation

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'position', 'chapter', 'format_type', 'created_at', 'score')
    list_filter = ('position', 'chapter', 'format_type', 'created_at')
    search_fields = ('candidate_name', 'position', 'chapter')
    readonly_fields = ('created_at', 'score')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
