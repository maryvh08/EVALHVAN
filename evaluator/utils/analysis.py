import os
import re
import fitz
from spellchecker import SpellChecker
from textstat import textstat
from django.conf import settings
from .utils import (
    extract_text_with_ocr, extract_cleaned_lines, calculate_similarity,
    calculate_word_repetition, calculate_sentence_fluency
)

# FUNCIONES PARA ANÁLISIS DE FORMATO SIMPLIFICADO

def extract_profile_section_with_ocr(pdf_path):
    """Extrae la sección 'Perfil' de un archivo PDF"""
    text = extract_text_with_ocr(pdf_path)

    if not text or len(text.strip()) == 0:
        return ""

    # Palabras clave para identificar el inicio y fin de la sección
    start_keyword = "Perfil"
    end_keywords = [
        "Asistencia a eventos",
        "Actualización profesional",
    ]

    # Buscar la palabra clave de inicio
    start_idx = text.lower().find(start_keyword.lower())
    if start_idx == -1:
        return ""

    # Encontrar el índice más cercano de las palabras clave de fin
    end_idx = len(text)
    for keyword in end_keywords:
        idx = text.lower().find(keyword.lower(), start_idx)
        if idx != -1:
            end_idx = min(end_idx, idx)

    # Extraer la sección entre inicio y fin
    candidate_profile_text = text[start_idx:end_idx].strip()

    # Depuración del texto extraído
    cleaned_profile_text = re.sub(r"[^\w\s.,;:()\-]", "", candidate_profile_text)  # Mantiene paréntesis y guiones
    cleaned_profile_text = re.sub(r"\s+", " ", cleaned_profile_text)  # Normaliza espacios

    return cleaned_profile_text
    
def extract_experience_section_with_ocr(pdf_path):
    """Extrae la sección 'EXPERIENCIA EN ANEIAP' de un archivo PDF"""
    text = extract_text_with_ocr(pdf_path)

    # Palabras clave para identificar inicio y fin de la sección
    start_keyword = "EXPERIENCIA EN ANEIAP"
    end_keywords = [
        "EVENTOS ORGANIZADOS",
        "Reconocimientos individuales",
        "Reconocimientos grupales",
        "Reconocimientos",
    ]

    # Encontrar índice de inicio
    start_idx = text.lower().find(start_keyword.lower())
    if start_idx == -1:
        return None  # No se encontró la sección

    # Encontrar índice más cercano de fin basado en palabras clave
    end_idx = len(text)  # Por defecto, tomar hasta el final
    for keyword in end_keywords:
        idx = text.lower().find(keyword.lower(), start_idx)
        if idx != -1:
            end_idx = min(end_idx, idx)

    # Extraer la sección entre inicio y fin
    experience_text = text[start_idx:end_idx].strip()

    # Filtrar y limpiar texto
    exclude_lines = [
        "a nivel capitular",
        "a nivel nacional",
        "a nivel seccional",
        "reconocimientos individuales",
        "reconocimientos grupales",
        "trabajo capitular",
        "trabajo nacional",
        "nacional 2024",
        "nacional 20212023",
    ]
    experience_lines = experience_text.split("\n")
    cleaned_lines = []
    for line in experience_lines:
        line = line.strip()
        line = re.sub(r"[^\w\s]", "", line)  # Eliminar caracteres no alfanuméricos excepto espacios
        normalized_line = re.sub(r"\s+", " ", line).lower()  # Normalizar espacios y convertir a minúsculas
        if (
            normalized_line
            and normalized_line not in exclude_lines
            and normalized_line != start_keyword.lower()
            and normalized_line not in [kw.lower() for kw in end_keywords]
        ):
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

def extract_event_section_with_ocr(pdf_path):
    """Extrae la sección 'EVENTOS ORGANIZADOS' de un archivo PDF"""
    text = extract_text_with_ocr(pdf_path)
    if not text:
        return []  # Retorna lista vacía si no hay contenido

    # Palabras clave para identificar inicio y fin de la sección
    start_keyword = "EVENTOS ORGANIZADOS"
    end_keywords = [
        "EXPERIENCIA LABORAL",
        "FIRMA",
    ]

    # Encontrar índice de inicio
    start_idx = text.lower().find(start_keyword.lower())
    if start_idx == -1:
        return None  # No se encontró la sección

    # Encontrar índice más cercano de fin basado en palabras clave
    end_idx = len(text)  # Por defecto, tomar hasta el final
    for keyword in end_keywords:
        idx = text.lower().find(keyword.lower(), start_idx)
        if idx != -1:
            end_idx = min(end_idx, idx)

    # Extraer la sección entre inicio y fin
    org_text = text[start_idx:end_idx].strip()
    
    # Filtrar y limpiar texto
    exclude_lines = [
        "a nivel capitular",
        "a nivel nacional",
        "a nivel seccional",
        "reconocimientos individuales",
        "reconocimientos grupales",
        "trabajo capitular",
        "trabajo nacional",
        "nacional 2024",
        "nacional 20212023",
    ]
    org_lines = org_text.split("\n")
    cleaned_lines = []
    for line in org_lines:
        line = line.strip()
        line = re.sub(r"[^\w\s]", "", line)  # Eliminar caracteres no alfanuméricos excepto espacios
        normalized_line = re.sub(r"\s+", " ", line).lower()  # Normalizar espacios y convertir a minúsculas
        if (
            normalized_line
            and normalized_line not in exclude_lines
            and normalized_line != start_keyword.lower()
            and normalized_line not in [kw.lower() for kw in end_keywords]
        ):
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

