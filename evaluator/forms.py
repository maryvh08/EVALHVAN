from django import forms
from .models import Evaluation

class EvaluationForm(forms.ModelForm):
    """Formulario para la carga de hojas de vida"""
    class Meta:
        model = Evaluation
        fields = ['candidate_name', 'position', 'chapter', 'resume_file', 'format_type']
        widgets = {
            'candidate_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'chapter': forms.Select(attrs={'class': 'form-select'}),
            'resume_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'format_type': forms.RadioSelect(),
        }
        labels = {
            'candidate_name': 'Nombre completo del candidato',
            'position': 'Cargo al que aspira',
            'chapter': 'Capítulo',
            'resume_file': 'Hoja de vida (PDF)',
            'format_type': 'Tipo de formato',
        }
        help_texts = {
            'resume_file': 'Solo se permiten archivos PDF',
            'format_type': 'Seleccione el formato que corresponde a su hoja de vida',
        }
