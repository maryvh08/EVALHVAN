import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.conf import settings
from .models import Evaluation
from .forms import EvaluationForm
from .utils.analysis import analyze_simple_format, analyze_descriptive_format
from .utils.pdf_generator import generate_simple_format_report, generate_descriptive_format_report
from .utils.utils import load_indicators, load_advice

def home(request):
    """Vista para la página de inicio"""
    return render(request, 'evaluator/home.html')

def evaluate_simple(request):
    """Vista para evaluación de formato simplificado"""
    if request.method == 'POST':
        form = EvaluationForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear una instancia pero no guardarla todavía
            evaluation = form.save(commit=False)
            evaluation.format_type = 'simple'
            
            # Guardar temporalmente el archivo
            temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', evaluation.resume_file.name)
            
            # Cargar indicadores y consejos
            indicators = load_indicators()
            advice = load_advice()
            
            # Analizar el PDF
            analysis_results = analyze_simple_format(
                temp_path, 
                evaluation.candidate_name, 
                evaluation.position, 
                evaluation.chapter,
                indicators,
                advice
            )
            
            if 'error' in analysis_results:
                messages.error(request, analysis_results['error'])
                return render(request, 'evaluator/simple.html', {'form': form})
            
            # Generar el reporte
            pdf_content, report_path = generate_simple_format_report(
                analysis_results,
                evaluation.candidate_name,
                evaluation.position,
                evaluation.chapter
            )
            
            # Actualizar y guardar la evaluación
            evaluation.report_file = os.path.relpath(report_path, settings.MEDIA_ROOT)
            evaluation.score = analysis_results['scores']['total']
            evaluation.save()
            
            messages.success(request, "Análisis completado con éxito.")
            return redirect('evaluator:view_report', pk=evaluation.pk)
    else:
        form = EvaluationForm()
    
    return render(request, 'evaluator/simple.html', {'form': form})

def evaluate_descriptive(request):
    """Vista para evaluación de formato descriptivo"""
    if request.method == 'POST':
        form = EvaluationForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear una instancia pero no guardarla todavía
            evaluation = form.save(commit=False)
            evaluation.format_type = 'descriptive'
            
            # Guardar temporalmente el archivo
            temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', evaluation.resume_file.name)
            
            # Cargar indicadores y consejos
            indicators = load_indicators()
            advice = load_advice()
            
            # Analizar el PDF
            analysis_results = analyze_descriptive_format(
                temp_path, 
                evaluation.candidate_name, 
                evaluation.position, 
                evaluation.chapter,
                indicators,
                advice
            )
            
            if 'error' in analysis_results:
                messages.error(request, analysis_results['error'])
                return render(request, 'evaluator/descriptive.html', {'form': form})
            
            # Generar el reporte
            pdf_content, report_path = generate_descriptive_format_report(
                analysis_results,
                evaluation.candidate_name,
                evaluation.position,
                evaluation.chapter
            )
            
            # Actualizar y guardar la evaluación
            evaluation.report_file = os.path.relpath(report_path, settings.MEDIA_ROOT)
            evaluation.score = analysis_results['scores']['total']
            evaluation.save()
            
            messages.success(request, "Análisis descriptivo completado con éxito.")
            return redirect('evaluator:view_report', pk=evaluation.pk)
    else:
        form = EvaluationForm()
    
    return render(request, 'evaluator/descriptive.html', {'form': form})

def view_report(request, pk):
    """Vista para ver el reporte"""
    evaluation = get_object_or_404(Evaluation, pk=pk)
    return render(request, 'evaluator/report.html', {'evaluation': evaluation})

def download_report(request, pk):
    """Vista para descargar el reporte PDF"""
    evaluation = get_object_or_404(Evaluation, pk=pk)
    if evaluation.report_file:
        file_path = os.path.join(settings.MEDIA_ROOT, str(evaluation.report_file))
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    
    messages.error(request, "No se encontró el archivo de reporte.")
    return redirect('evaluator:view_report', pk=evaluation.pk)

def evaluation_list(request):
    """Vista para listar todas las evaluaciones"""
    evaluations = Evaluation.objects.all().order_by('-created_at')
    return render(request, 'evaluator/list.html', {'evaluations': evaluations})