def extract_attendance_section_with_ocr(pdf_path):
  """Extrae la sección 'Asistencia Eventos ANEIAP' de un archivo PDF"""
  text = extract_text_with_ocr(pdf_path)

  # Palabras clave para identificar inicio y fin de la sección
  start_keyword = "ASISTENCIA A EVENTOS ANEIAP"
  end_keywords = [
      "ACTUALIZACIÓN PROFESIONAL",
      "EXPERIENCIA EN ANEIAP",
      "EVENTOS ORGANIZADOS",
      "RECONOCIMIENTOS",
    ]
  # Encontrar índice de inicio
  start_idx = text.lower().find(start_keyword.lower())
  if start_idx == -1:
      return None  # No se encontró la sección
  
  # Encontrar índice más cercano de fin basado en palabras clave
  end_idx = len(text)  # Por defecto, tomar hasta el final
  for keyword in end_keywords:
      idx = text.lower().find(keyword.lower(), start_idx)
      if idx != -1:
          end_idx = min(end_idx, idx)
  
  # Extraer la sección entre inicio y fin
  att_text = text[start_idx:end_idx].strip()
  
  # Filtrar y limpiar texto
  att_exclude_lines = [
      "a nivel capitular",
      "a nivel nacional",
      "a nivel seccional",
      "capitular",
      "seccional",
      "nacional",
  ]
  att_lines = att_text.split("\n")
  att_cleaned_lines = []
  for line in att_lines:
      line = line.strip()
      line = re.sub(r"[^\w\s]", "", line)  # Eliminar caracteres no alfanuméricos excepto espacios
      normalized_att_line = re.sub(r"\s+", " ", line).lower()  # Normalizar espacios y convertir a minúsculas
      if (
          normalized_att_line
          and normalized_att_line not in att_exclude_lines
          and normalized_att_line != start_keyword.lower()
          and normalized_att_line not in [kw.lower() for kw in end_keywords]
      ):
          att_cleaned_lines.append(line)
  
  return "\n".join(att_cleaned_lines)

def evaluate_cv_presentation(pdf_path):
    """
    Evalúa la presentación de la hoja de vida en términos de redacción, ortografía,
    coherencia básica, y claridad.
    """
    # Extraer texto completo de la hoja de vida
    resume_text = extract_text_with_ocr(pdf_path)

    if not resume_text:
        return None, "No se pudo extraer el texto de la hoja de vida."

    # Limpiar y filtrar texto
    pres_cleaned_lines = []
    lines = resume_text.split("\n")
    for line in lines:
        line = line.strip()
        line = re.sub(r"[^\w\s.,;:!?-]", "", line)  # Eliminar caracteres no alfanuméricos excepto signos básicos
        line = re.sub(r"\s+", " ", line)  # Normalizar espacios
        if line:
            pres_cleaned_lines.append(line)

    # Evaluación de calidad de presentación
    total_lines = len(pres_cleaned_lines)
    if total_lines == 0:
        return None, "El documento está vacío o no contiene texto procesable."
        
    return "\n".join(pres_cleaned_lines)

def calculate_all_indicators(lines, position_indicators):
    """
    Calcula los porcentajes de todos los indicadores para un cargo.
    """
    total_lines = len(lines)
    if total_lines == 0:
        return {indicator: 0 for indicator in position_indicators}  # Evitar división por cero

    indicator_results = {}
    for indicator, keywords in position_indicators.items():
        relevant_lines = sum(
            any(keyword.lower() in line.lower() for keyword in keywords) for line in lines
        )
        indicator_results[indicator] = (relevant_lines / total_lines) * 100  # Cálculo del porcentaje
    return indicator_results

def calculate_indicators_for_report(lines, position_indicators):
    """
    Calcula los porcentajes de relevancia de indicadores para el reporte.
    """
    total_lines = len(lines)
    if total_lines == 0:
        return {indicator: {"percentage": 0, "relevant_lines": 0} for indicator in position_indicators}

    indicator_results = {}
    for indicator, keywords in position_indicators.items():
        relevant_lines = sum(
            any(keyword.lower() in line.lower() for keyword in keywords) for line in lines
        )
        percentage = (relevant_lines / total_lines) * 100
        indicator_results[indicator] = {"percentage": percentage, "relevant_lines": relevant_lines}

    return indicator_results

# FUNCIONES PARA ANÁLISIS DE FORMATO DESCRIPTIVO

def extract_text_with_headers_and_details(pdf_path):
    """
    Extrae encabezados (en negrita) y detalles del texto de un archivo PDF.
    """
    items = {}
    current_header = None

    with fitz.open(pdf_path) as doc:
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue

                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue

                        # Detectar encabezados (negrita)
                        if "bold" in span["font"].lower() and not text.startswith("-"):
                            current_header = text
                            items[current_header] = []
                        elif current_header:
                            # Agregar detalles al encabezado actual
                            items[current_header].append(text)

    return items

def extract_experience_items_with_details(pdf_path):
    """
    Extrae encabezados (en negrita) y sus detalles de la sección 'EXPERIENCIA EN ANEIAP'.
    """
    items = {}
    current_item = None
    in_experience_section = False

    with fitz.open(pdf_path) as doc:
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue

                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue

                        # Detectar inicio y fin de la sección
                        if "experiencia en aneiap" in text.lower():
                            in_experience_section = True
                            continue
                        elif any(key in text.lower() for key in ["reconocimientos", "eventos organizados"]):
                            in_experience_section = False
                            break

                        if not in_experience_section:
                            continue

                        # Detectar encabezados (negrita) y detalles
                        if "bold" in span["font"].lower() and not text.startswith("-"):
                            current_item = text
                            items[current_item] = []
                        elif current_item:
                            items[current_item].append(text)

    return items

def extract_event_items_with_details(pdf_path):
    """
    Extrae encabezados (en negrita) y sus detalles de la sección 'EVENTOS ORGANIZADOS'.
    """
    items = {}
    current_item = None
    in_eventos_section = False

    with fitz.open(pdf_path) as doc:
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue

                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue

                        # Detectar inicio y fin de la sección
                        if "eventos organizados" in text.lower():
                            in_eventos_section = True
                            continue
                        elif any(key in text.lower() for key in ["firma", "experiencia laboral"]):
                            in_eventos_section = False
                            break

                        if not in_eventos_section:
                            continue

                        # Detectar encabezados (negrita) y detalles
                        if "bold" in span["font"].lower() and not text.startswith("-"):
                            current_item = text
                            items[current_item] = []
                        elif current_item:
                            items[current_item].append(text)

    return items

def extract_asistencia_items_with_details(pdf_path):
    """
    Extrae encabezados (en negrita) y sus detalles de la sección 'Asistencia a eventos ANEIAP'.
    """
    items = {}
    current_item = None
    in_asistencia_section = False
    excluded_terms = {
        "dirección de residencia:",
        "tiempo en aneiap:",
        "medios de comunicación:"
    }

    with fitz.open(pdf_path) as doc:
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue

                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        text_lower = text.lower()  # Solo para comparación

                        if not text or text_lower in excluded_terms:
                            continue

                        # Detectar inicio y fin de la sección
                        if "asistencia a eventos aneiap" in text_lower:
                            in_asistencia_section = True
                            continue
                        elif any(key in text_lower for key in ["actualización profesional", "firma"]):
                            in_asistencia_section = False
                            break

                        if not in_asistencia_section:
                            continue

                        # Detectar encabezados (negrita) y detalles
                        if "bold" in span["font"].lower() and not text.startswith("-"):
                            current_item = text  # Se mantiene el formato original
                            items[current_item] = []
                        elif current_item:
                            items[current_item].append(text)  # Se mantiene el formato original

    return items

def extract_profile_section_with_details(pdf_path):
    """
    Extrae la sección 'Perfil' de un archivo PDF
    """
    try:
        candidate_profile_text = ""
        in_profile_section = False

        with fitz.open(pdf_path) as doc:
            for page in doc:
                blocks = page.get_text("dict")["blocks"]
                for block in blocks:
                    if "lines" not in block:
                        continue

                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if not text:
                                continue

                            # Detectar inicio y fin de la sección
                            if "perfil" in text.lower():
                                in_profile_section = True
                                continue
                            elif any(key in text.lower() for key in ["asistencia a eventos aneiap", "actualización profesional"]):
                                in_profile_section = False
                                break

                            if in_profile_section:
                                candidate_profile_text += text + " "

        return candidate_profile_text.strip()
    
    except Exception:
        return ""

def evaluate_cv_presentation_with_headers(pdf_path):
    """
    Evalúa la presentación de la hoja de vida en términos de redacción, ortografía,
    coherencia básica, y claridad, considerando encabezados y detalles.
    """
    # Cargar texto del PDF
    text = extract_text_with_ocr(pdf_path)

    if not text:
        return None, "No se pudo extraer texto del archivo PDF."

    # Instanciar SpellChecker
    spell = SpellChecker(language='es')

    # Función para evaluar ortografía
    def evaluate_spelling(text):
        """Evalúa la ortografía del texto y retorna un puntaje entre 0 y 100."""
        if not text or not isinstance(text, str):
            return 100  # Si no hay texto, asumimos puntaje perfecto
    
        words = text.split()
        if len(words) < 2:
            return 100  # Evitar dividir por 0 si hay muy pocas palabras
    
        misspelled = spell.unknown(words)
        total_words = len(words)
    
        return round(((total_words - len(misspelled)) / total_words) * 100, 2)

    # Función para evaluar capitalización
    def evaluate_capitalization(text):
        sentences = re.split(r'[.!?]\s*', text.strip())  # Dividir en oraciones usando signos de puntuación
        sentences = [sentence for sentence in sentences if sentence]  # Filtrar oraciones vacías
        correct_caps = sum(1 for sentence in sentences if sentence and sentence[0].isupper())
        if not sentences:
            return 100  # Si no hay oraciones, asumimos puntaje perfecto
        return (correct_caps / len(sentences)) * 100

    # Función para evaluar coherencia de las frases
    def evaluate_sentence_coherence(text):
        try:
            return max(0, min(100, 100 - textstat.flesch_kincaid_grade(text) * 10))  # Normalizar entre 0 y 100
        except Exception:
            return 50  # Puntaje intermedio en caso de error

    # Calcular métricas
    spelling_score = evaluate_spelling(text)
    capitalization_score = evaluate_capitalization(text)
    coherence_score = evaluate_sentence_coherence(text)
    overall_score = (spelling_score + capitalization_score + coherence_score) / 3
    
    return {
        "spelling_score": spelling_score,
        "capitalization_score": capitalization_score,
        "coherence_score": coherence_score,
        "overall_score": overall_score,
    }

# Funciones principales de análisis

def analyze_simple_format(pdf_path, candidate_name, position, chapter, indicators, advice):
    """
    Función principal para analizar hojas de vida en formato simplificado
    """
    # Extraer secciones
    profile_text = extract_profile_section_with_ocr(pdf_path)
    experience_text = extract_experience_section_with_ocr(pdf_path)
    event_text = extract_event_section_with_ocr(pdf_path)
    attendance_text = extract_attendance_section_with_ocr(pdf_path)
    resume_text = evaluate_cv_presentation(pdf_path)
    
    # Validar extracciones
    if not profile_text:
        return {'error': "No se encontró la sección 'Perfil' en el PDF."}
    if not experience_text:
        return {'error': "No se encontró la sección 'EXPERIENCIA EN ANEIAP' en el PDF."}
    if not event_text:
        return {'error': "No se encontró la sección 'EVENTOS ORGANIZADOS' en el PDF."}
    if not attendance_text:
        return {'error': "No se encontró la sección 'Asistencia a Eventos ANEIAP' en el PDF."}
    if not resume_text:
        return {'error': "No se pudo extraer el texto de la hoja de vida."}
    
    # Obtener indicadores para el cargo y capítulo
    position_indicators = indicators.get(chapter, {}).get(position, {})
    if not position_indicators:
        return {'error': f"No se encontraron indicadores para el cargo {position} en el capítulo {chapter}."}
    
    # Cargar funciones y perfil
    try:
        func_path = os.path.join(settings.DATA_DIR, 'Funciones', f"F{position}.pdf")
        profile_path = os.path.join(settings.DATA_DIR, 'Perfiles', f"P{position}.pdf")
        
        with fitz.open(func_path) as func_doc:
            functions_text = func_doc[0].get_text()
        with fitz.open(profile_path) as profile_doc:
            profile_text_cargo = profile_doc[0].get_text()
    except Exception as e:
        return {'error': f"Error al cargar funciones o perfil: {e}"}
    
    # Análisis detallado
    analysis_results = perform_detailed_analysis(
        experience_text, event_text, attendance_text, profile_text, resume_text,
        position_indicators, functions_text, profile_text_cargo
    )
    
    return analysis_results

def analyze_descriptive_format(pdf_path, candidate_name, position, chapter, indicators, advice):
    """
    Función principal para analizar hojas de vida en formato descriptivo
    """
    # Extraer secciones
    profile_text = extract_profile_section_with_details(pdf_path)
    experience_items = extract_experience_items_with_details(pdf_path)
    event_items = extract_event_items_with_details(pdf_path)
    attendance_items = extract_asistencia_items_with_details(pdf_path)
    presentation_results = evaluate_cv_presentation_with_headers(pdf_path)
    
    # Validar extracciones
    if not profile_text:
        return {'error': "No se encontró la sección 'Perfil' en el PDF."}
    if not experience_items:
        return {'error': "No se encontraron encabezados y detalles de experiencia para analizar."}
    if not event_items:
        return {'error': "No se encontraron encabezados y detalles de eventos para analizar."}
    if not attendance_items:
        return {'error': "No se encontraron encabezados y detalles de asistencias para analizar."}
    
    # Obtener indicadores para el cargo y capítulo
    position_indicators = indicators.get(chapter, {}).get(position, {})
    if not position_indicators:
        return {'error': f"No se encontraron indicadores para el cargo {position} en el capítulo {chapter}."}
    
    # Cargar funciones y perfil
    try:
        func_path = os.path.join(settings.DATA_DIR, 'Funciones', f"F{position}.pdf")
        profile_path = os.path.join(settings.DATA_DIR, 'Perfiles', f"P{position}.pdf")
        
        with fitz.open(func_path) as func_doc:
            functions_text = func_doc[0].get_text()
        with fitz.open(profile_path) as profile_doc:
            profile_text_cargo = profile_doc[0].get_text()
    except Exception as e:
        return {'error': f"Error al cargar funciones o perfil: {e}"}
    
    # Análisis con formato descriptivo
    analysis_results = perform_descriptive_analysis(
        experience_items, event_items, attendance_items, profile_text, presentation_results,
        position_indicators, functions_text, profile_text_cargo
    )
    
    return analysis_results

def perform_detailed_analysis(experience_text, event_text, attendance_text, profile_text, resume_text, 
                             position_indicators, functions_text, profile_text_cargo):
    """Realizar análisis detallado de las secciones en formato simplificado"""
    # Dividir texto en líneas
    experience_lines = experience_text.split("\n")
    experience_lines = [line.strip() for line in experience_lines if line.strip()]
    
    event_lines = event_text.split("\n")
    event_lines = [line.strip() for line in event_lines if line.strip()]
    
    attendance_lines = attendance_text.split("\n")
    attendance_lines = [line.strip() for line in attendance_lines if line.strip()]
    
    # Inicializar resultados
    results = {
        'experience': [],
        'events': [],
        'attendance': [],
        'profile': {'func_match': 0, 'profile_match': 0},
        'presentation': {},
        'indicators': {},
        'scores': {}
    }
    
    # Analizar indicadores
    indicator_results = calculate_indicators_for_report(experience_lines, position_indicators)
    results['indicators'] = indicator_results
    
    # Evaluar experiencia
    for line in experience_lines:
        if not line:
            continue
        
        if any(keyword.lower() in line.lower() for kw_set in position_indicators.values() for keyword in kw_set):
            func_match = 100.0
            profile_match = 100.0
        else:
            func_match = calculate_similarity(line, functions_text)
            profile_match = calculate_similarity(line, profile_text_cargo)
        
        if func_match > 0 or profile_match > 0:
            results['experience'].append({'line': line, 'func_match': func_match, 'profile_match': profile_match})
    
    # Evaluar eventos organizados
    for line in event_lines:
        if not line:
            continue
        
        if any(keyword.lower() in line.lower() for kw_set in position_indicators.values() for keyword in kw_set):
            func_match = 100.0
            profile_match = 100.0
        else:
            func_match = calculate_similarity(line, functions_text)
            profile_match = calculate_similarity(line, profile_text_cargo)
        
        if func_match > 0 or profile_match > 0:
            results['events'].append({'line': line, 'func_match': func_match, 'profile_match': profile_match})
    
    # Evaluar asistencia a eventos
    for line in attendance_lines:
        if not line:
            continue
        
        if any(keyword.lower() in line.lower() for kw_set in position_indicators.values() for keyword in kw_set):
            func_match = 100.0
            profile_match = 100.0
        else:
            func_match = calculate_similarity(line, functions_text)
            profile_match = calculate_similarity(line, profile_text_cargo)
        
        if func_match > 0 or profile_match > 0:
            results['attendance'].append({'line': line, 'func_match': func_match, 'profile_match': profile_match})
    
    # Evaluar perfil
    keyword_count = 0
    words = re.findall(r"\b\w+\b", profile_text)
    total_words = len(words)
    for kw_set in position_indicators.values():
        for keyword in kw_set:
            keyword_count += profile_text.lower().count(keyword.lower())
    
    prop_keyword = keyword_count/total_words if total_words > 0 else 0
    
    if prop_keyword <= 0.01:
        keyword_match_percentage = 0
    elif 0.01 < prop_keyword <= 0.15:
        keyword_match_percentage = 25
    elif 0.15 < prop_keyword <= 0.5:
        keyword_match_percentage = 50
    elif 0.5 < prop_keyword <= 0.75:
        keyword_match_percentage = 75
    else:
        keyword_match_percentage = 100
    
    if keyword_match_percentage == 100:
        results['profile']['func_match'] = 100.0
        results['profile']['profile_match'] = 100.0
    else:
        prof_func_match = calculate_similarity(profile_text, functions_text)
        prof_profile_match = calculate_similarity(profile_text, profile_text_cargo)
        results['profile']['func_match'] = keyword_match_percentage + prof_func_match
        results['profile']['profile_match'] = keyword_match_percentage + prof_profile_match
    
    # Evaluar presentación
    spell = SpellChecker(language='es')
    
    # Limpiar y dividir el texto en líneas
    pres_cleaned_lines = [line.strip() for line in resume_text.split("\n") if line.strip()]
    total_lines = len(pres_cleaned_lines)
    
    # Métricas
    total_words = 0
    spelling_errors = 0
    missing_capitalization = 0
    incomplete_sentences = 0
    grammar_errors = 0
    
    for line in pres_cleaned_lines:
        # Dividir en palabras y contar
        words = re.findall(r'\b\w+\b', line)
        total_words += len(words)
        
        # Ortografía
        misspelled = spell.unknown(words)
        spelling_errors += len(misspelled)
        
        # Verificar capitalización
        if line and not line[0].isupper():
            missing_capitalization += 1
        
        # Verificar que termine en signo de puntuación
        if not line.endswith((".", "!", "?", ":", ";")):
            incomplete_sentences += 1
        
        # Gramática básica
        grammar_errors += len(re.findall(r'\b(?:es|está|son)\b [^\w\s]', line))
    
    # Calcular métricas secundarias
    spelling = 1 - (spelling_errors / total_words) if total_words > 0 else 1
    capitalization_score = 1 - (missing_capitalization / total_lines) if total_lines > 0 else 1
    sentence_completion_score = 1 - (incomplete_sentences / total_lines) if total_lines > 0 else 1
    grammar = 1 - (grammar_errors / total_lines) if total_lines > 0 else 1
    
    # Calcular métricas principales
    grammar_score = ((sentence_completion_score + grammar) / 2) * 5
    spelling_score = ((spelling + capitalization_score) / 2) * 5
    
    # Calcular coherencia
    rep_score, _ = calculate_word_repetition(pres_cleaned_lines)
    fluency_score = calculate_sentence_fluency(pres_cleaned_lines)
    coherence_score = min(5, (rep_score + fluency_score) * 2.5)
    
    # Puntaje general
    overall_score = (spelling_score + coherence_score + grammar_score) / 3
    
    results['presentation'] = {
        'spelling_score': spelling_score,
        'grammar_score': grammar_score,
        'coherence_score': coherence_score,
        'overall_score': overall_score
    }
    
    # Calcular puntajes parciales
    exp_func_sum = sum(item['func_match'] for item in results['experience']) if results['experience'] else 0
    exp_profile_sum = sum(item['profile_match'] for item in results['experience']) if results['experience'] else 0
    exp_count = len(results['experience']) if results['experience'] else 1
    
    event_func_sum = sum(item['func_match'] for item in results['events']) if results['events'] else 0
    event_profile_sum = sum(item['profile_match'] for item in results['events']) if results['events'] else 0
    event_count = len(results['events']) if results['events'] else 1
    
    att_func_sum = sum(item['func_match'] for item in results['attendance']) if results['attendance'] else 0
    att_profile_sum = sum(item['profile_match'] for item in results['attendance']) if results['attendance'] else 0
    att_count = len(results['attendance']) if results['attendance'] else 1
    
    # Porcentajes parciales
    parcial_exp_func_match = exp_func_sum / exp_count
    parcial_exp_profile_match = exp_profile_sum / exp_count
    
    parcial_org_func_match = event_func_sum / event_count
    parcial_org_profile_match = event_profile_sum / event_count
    
    parcial_att_func_match = att_func_sum / att_count
    parcial_att_profile_match = att_profile_sum / att_count
    
    # Puntajes normalizados (0-5)
    exp_func_score = (parcial_exp_func_match * 5) / 100
    exp_profile_score = (parcial_exp_profile_match * 5) / 100
    
    org_func_score = (parcial_org_func_match * 5) / 100
    org_profile_score = (parcial_org_profile_match * 5) / 100
    
    att_func_score = (parcial_att_func_match * 5) / 100
    att_profile_score = (parcial_att_profile_match * 5) / 100
    
    profile_func_score = (results['profile']['func_match'] * 5) / 100
    profile_profile_score = (results['profile']['profile_match'] * 5) / 100
    
    # Resultados globales
    global_func_match = (parcial_exp_func_match + parcial_att_func_match + parcial_org_func_match + results['profile']['func_match']) / 4
    global_profile_match = (parcial_exp_profile_match + parcial_att_profile_match + parcial_org_profile_match + results['profile']['profile_match']) / 4
    
    # Puntaje global
    global_func_score = (global_func_match * 5) / 100
    global_profile_score = (global_profile_match * 5) / 100
    
    # Puntajes totales por sección
    exp_score = (exp_func_score + exp_profile_score) / 2
    org_score = (org_func_score + org_profile_score) / 2
    att_score = (att_func_score + att_profile_score) / 2
    prof_score = (profile_func_score + profile_profile_score) / 2
    
    # Puntaje final
    total_score = (overall_score + exp_score + org_score + att_score + prof_score) / 5
    
    # Guardar puntajes calculados
    results['scores'] = {
        'partial': {
            'experience': {
                'func_match': parcial_exp_func_match,
                'profile_match': parcial_exp_profile_match,
                'func_score': exp_func_score,
                'profile_score': exp_profile_score,
                'score': exp_score
            },
            'events': {
                'func_match': parcial_org_func_match,
                'profile_match': parcial_org_profile_match,
                'func_score': org_func_score,
                'profile_score': org_profile_score,
                'score': org_score
            },
            'attendance': {
                'func_match': parcial_att_func_match,
                'profile_match': parcial_att_profile_match,
                'func_score': att_func_score,
                'profile_score': att_profile_score,
                'score': att_score
            },
            'profile': {
                'func_match': results['profile']['func_match'],
                'profile_match': results['profile']['profile_match'],
                'func_score': profile_func_score,
                'profile_score': profile_profile_score,
                'score': prof_score
            }
        },
        'global': {
            'func_match': global_func_match,
            'profile_match': global_profile_match,
            'func_score': global_func_score,
            'profile_score': global_profile_score
        },
        'total': total_score
    }
    
    return results

def perform_descriptive_analysis(experience_items, event_items, attendance_items, profile_text, 
                                presentation_results, position_indicators, functions_text, profile_text_cargo):
    """Realizar análisis detallado de las secciones en formato descriptivo"""
    # Inicializar resultados
    results = {
        'experience': [],
        'events': [],
        'attendance': [],
        'profile': {'func_match': 0, 'profile_match': 0},
        'presentation': {},
        'indicators': {},
        'scores': {}
    }
    
    # Calcular la cantidad de ítems relacionados para cada indicador
    related_items_count = {indicator: 0 for indicator in position_indicators}
    
    # Analizar EXPERIENCIA EN ANEIAP
    for header, details in experience_items.items():
        header_and_details = f"{header} {' '.join(details)}"
        
        # Revisar palabras clave en el encabezado
        header_contains_keywords = any(
            keyword.lower() in header.lower() for keywords in position_indicators.values() for keyword in keywords
        )
        
        # Revisar palabras clave en los detalles
        details_contains_keywords = any(
            keyword.lower() in detail.lower() for detail in details for keywords in position_indicators.values() for keyword in keywords
        )
        
        # Determinar concordancia en funciones y perfil
        if header_contains_keywords or details_contains_keywords:
            exp_func_match = 100
            exp_profile_match = 100
        else:
            exp_func_match = calculate_similarity(header_and_details, functions_text)
            exp_profile_match = calculate_similarity(header_and_details, profile_text_cargo)
        
        # Ignorar ítems con 0% en funciones y perfil
        if exp_func_match > 0 or exp_profile_match > 0:
            results['experience'].append({
                'header': header, 
                'details': details, 
                'func_match': exp_func_match, 
                'profile_match': exp_profile_match
            })
        
        # Evaluar indicadores únicamente para el cargo seleccionado
        for indicator, keywords in position_indicators.items():
            # Identificar si el encabezado o detalles contienen palabras clave del indicador
            if any(keyword.lower() in header_and_details.lower() for keyword in keywords):
                related_items_count[indicator] += 1
    
    # Calcular porcentajes de indicadores
    total_items = len(experience_items)
    indicator_percentages = {
        indicator: (count / total_items) * 100 if total_items > 0 else 0 
        for indicator, count in related_items_count.items()
    }
    results['indicators'] = indicator_percentages
    
    # Analizar EVENTOS ORGANIZADOS
    for header, details in event_items.items():
        header_and_details = f"{header} {' '.join(details)}"
        
        # Revisar palabras clave en el encabezado
        header_contains_keywords = any(
            keyword.lower() in header.lower() for keywords in position_indicators.values() for keyword in keywords
        )
        
        # Revisar palabras clave en los detalles
        details_contains_keywords = any(
            keyword.lower() in detail.lower() for detail in details for keywords in position_indicators.values() for keyword in keywords
        )
        
        # Determinar concordancia en funciones y perfil
        if header_contains_keywords or details_contains_keywords:
            org_func_match = 100
            org_profile_match = 100
        else:
            org_func_match = calculate_similarity(header_and_details, functions_text)
            org_profile_match = calculate_similarity(header_and_details, profile_text_cargo)
        
        # Ignorar ítems con 0% en funciones y perfil
        if org_func_match > 0 or org_profile_match > 0:
            results['events'].append({
                'header': header, 
                'details': details, 
                'func_match': org_func_match, 
                'profile_match': org_profile_match
            })
    
    # Analizar ASISTENCIA A EVENTOS
    for header, details in attendance_items.items():
        header_and_details = f"{header} {' '.join(details)}"
        
        # Revisar palabras clave en el encabezado
        header_contains_keywords = any(
            keyword.lower() in header.lower() for keywords in position_indicators.values() for keyword in keywords
        )
        
        # Revisar palabras clave en los detalles
        details_contains_keywords = any(
            keyword.lower() in detail.lower() for detail in details for keywords in position_indicators.values() for keyword in keywords
        )
        
        # Determinar concordancia en funciones y perfil
        if header_contains_keywords or details_contains_keywords:
            att_func_match = 100
            att_profile_match = 100
        else:
            att_func_match = calculate_similarity(header_and_details, functions_text)
            att_profile_match = calculate_similarity(header_and_details, profile_text_cargo)
        
        # Ignorar ítems con 0% en funciones y perfil
        if att_func_match > 0 or att_profile_match > 0:
            results['attendance'].append({
                'header': header, 
                'details': details, 
                'func_match': att_func_match, 
                'profile_match': att_profile_match
            })
    
    # Analizar PERFIL
    profile_contains_keywords = any(
        keyword.lower() in profile_text.lower() for keywords in position_indicators.values() for keyword in keywords
    )
    
    if profile_contains_keywords:
        results['profile']['func_match'] = 100
        results['profile']['profile_match'] = 100
    else:
        results['profile']['func_match'] = calculate_similarity(profile_text, functions_text)
        results['profile']['profile_match'] = calculate_similarity(profile_text, profile_text_cargo)
    
    # Analizar Presentación
    results['presentation'] = {
        'spelling_score': (presentation_results['spelling_score'] / 100) * 5,
        'capitalization_score': (presentation_results['capitalization_score'] / 100) * 5,
        'coherence_score': (presentation_results['coherence_score'] / 100) * 5,
        'overall_score': (presentation_results['overall_score'] / 100) * 5
    }
    
    # Calcular puntajes parciales
    exp_func_sum = sum(item['func_match'] for item in results['experience']) if results['experience'] else 0
    exp_profile_sum = sum(item['profile_match'] for item in results['experience']) if results['experience'] else 0
    exp_count = len(results['experience']) if results['experience'] else 1
    
    event_func_sum = sum(item['func_match'] for item in results['events']) if results['events'] else 0
    event_profile_sum = sum(item['profile_match'] for item in results['events']) if results['events'] else 0
    event_count = len(results['events']) if results['events'] else 1
    
    att_func_sum = sum(item['func_match'] for item in results['attendance']) if results['attendance'] else 0
    att_profile_sum = sum(item['profile_match'] for item in results['attendance']) if results['attendance'] else 0
    att_count = len(results['attendance']) if results['attendance'] else 1
    
    # Porcentajes parciales
    parcial_exp_func_match = exp_func_sum / exp_count
    parcial_exp_profile_match = exp_profile_sum / exp_count
    
    parcial_org_func_match = event_func_sum / event_count
    parcial_org_profile_match = event_profile_sum / event_count
    
    parcial_att_func_match = att_func_sum / att_count
    parcial_att_profile_match = att_profile_sum / att_count
    
    # Puntajes normalizados (0-5)
    exp_func_score = (parcial_exp_func_match * 5) / 100
    exp_profile_score = (parcial_exp_profile_match * 5) / 100
    
    org_func_score = (parcial_org_func_match * 5) / 100
    org_profile_score = (parcial_org_profile_match * 5) / 100
    
    att_func_score = (parcial_att_func_match * 5) / 100
    att_profile_score = (parcial_att_profile_match * 5) / 100
    
    profile_func_score = (results['profile']['func_match'] * 5) / 100
    profile_profile_score = (results['profile']['profile_match'] * 5) / 100
    
    # Resultados globales
    global_func_match = (parcial_exp_func_match + parcial_att_func_match + parcial_org_func_match + results['profile']['func_match']) / 4
    global_profile_match = (parcial_exp_profile_match + parcial_att_profile_match + parcial_org_profile_match + results['profile']['profile_match']) / 4
    
    # Puntaje global
    global_func_score = (global_func_match * 5) / 100
    global_profile_score = (global_profile_match * 5) / 100
    
    # Puntajes totales por sección
    exp_score = (exp_func_score + exp_profile_score) / 2
    org_score = (org_func_score + org_profile_score) / 2
    att_score = (att_func_score + att_profile_score) / 2
    prof_score = (profile_func_score + profile_profile_score) / 2
    
    # Puntaje final
    total_score = (results['presentation']['overall_score'] + exp_score + org_score + att_score + prof_score) / 5
    
    # Guardar puntajes calculados
    results['scores'] = {
        'partial': {
            'experience': {
                'func_match': parcial_exp_func_match,
                'profile_match': parcial_exp_profile_match,
                'func_score': exp_func_score,
                'profile_score': exp_profile_score,
                'score': exp_score
            },
            'events': {
                'func_match': parcial_org_func_match,
                'profile_match': parcial_org_profile_match,
                'func_score': org_func_score,
                'profile_score': org_profile_score,
                'score': org_score
            },
            'attendance': {
                'func_match': parcial_att_func_match,
                'profile_match': parcial_att_profile_match,
                'func_score': att_func_score,
                'profile_score': att_profile_score,
                'score': att_score
            },
            'profile': {
                'func_match': results['profile']['func_match'],
                'profile_match': results['profile']['profile_match'],
                'func_score': profile_func_score,
                'profile_score': profile_profile_score,
                'score': prof_score
            }
        },
        'global': {
            'func_match': global_func_match,
            'profile_match': global_profile_match,
            'func_score': global_func_score,
            'profile_score': global_profile_score
        },
        'total': total_score
    }
    
    return results
