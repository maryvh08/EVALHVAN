import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import fitz
import numpy as np
import spacy
import pandas as pd
import streamlit as st # Keep streamlit import, some functions might still use it internally, but remove UI elements
from collections import Counter
from io import BytesIO
from textstat import textstat
from reportlab.platypus.flowables import PageBreak
import requests
import tarfile
import io
import re
import json
import os
import pytesseract
from spellchecker import SpellChecker
from textblob import TextBlob
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageTemplate, Frame, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.units import inch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import statsmodels.api as sm
from spellchecker import SpellChecker
import re
from PIL import Image as PILImage
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from fastapi.responses import JSONResponse
import shutil
import base64  # Import base64 for encoding PDF

app = FastAPI()

# Cargar las palabras clave y consejos desde los archivos JSON
def load_indicators(filepath="indicators.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)
def load_advice(filepath="advice.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)
def load_profile_examples():
    with open("profile.json", "r") as f:
        return json.load(f)

# Cargar indicadores y consejos al inicio del script
indicators = load_indicators()
advice = load_advice()
profile_examples = load_profile_examples()

# Uso del código
background_path = "Fondo reporte.png"
portada_path= "Portada Analizador.png"

# Asegurar que las dependencias de NLTK estén descargadas
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download("wordnet")

def preprocess_image(image):
    """
    Preprocesa una imagen antes de aplicar OCR.
    :param image: Imagen a preprocesar.
    :return: Imagen preprocesada.
    """
    # Convertir la imagen a escala de grises
    image = image.convert("L")

    # Mejorar el contraste
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # Aplicar umbral para binarización
    image = ImageOps.autocontrast(image)

    return image

def extract_text_with_ocr(pdf_path):
    """
    Extrae texto de un PDF utilizando PyMuPDF y OCR con preprocesamiento optimizado.
    :param pdf_path: Ruta del archivo PDF.
    :return: Texto extraído del PDF.
    """
    extracted_text = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            # 📌 **1️⃣ Intentar extraer texto directamente**
            page_text = page.get_text("text").strip()

            if not page_text:  # Si no hay texto, usar OCR
                pix = page.get_pixmap(dpi=300)  # Aumentar DPI para mejorar OCR
                img = Image.open(io.BytesIO(pix.tobytes(output="png")))

                # 📌 **2️⃣ Preprocesamiento de imagen**
                img = img.convert("L")  # Convertir a escala de grises
                img = img.filter(ImageFilter.MedianFilter())  # Reducir ruido
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(2)  # Aumentar contraste

                # 📌 **3️⃣ Aplicar OCR**
                page_text = pytesseract.image_to_string(img, config="--psm 3").strip()

            extracted_text.append(page_text)

    return "\n".join(extracted_text)

def extract_cleaned_lines(text):
    if isinstance(text, list):
        text = "\n".join(text)  # Convierte la lista en un texto único antes de dividirlo

    lines = text.split("\n")  # Ahora estamos seguros de que text es una cadena
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        # 📌 **1️⃣ Filtrar líneas vacías y no imprimibles**
        if not line or not any(char.isalnum() for char in line):
            continue  # Ignorar líneas sin caracteres alfanuméricos

        # 📌 **2️⃣ Remover líneas con solo números (ejemplo: números de página)**
        if re.fullmatch(r"\d+", line):
            continue

        # 📌 **3️⃣ Ignorar líneas con muy pocos caracteres (posibles errores OCR)**
        if len(line) < 3:
            continue

        cleaned_lines.append(line)

    return cleaned_lines

def calculate_all_indicators(lines, position_indicators):
    """
    Calcula los porcentajes de todos los indicadores para un cargo.
    :param lines: Lista de líneas de la sección "EXPERIENCIA EN ANEIAP".
    :param position_indicators: Diccionario de indicadores y palabras clave del cargo.
    :return: Diccionario con los porcentajes por indicador.
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
    :param lines: Lista de líneas de la sección "EXPERIENCIA EN ANEIAP".
    :param position_indicators: Diccionario de indicadores y palabras clave del cargo.
    :return: Diccionario con los porcentajes por indicador y detalles de líneas relevantes.
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

# Función para calcular la similitud usando TF-IDF y similitud de coseno
def clean_text(text):
    """Limpia el texto eliminando caracteres especiales y espacios extra."""

    if not isinstance(text, str):  # Si no es una cadena de texto, manejar el error
        print(f"⚠️ Error en clean_text: Se esperaba str, pero se recibió {type(text)} -> {text}")
        return ""  # Evita que falle devolviendo una cadena vacía

    text = re.sub(r"[^\w\s]", "", text)  # Elimina puntuación
    text = re.sub(r"\s+", " ", text).strip().lower()  # Normaliza espacios y minúsculas
    return text

def calculate_similarity(text1, text2):
    """Calcula la similitud entre dos textos usando TF-IDF y similitud de coseno."""

    if not isinstance(text1, str) or not isinstance(text2, str):
        print(f"⚠️ Error en calculate_similarity: text1 ({type(text1)}) = {text1}, text2 ({type(text2)}) = {text2}")
        return 0  # Evita errores si los valores son incorrectos

    text1, text2 = clean_text(text1), clean_text(text2)

    if not text1 or not text2:  # Si después de limpiar los textos están vacíos
        print(f"⚠️ Textos vacíos después de limpieza: text1='{text1}', text2='{text2}'")
        return 0

    try:
        vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(similarity * 100, 2)
    except Exception as e:
        print(f"⚠️ Error en calculate_similarity: {e}")
        return 0

def calculate_presence(texts, keywords):
    """
    Calcula el porcentaje de palabras clave presentes en los textos.
    :param texts: Lista de textos (e.g., detalles).
    :param keywords: Lista de palabras clave a buscar.
    :return: Porcentaje de coincidencia.
    """
    if not texts or not keywords:
        return 0  # Evitar división por cero

    keywords = set(map(str.lower, keywords))  # Convertir palabras clave a minúsculas
    matches = 0

    for text in texts:
        words = set(re.findall(r"\b\w+\b", text.lower()))  # Extraer palabras únicas en minúsculas
        matches += sum(1 for keyword in keywords if keyword in words)

    return round((matches / len(keywords)) * 100, 2)  # Redondear a 2 decimales


def draw_full_page_cover(canvas, portada_path, candidate_name, position,chapter):
    """
    Dibuja la portada con una imagen a página completa y el título del reporte completamente centrado.
    :param canvas: Lienzo de ReportLab.
    :param portada_path: Ruta de la imagen de la portada.
    :param candidate_name: Nombre del candidato.
    :param position: Cargo al que aspira.
    :param chapter: Capítulo del Candidato
    """
    # 📌 Obtener el tamaño de la página (Carta)
    page_width, page_height = letter

    # 📌 Cargar la imagen de la portada
    img = ImageReader(portada_path)
    img_width, img_height = img.getSize()

    # 📌 Ajustar la imagen proporcionalmente para que llene la página
    scale_factor = max(page_width / img_width, page_height / img_height)
    new_width = img_width * scale_factor
    new_height = img_height * scale_factor

    # 📌 Centrar la imagen en la página
    x_offset = (page_width - new_width) / 2
    y_offset = (page_height - new_height) / 2

    # 📌 Dibujar la imagen de portada en toda la página
    canvas.drawImage(portada_path, x_offset, y_offset, width=new_width, height=new_height)

    # 📌 **AGREGAR EL TÍTULO DEL REPORTE EN EL CENTRO**
    title_style = ParagraphStyle(name="Title", fontName="CenturyGothicBold", fontSize=48, textColor=colors.black, alignment=1,)

    title_text = f"REPORTE DE ANÁLISIS\n{candidate_name.upper()}\nCARGO: {position.upper()}\nCAPÍTULO:{chapter.upper()}"

    # 📌 Configurar fuente y color del texto
    canvas.setFont("CenturyGothicBold", 36)
    canvas.setFillColor(colors.black)

    # 📌 Medir el ancho y alto del texto
    text_width = max(canvas.stringWidth(line, "CenturyGothicBold", 36) for line in title_text.split("\n"))
    text_height = 36 * len(title_text.split("\n"))  # Multiplicamos por el número de líneas

    # 📌 Centrar el texto
    text_x = (page_width - text_width) / 2
    text_y = (page_height - text_height) / 2  # Ajuste para centrar verticalmente

    # 📌 Dibujar cada línea del título centrado
    for i, line in enumerate(title_text.split("\n")):
        line_width = canvas.stringWidth(line, "CenturyGothicBold", 36)
        line_x = (page_width - line_width) / 2
        canvas.drawString(line_x, text_y - (i * 30), line)  # Espaciado entre líneas


def add_background(canvas, background_path):
    """
    Dibuja una imagen de fondo en cada página del PDF.
    :param canvas: Lienzo de ReportLab.
    :param background_path: Ruta a la imagen de fondo.
    """
    canvas.saveState()
    canvas.drawImage(background_path, 0, 0, width=letter[0], height=letter[1])
    canvas.restoreState()

# FUNCIONES PARA PRIMARY
def count_matching_keywords(text, keywords):
    """
    Cuenta cuántas palabras clave aparecen en un texto y calcula su peso relativo.
    :param text: Texto de la sección "Perfil".
    :param keyword_sets: Diccionario con listas de palabras clave agrupadas por categoría.
    :return: Total de palabras en el perfil y porcentaje de coincidencia con palabras clave.
    """
    words = re.findall(r"\b\w+\b", text.lower())  # Tokeniza sin usar NLTK
    total_words = len(words)

    # Crear un contador de palabras en el texto
    word_freq = Counter(words)

    # Contar coincidencias con palabras clave
    keyword_count = sum(word_freq[word] for kw_set in keywords.values() for word in kw_set if word in word_freq)

    # Evitar división por cero
    match_percentage = (keyword_count / total_words) * 100 if total_words > 0 else 0

    return total_words, keyword_count, match_percentage

def extract_profile_section_with_ocr(pdf_path):
    """
    Extrae la sección 'Perfil' de un archivo PDF con soporte de OCR.
    :param pdf_path: Ruta del archivo PDF.
    :return: Texto de la sección 'Perfil'.
    """
    text = extract_text_with_ocr(pdf_path)

    if not text or len(text.strip()) == 0:
        print("⚠️ No se pudo extraer texto del PDF.")
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
        print("⚠️ No se encontró la sección 'Perfil'.")
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
    """
    Extrae la sección 'EXPERIENCIA EN ANEIAP' de un archivo PDF con soporte de OCR.
    :param pdf_path: Ruta del archivo PDF.
    :return: Texto de la sección 'EXPERIENCIA EN ANEIAP'.
    """
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

    # Debugging: Imprime líneas procesadas
    print("Líneas procesadas:")
    for line in cleaned_lines:
        print(f"- {line}")

    return "\n".join(cleaned_lines)

def extract_event_section_with_ocr(pdf_path):
    """
    Extrae la sección 'EVENTOS ORGANIZADOS' de un archivo PDF con OCR,
    asegurando que los ítems sean correctamente identificados.
    """
    text = extract_text_with_ocr(pdf_path)
    if not text:
        return []  # Retorna lista vacía si no hay contenido

    text = extract_text_with_ocr(pdf_path)

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

    # Debugging: Imprime líneas procesadas
    print("Líneas procesadas:")
    for line in cleaned_lines:
        print(f"- {line}")

    return "\n".join(cleaned_lines)

def evaluate_cv_presentation(pdf_path):
    """
    Evalúa la presentación de la hoja de vida en términos de redacción, ortografía,
    coherencia básica, y claridad.
    :param pdf_path: Ruta del archivo PDF.
    :return: Texto limpio y análisis detallado de la presentación.
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

def extract_attendance_section_with_ocr(pdf_path):
    """
    Extrae la sección 'Asistencia Eventos ANEIAP' de un archivo PDF con soporte de OCR.
    :param pdf_path: Ruta del archivo PDF.
    :return: Texto de la sección 'Asistencia Eventos ANEIAP'.
    """
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

    # Debugging: Imprime líneas procesadas
    print("Líneas procesadas:")
    for line in att_cleaned_lines:
        print(f"- {line}")

    return "\n".join(att_cleaned_lines)

def generate_report_with_background_api(pdf_path, position, candidate_name,background_path, chapter):
    """
    Genera un reporte con un fondo en cada página for API usage, returns base64 encoded PDF.
    :param pdf_path: Ruta del PDF.
    :param position: Cargo al que aspira.
    :param candidate_name: Nombre del candidato.
    :param background_path: Ruta de la imagen de fondo.
    :param chapter: Capítulo del Candidato
    :return: base64 encoded PDF content and report path
    """
    experience_text = extract_experience_section_with_ocr(pdf_path)
    if not experience_text:
        return None, "No se encontró la sección 'EXPERIENCIA EN ANEIAP' en el PDF."

    org_text = extract_event_section_with_ocr(pdf_path)
    if not org_text:
        return None, "No se encontró la sección 'EVENTOS ORGANIZADOS' en el PDF."

    att_text = extract_attendance_section_with_ocr(pdf_path)
    if not att_text:
        return None, "No se encontró la sección 'Asistencia a Eventos ANEIAP' en el PDF."

    resume_text= evaluate_cv_presentation(pdf_path)
    if not resume_text:
        return None, "No se encontró el texto de la hoja de vida"

    candidate_profile_text= extract_profile_section_with_ocr(pdf_path)
    if not candidate_profile_text:
        return None, "No se encontró la sección 'Perfil' en el PDF."

    # Dividir la experiencia en líneas
    lines = extract_cleaned_lines(experience_text)
    lines= experience_text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]  # Eliminar líneas vacías

    # Dividir los eventos en líneas
    org_lines = extract_cleaned_lines(org_text)
    org_lines= org_text.split("\n")
    org_lines = [line.strip() for line in org_lines if line.strip()]  # Eliminar líneas vacías

    #Dividir lineas de perfil
    candidate_profile_lines = extract_cleaned_lines(candidate_profile_text)
    candidate_profile_lines= candidate_profile_text.split("\n")
    candidate_profile_lines= [line.strip() for line in candidate_profile_lines if line.strip()]

    # Dividir la asistencia en líneas
    att_lines = extract_cleaned_lines(att_text)
    att_lines= att_text.split("\n")
    att_lines = [line.strip() for line in att_lines if line.strip()]  # Eliminar líneas vacías

    # Obtener los indicadores y palabras clave para el cargo seleccionado
    position_indicators = indicators.get(position, {})

    indicator_results = calculate_all_indicators(lines, position_indicators)

    # Cargar funciones y perfil
    try:
        with fitz.open(f"Funciones//F{position}.pdf") as func_doc:
            functions_text = func_doc[0].get_text()
        with fitz.open(f"Perfiles/P{position}.pdf") as profile_doc:
            profile_text = profile_doc[0].get_text()
    except Exception as e:
        return None, f"Error al cargar funciones o perfil: {e}"

    line_results = []
    org_line_results = []
    att_line_results = []

    # Evaluación de renglones de EXPERIENCIA EN ANEIAP
    # Evaluación de renglones
    for line in lines:
        line = line.strip()
        if not line:  # Ignorar líneas vacías
            continue

        # Dividir la experiencia en líneas
        lines = extract_cleaned_lines(experience_text)
        lines = experience_text.split("\n")
        lines = [line.strip() for line in lines if line.strip()]  # Eliminar líneas vacías

        # Obtener los indicadores y palabras clave para el cargo seleccionado
        position_indicators = indicators.get(position, {})
        indicator_results = {}

        # Calcular el porcentaje por cada indicador
        indicator_results = calculate_indicators_for_report(lines, position_indicators)
        for indicator, keywords in position_indicators.items():
            indicator_results = calculate_indicators_for_report(lines, position_indicators)

        # Calcular la presencia total (si es necesario)
        total_presence = sum(result["percentage"] for result in indicator_results.values())

        # Normalizar los porcentajes si es necesario
        if total_presence > 0:
            for indicator in indicator_results:
                indicator_results[indicator]["percentage"] = (indicator_results[indicator]["percentage"] / total_presence) * 100

        # Evaluación general de concordancia
        if any(keyword.lower() in line.lower() for kw_set in position_indicators.values() for keyword in kw_set):
            func_match = 100.0
            profile_match = 100.0
        else:
            # Calcular similitud
            func_match = calculate_similarity(line, functions_text)
            profile_match = calculate_similarity(line, profile_text)

        # Solo agregar al reporte si no tiene 0% en ambas métricas
        if func_match > 0 or profile_match > 0:
            line_results.append((line, func_match, profile_match))

    # Normalización de los resultados de indicadores
    total_presence = sum(indicator["percentage"] for indicator in indicator_results.values())
    if total_presence > 0:
        for indicator in indicator_results:
            indicator_results[indicator]["percentage"] = (indicator_results[indicator]["percentage"] / total_presence) * 100

    # Evaluación de renglones eventos organizados
    for line in org_lines:
        line = line.strip()
        if not line:  # Ignorar líneas vacías
            continue

        # Dividir los eventos en líneas
        org_lines = extract_cleaned_lines(org_text)
        org_lines= att_text.split("\n")
        org_lines = [line.strip() for line in org_lines if line.strip]

        # Evaluación general de concordancia
        if any(keyword.lower() in line.lower() for kw_set in position_indicators.values() for keyword in kw_set):
            org_func_match = 100.0
            org_profile_match = 100.0
        else:
            # Calcular similitud
            org_func_match = calculate_similarity(line, functions_text)
            org_profile_match = calculate_similarity(line, profile_text)

        # Solo agregar al reporte si no tiene 0% en ambas métricas
        if org_func_match > 0 or org_profile_match > 0:
            org_line_results.append((line, org_func_match, org_profile_match))

    # Evaluación de renglones asistencia a eventos
    for line in att_lines:
        line = line.strip()
        if not line:  # Ignorar líneas vacías
            continue

        # Dividir los asistencia en líneas
        att_lines = extract_cleaned_lines(att_text)
        att_lines= att_text.split("\n")
        att_lines = [line.strip() for line in att_lines if line.strip]

        # Evaluación general de concordancia
        if any(keyword.lower() in line.lower() for kw_set in position_indicators.values() for keyword in kw_set):
            att_func_match = 100.0
            att_profile_match = 100.0
        else:
            # Calcular similitud
            att_func_match = calculate_similarity(line, functions_text)
            att_profile_match = calculate_similarity(line, profile_text)

        # Solo agregar al reporte si no tiene 0% en ambas métricas
        if att_func_match > 0 or att_profile_match > 0:
            att_line_results.append((line, att_func_match, att_profile_match))

    # Calcular porcentajes de concordancia con perfil de candidato
    keyword_count = 0
    words = re.findall(r"\b\w+\b", candidate_profile_text)
    total_words = len(words)
    for kw_set in position_indicators.values():
        for keyword in kw_set:
            keyword_count += candidate_profile_text.count(keyword)

    prop_keyword= keyword_count/total_words

    # Evitar división por cero
    if prop_keyword<= 0.01:
        keyword_match_percentage = 0
    elif 0.01 <prop_keyword <= 0.15:
        keyword_match_percentage = 25
    elif 0.15 <prop_keyword <= 0.5:
        keyword_match_percentage = 50
    elif 0.5 <prop_keyword <= 0.75:
        keyword_match_percentage = 75
    else:
        keyword_match_percentage = 100

    # Evaluación de concordancia basada en palabras clave
    if keyword_match_percentage == 100:
        profile_func_match = 100.0
        profile_profile_match = 100.0
    else:
        # Calcular similitud con funciones y perfil del cargo si la coincidencia es baja
        prof_func_match = calculate_similarity(candidate_profile_text, functions_text)
        prof_profile_match = calculate_similarity(candidate_profile_text, profile_text)
        profile_func_match = keyword_match_percentage + prof_func_match
        profile_profile_match = keyword_match_percentage + prof_profile_match

    # Calcular porcentajes parciales respecto a la Experiencia ANEIAP
    if line_results:  # Evitar división por cero si no hay ítems válidos
        parcial_exp_func_match = sum([res[1] for res in line_results]) / len(line_results)
        parcial_exp_profile_match = sum([res[2] for res in line_results]) / len(line_results)
    else:
        parcial_exp_func_match = 0
        parcial_exp_profile_match = 0

    # Calcular porcentajes parciales respecto a los Eventos ANEIAP
    if org_line_results:  # Evitar división por cero si no hay ítems válidos
        parcial_org_func_match = sum([res[1] for res in org_line_results]) / len(org_line_results)
        parcial_org_profile_match = sum([res[2] for res in org_line_results]) / len(org_line_results)
    else:
        parcial_org_func_match = 0
        parcial_org_profile_match = 0

    # Calcular porcentajes parciales respecto a la asistencia a eventos
    if att_line_results:  # Evitar división por cero si no hay ítems válidos
        parcial_att_func_match = sum([res[1] for res in att_line_results]) / len(att_line_results)
        parcial_att_profile_match = sum([res[2] for res in att_line_results]) / len(att_line_results)
    else:
        parcial_att_func_match = 0
        parcial_att_profile_match = 0

    resume_text= evaluate_cv_presentation(pdf_path)

    # Inicializar corrector ortográfico
    spell = SpellChecker(language='es')

    punctuation_errors = 0

    for i, line in enumerate(lines):
        # Verificar si la oración termina con puntuación válida
        if not line.endswith((".", "!", "?")):
            punctuation_errors += 1

    # Limpiar y dividir el texto en líneas
    pres_cleaned_lines = [line.strip() for line in resume_text.split("\n") if line.strip()]
    total_lines = len(pres_cleaned_lines)

    # Métricas
    total_words = 0
    spelling_errors = 0
    missing_capitalization = 0
    incomplete_sentences = 0
    punctuation_marks = 0
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

        # Gramática básica: verificar patrones comunes (ejemplo)
        grammar_errors += len(re.findall(r'\b(?:es|está|son)\b [^\w\s]', line))  # Ejemplo: "es" sin continuación válida

    # Calcular métricas secundarias
    spelling = 1- (spelling_errors / total_words)
    capitalization_score = 1- (missing_capitalization / total_lines)
    sentence_completion_score = 1- (incomplete_sentences / total_lines)
    grammar = 1- (grammar_errors / total_lines)
    punctuation_error_rate = 1- (punctuation_errors / total_lines)

    #Calcular métricas principales
    grammar_score = round(((punctuation_error_rate+ grammar+ sentence_completion_score)/3)*5, 2)
    spelling_score= round(((spelling+ capitalization_score)/2)*5,2)

    if total_lines == 0:
        return 100  # Si no hay oraciones, asumimos coherencia perfecta.

    # Calcular métricas coherencia
    # 1. Repetición de palabras
    def calculate_word_repetition(pres_cleaned_lines):
        repeated_words = Counter()
        for line in pres_cleaned_lines:
            words = line.split()
            repeated_words.update([word.lower() for word in words])

        total_words = sum(repeated_words.values())
        unique_words = len(repeated_words)
        most_common_word_count = repeated_words.most_common(1)[0][1] if repeated_words else 0
        repeated_word_ratio = (most_common_word_count / total_words) if total_words > 0 else 0

        # Una menor repetición indica mayor calidad
        repetition_score = 1 - repeated_word_ratio
        return repetition_score, repeated_words

    # 2. Fluidez entre oraciones
    def calculate_sentence_fluency(pres_cleaned_lines):
        """
        Calcula el puntaje de fluidez de las oraciones basándose en conectores lógicos, puntuación,
        y variabilidad en la longitud de las oraciones.
        :param pres_cleaned_lines: Lista de líneas limpias del texto.
        :return: Puntaje de fluidez de las oraciones entre 0 y 1.
        """
        # Lista de conectores lógicos comunes
        logical_connectors = {
        "adición": [
            "además", "también", "asimismo", "igualmente", "de igual manera",
            "por otro lado", "de la misma forma", "junto con"
        ],
        "causa": [
            "porque", "ya que", "debido a", "dado que", "por motivo de",
            "gracias a", "en razón de", "a causa de"
        ],
        "consecuencia": [
            "por lo tanto", "así que", "en consecuencia", "como resultado",
            "por esta razón", "de modo que", "lo que permitió", "de ahí que"
        ],
        "contraste": [
            "sin embargo", "pero", "aunque", "no obstante", "a pesar de",
            "por el contrario", "en cambio", "si bien", "mientras que"
        ],
        "condición": [
            "si", "en caso de", "a menos que", "siempre que", "con la condición de",
            "a no ser que", "en el supuesto de que"
        ],
        "tiempo": [
            "mientras", "cuando", "después de", "antes de", "al mismo tiempo",
            "posteriormente", "una vez que", "simultáneamente", "en el transcurso de"
        ],
        "descripción de funciones": [
            "encargado de", "responsable de", "mis funciones incluían",
            "lideré", "gestioné", "coordiné", "dirigí", "supervisé",
            "desarrollé", "planifiqué", "ejecuté", "implementé", "organicé"
        ],
        "logros y resultados": [
            "logré", "alcancé", "conseguí", "incrementé", "reduje",
            "optimizé", "mejoré", "aumenté", "potencié", "maximicé",
            "contribuí a", "obtuve", "permitió mejorar", "impactó positivamente en"
        ],
        "secuencia": [
            "primero", "en primer lugar", "a continuación", "luego", "después",
            "seguidamente", "posteriormente", "finalmente", "por último"
        ],
        "énfasis": [
            "sobre todo", "en particular", "especialmente", "principalmente",
            "específicamente", "vale la pena destacar", "conviene resaltar",
            "cabe mencionar", "es importante señalar"
        ],
        "conclusión": [
            "en resumen", "para concluir", "en definitiva", "en síntesis",
            "como conclusión", "por ende", "por consiguiente", "para finalizar"
        ]
    }
        connector_count = 0
        total_lines = len(pres_cleaned_lines)

        # Validación para evitar divisiones por cero
        if total_lines == 0:
            return 0  # Sin líneas, no se puede calcular fluidez

        # Inicialización de métricas
        punctuation_errors = 0
        sentence_lengths = []

        for line in pres_cleaned_lines:
            # Verificar errores de puntuación (oraciones sin punto final)
            if not line.endswith((".", "!", "?")):
                punctuation_errors += 1

            # Almacenar la longitud de cada oración
            sentence_lengths.append(len(line.split()))

            # Contar conectores lógicos en la línea
            for connector in logical_connectors:
                if connector in line.lower():
                    connector_count += 1

        # Calcular métricas individuales
        avg_length = sum(sentence_lengths) / total_lines
        length_variance = sum(
            (len(line.split()) - avg_length) ** 2 for line in pres_cleaned_lines
        ) / total_lines if total_lines > 1 else 0

        # Normalizar métricas entre 0 y 1
        punctuation_score = max(0, 1 - (punctuation_errors / total_lines))  # 1 si no hay errores
        connector_score = min(1, connector_count / total_lines)  # Máximo 1, basado en conectores
        variance_penalty = max(0, 1 - length_variance / avg_length) if avg_length > 0 else 0

        # Calcular puntaje final de fluidez
        fluency_score = (punctuation_score + connector_score + variance_penalty) / 3
        return round(fluency_score, 2)


    # Calcular métricas individuales
    repetition_score, repeated_words = calculate_word_repetition(pres_cleaned_lines)
    fluency_score = calculate_sentence_fluency(pres_cleaned_lines)

    # Asegurar que repetition_score y fluency_score están entre 0 y 1 antes de la conversión
    normalized_repetition_score = min(1, max(0, repetition_score))
    normalized_fluency_score = min(1, max(0, fluency_score))

    # Calcular coherencia asegurando que el resultado final no pase de 5
    coherence_score = round(min(5, (normalized_repetition_score + normalized_fluency_score) * 2.5), 2)

    # Puntaje general ponderado
    overall_score = round((spelling_score  + coherence_score + grammar_score) / 3, 2)

    # Calculo puntajes parciales
    parcial_exp_func_score = round((parcial_exp_func_match * 5) / 100, 2)
    parcial_exp_profile_score = round((parcial_exp_profile_match * 5) / 100, 2)
    parcial_org_func_score = round((parcial_org_func_match * 5) / 100, 2)
    parcial_org_profile_score = round((parcial_org_profile_match * 5) / 100, 2)
    parcial_att_func_score = round((parcial_att_func_match * 5) / 100, 2)
    parcial_att_profile_score = round((parcial_att_profile_match * 5) / 100, 2)
    profile_func_score= round((profile_func_match * 5) / 100, 2)
    profile_profile_score= round((profile_profile_match * 5) / 100, 2)

    #Calcular resultados globales
    global_func_match = (parcial_exp_func_match + parcial_att_func_match + parcial_org_func_match+ profile_func_match) / 4
    global_profile_match = (parcial_exp_profile_match + parcial_att_profile_match + parcial_org_profile_match + profile_profile_match) / 4
    func_score = round((global_func_match * 5) / 100, 2)
    profile_score = round((global_profile_match * 5) / 100, 2)

    #Calculo puntajes totales
    exp_score= (parcial_exp_func_score+ parcial_exp_profile_score)/2
    org_score= (parcial_org_func_score+ parcial_org_profile_score)/2
    att_score= (parcial_att_func_score+ parcial_att_profile_score)/2
    prof_score= (profile_func_score+ profile_profile_score)/2
    total_score= (overall_score+ exp_score+ org_score+ att_score+ profile_score)/5

    # Registrar la fuente personalizada
    pdfmetrics.registerFont(TTFont('CenturyGothic', 'Century_Gothic.ttf'))
    pdfmetrics.registerFont(TTFont('CenturyGothicBold', 'Century_Gothic_Bold.ttf'))

    # Estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CenturyGothic", fontName="CenturyGothic", fontSize=12, leading=14, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name="CenturyGothicBold", fontName="CenturyGothicBold", fontSize=12, leading=14, alignment=TA_JUSTIFY))

    # Crear el documento PDF
    report_path = f"Reporte_analisis_cargo_{candidate_name}_{position}_{chapter}.pdf"
    doc = SimpleDocTemplate(report_path, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=100, bottomMargin=72)

    # Lista de elementos para el reporte
    elements = []

    # 📌 **3️⃣ AGREGAR PORTADA SIN FONDO**
    def on_first_page(canvas, doc):
        """Dibuja una portada que ocupa toda la página."""
        draw_full_page_cover(canvas, portada_path, candidate_name, position, chapter)

    # Título del reporte centrado
    title_style = ParagraphStyle(name='CenteredTitle', fontName='CenturyGothicBold', fontSize=14, leading=16, alignment=1,  # 1 significa centrado, textColor=colors.black
                                )
    # Convertir texto a mayúsculas
    elements.append(PageBreak())
    title_candidate_name = candidate_name.upper()
    title_position = position.upper()
    tittle_chapter= chapter.upper()

    elements.append(Paragraph(f"REPORTE DE ANÁLISIS {title_candidate_name} CARGO {title_position} {tittle_chapter}", title_style))

    elements.append(Spacer(1, 0.2 * inch))

    # Concordancia de items organizada en tabla con ajuste de texto
    elements.append(Paragraph("<b>Análisis de perfil de aspirante:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    # Encabezados de la tabla
    prof_table_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]

    #Agregar resultados parciales
    prof_table_data.append([Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']), f"{profile_func_match:.2f}%", f"{profile_profile_match:.2f}%"])
    prof_table_data.append([Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']), f"{profile_func_score:.2f}", f"{profile_profile_score:.2f}"])

    # Crear la tabla con ancho de columnas ajustado
    prof_item_table = Table(prof_table_data, colWidths=[3 * inch, 2 * inch, 2 * inch])

    # Estilos de la tabla con ajuste de texto
    prof_item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto en encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),  # Fuente para encabezados
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),  # Fuente para el resto de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear texto verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de texto
    ]))

    # Agregar tabla a los elementos
    elements.append(prof_item_table)

    elements.append(Spacer(1, 0.2 * inch))

    # Concordancia de items organizada en tabla con ajuste de texto
    elements.append(Paragraph("<b>Análisis de ítems de asistencia a eventos:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    # Encabezados de la tabla
    att_table_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]

    # Agregar datos de line_results a la tabla
    for line, att_func_match, att_profile_match in att_line_results:
        att_table_data.append([Paragraph(line, styles['CenturyGothic']), f"{att_func_match:.2f}%", f"{att_profile_match:.2f}%"])

    #Agregar resultados parciales
    att_table_data.append([Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']), f"{parcial_att_func_match:.2f}%", f"{parcial_att_profile_match:.2f}%"])
    att_table_data.append([Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']), f"{parcial_att_func_score:.2f}", f"{parcial_att_profile_score:.2f}"])

    # Crear la tabla con ancho de columnas ajustado
    att_item_table = Table(att_table_data, colWidths=[3 * inch, 2 * inch, 2 * inch])

    # Estilos de la tabla con ajuste de texto
    att_item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto en encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),  # Fuente para encabezados
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),  # Fuente para el resto de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear texto verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de texto
    ]))

    # Agregar tabla a los elementos
    elements.append(att_item_table)

    elements.append(Spacer(1, 0.1 * inch))

    # Total de líneas analizadas en ASISTENCIA A EVENTOS ANEIAP
    att_total_lines = len(att_line_results)
    elements.append(Paragraph(f"• Total de asistencias a eventos analizadas: {att_total_lines}", styles['CenturyGothicBold']))

    elements.append(Spacer(1, 0.2 * inch))

    # Concordancia de items organizada en tabla con ajuste de texto
    elements.append(Paragraph("<b>Análisis de ítems de eventos organizados:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    # Encabezados de la tabla
    org_table_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]

    # Agregar datos de line_results a la tabla
    for line, org_func_match, org_profile_match in org_line_results:
        org_table_data.append([Paragraph(line, styles['CenturyGothic']), f"{org_func_match:.2f}%", f"{org_profile_match:.2f}%"])

    #Agregar resultados parciales
    org_table_data.append([Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']), f"{parcial_org_func_match:.2f}%", f"{parcial_org_profile_match:.2f}%"])
    org_table_data.append([Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']), f"{parcial_org_func_score:.2f}", f"{parcial_org_profile_score:.2f}"])

    # Crear la tabla con ancho de columnas ajustado
    org_item_table = Table(org_table_data, colWidths=[3 * inch, 2 * inch, 2 * inch])

    # Estilos de la tabla con ajuste de texto
    org_item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto en encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),  # Fuente para encabezados
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),  # Fuente para el resto de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear texto verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de texto
    ]))

    # Agregar tabla a los elementos
    elements.append(org_item_table)

    elements.append(Spacer(1, 0.1 * inch))

    # Total de líneas analizadas en ASISTENCIA A EVENTOS ANEIAP
    org_total_lines = len(org_line_results)
    elements.append(Paragraph(f"• Total de eventos analizados: {org_total_lines}", styles['CenturyGothicBold']))

    elements.append(Spacer(1, 0.2 * inch))

    # Concordancia de items organizada en tabla con ajuste de texto
    elements.append(Paragraph("<b>Análisis de ítems:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    # Encabezados de la tabla
    table_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]

    # Agregar datos de line_results a la tabla
    for line, exp_func_match, exp_profile_match in line_results:
        table_data.append([Paragraph(line, styles['CenturyGothic']), f"{exp_func_match:.2f}%", f"{exp_profile_match:.2f}%"])

    #Agregar resultados parciales
    table_data.append([Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']), f"{parcial_exp_func_match:.2f}%", f"{parcial_exp_profile_match:.2f}%"])
    table_data.append([Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']), f"{parcial_exp_func_score:.2f}", f"{parcial_exp_profile_score:.2f}"])

    # Crear la tabla con ancho de columnas ajustado
    item_table = Table(table_data, colWidths=[3 * inch, 2 * inch, 2 * inch])

    # Estilos de la tabla con ajuste de texto
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto en encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),  # Fuente para encabezados
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),  # Fuente para el resto de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear texto verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de texto
    ]))

    # Agregar tabla a los elementos
    elements.append(item_table)

    elements.append(Spacer(1, 0.2 * inch))

    # Total de líneas analizadas en EXPERIENCIA EN ANEIAP
    total_lines = len(line_results)
    elements.append(Paragraph(f"• Total de experiencias analizadas: {total_lines}", styles['CenturyGothicBold']))

    elements.append(Spacer(1, 0.2 * inch))

    # Añadir resultados al reporte
    elements.append(Paragraph("<b>Evaluación de la Presentación:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    # Crear tabla de evaluación de presentación
    presentation_table = Table(
        [
            ["Criterio", "Puntaje"],
            ["Coherencia", f"{coherence_score:.2f}"],
            ["Ortografía", f"{spelling_score:.2f}"],
            ["Gramática", f"{grammar_score:.2f}"],
            ["Puntaje Total", f"{overall_score:.2f}"]
        ],
        colWidths=[3 * inch, 2 * inch]
    )

    # Estilo de la tabla
    presentation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(presentation_table)

    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("<b>Consejos para mejorar la presentación de la hoja de vida:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    # Concordancia de items organizada en tabla con ajuste de texto
    elements.append(Paragraph("<b>Resultados de indicadores:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    # Encabezados de la tabla
    table_indicator = [["Indicador", "Concordancia (%)"]]

    # Agregar datos de line_results a la tabla
    for indicator, data in indicator_results.items():
        relevant_lines = sum(
            any(keyword.lower() in line.lower() for keyword in keywords) for line in lines
        )
        total_lines = len(line_results)
        percentage = (relevant_lines / total_lines) * 100 if total_lines > 0 else 0
        if isinstance(percentage, (int, float)):  # Validar que sea un número
            table_indicator.append([Paragraph(indicator, styles['CenturyGothic']), f"{percentage:.2f}%"])

    # Crear la tabla con ancho de columnas ajustado
    indicator_table = Table(table_indicator, colWidths=[3 * inch, 2 * inch, 2 * inch])

    # Estilos de la tabla con ajuste de texto
    indicator_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto en encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),  # Fuente para encabezados
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),  # Fuente para el resto de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear texto verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de texto
    ]))

    # Agregar tabla a los elementos
    elements.append(indicator_table)

    elements.append(Spacer(1, 0.2 * inch))

    # Consejos para mejorar indicadores con baja presencia
    low_performance_indicators = {k: v for k, v in indicator_results.items() if (relevant_lines/ total_lines) * 100 < 60.0}
    if low_performance_indicators:
        elements.append(Paragraph("<b>Consejos para Mejorar:</b>", styles['CenturyGothicBold']))
        elements.append(Spacer(1, 0.05 * inch))
        for indicator, result in low_performance_indicators.items():
            percentage = (relevant_lines/ total_lines)*100
            elements.append(Paragraph(f" {indicator}: ({percentage:.2f}%)", styles['CenturyGothicBold']))
            elements.append(Spacer(1, 0.05 * inch))
            for tip in advice[position].get(indicator, []):
                elements.append(Paragraph(f"  • {tip}", styles['CenturyGothic']))
                elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.2 * inch))

   # Concordancia de items organizada en tabla global con ajuste de texto
    elements.append(Paragraph("<b>Resultados globales:</b>", styles['CenturyGothicBold']))

    elements.append(Spacer(1, 0.2 * inch))

    # Encabezados de la tabla global
    global_table_data = [["Criterio","Funciones del Cargo", "Perfil del Cargo"]]

    # Agregar datos de global_results a la tabla
    global_table_data.append([Paragraph("<b>Concordancia Global</b>", styles['CenturyGothicBold']), f"{global_func_match:.2f}%", f"{global_profile_match:.2f}%"])
    global_table_data.append([Paragraph("<b>Puntaje Global</b>", styles['CenturyGothicBold']), f"{func_score:.2f}", f"{profile_score:.2f}"])

    # Crear la tabla con ancho de columnas ajustado
    global_table = Table(global_table_data, colWidths=[3 * inch, 2 * inch, 2 * inch])

    # Estilos de la tabla con ajuste de texto
    global_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto en encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),  # Fuente para encabezados
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),  # Fuente para el resto de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear texto verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de texto
    ]))

    # Agregar tabla a los elementos
    elements.append(global_table)

    elements.append(Spacer(1, 0.2 * inch))

    # Interpretación de resultados
    elements.append(Paragraph("<b>Interpretación de resultados globales:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.1 * inch))
    if global_profile_match > 75 and global_func_match > 75:
        elements.append(Paragraph(
            f" Alta Concordancia (> 0.75): El análisis revela que {candidate_name} tiene una excelente adecuación con las funciones del cargo de {position} y el perfil buscado. La experiencia detallada en su hoja de vida está estrechamente alineada con las responsabilidades y competencias requeridas para este rol crucial en la prevalencia del Capítulo. La alta concordancia indica que {candidate_name} está bien preparado para asumir este cargo y contribuir significativamente al éxito y la misión del Capítulo. Se recomienda proceder con el proceso de selección y considerar a {candidate_name} como una opción sólida para el cargo.",
            styles['CenturyGothic']
        ))
    elif 60 < global_profile_match <= 75 or 60 < global_func_match <= 75:
        elements.append(Paragraph(
            f" Buena Concordancia (> 0.60): El análisis muestra que {candidate_name} tiene una buena correspondencia con las funciones del cargo de {position} y el perfil deseado. Aunque su experiencia en la asociación es relevante, existe margen para mejorar. {candidate_name} muestra potencial para cumplir con el rol crucial en la prevalencia del Capítulo, pero se recomienda que continúe desarrollando sus habilidades y acumulando más experiencia relacionada con el cargo objetivo. Su candidatura debe ser considerada con la recomendación de enriquecimiento adicional.",
            styles['CenturyGothic']
        ))
    elif 60 < global_profile_match or 60 < global_func_match:
        elements.append(Paragraph(
            f" Baja Concordancia (< 0.60): El análisis indica que {candidate_name} tiene una baja concordancia con los requisitos del cargo de {position} y el perfil buscado. Esto sugiere que aunque el aspirante posee algunas experiencias relevantes, su historial actual no cubre adecuadamente las competencias y responsabilidades necesarias para este rol crucial en la prevalencia del Capítulo. Se aconseja a {candidate_name} enfocarse en mejorar su perfil profesional y desarrollar las habilidades necesarias para el cargo. Este enfoque permitirá a {candidate_name} alinear mejor su perfil con los requisitos del puesto en futuras oportunidades.",
            styles['CenturyGothic']
        ))

    elements.append(Spacer(1, 0.2 * inch))

    # Añadir resultados al reporte
    elements.append(Paragraph("<b>Puntajes totales:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    total_score= (exp_score+ att_score+ org_score+ round_overall_score+ profile_score)/5

    # Crear tabla de evaluación de presentación
    total_table = Table(
        [
            ["Criterio", "Puntaje"],
            ["Experiencia en ANEIAP", f"{exp_score:.2f}"],
            ["Asistencia a eventos", f"{att_score:.2f}"],
            ["Eventos organizados", f"{org_score:.2f}"],
            ["Perfil", f"{prof_score:.2f}"],
            ["Presentación", f"{round_overall_score:.2f}"],
            ["Puntaje Total", f"{total_score:.2f}"]
        ],
        colWidths=[3 * inch, 2 * inch]
    )

    # Estilo de la tabla
    total_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(total_table)

    elements.append(Spacer(1, 0.2 * inch))

    # Generar comentarios para los resultados
    comments = []

    if exp_score >= 4:
        comments.append("Tu experiencia en ANEIAP refleja un nivel destacado, lo que demuestra un conocimiento sólido de la organización y tus contribuciones en actividades clave. Continúa fortaleciendo tu participación para mantener este nivel y destacar aún más.")
    elif exp_score >= 3:
        comments.append("Tu experiencia en ANEIAP es buena, pero podrías enfocarte en profundizar tus contribuciones y participación en actividades clave.")
    else:
        comments.append("Es importante fortalecer tu experiencia en ANEIAP. Considera involucrarte en más actividades y proyectos para adquirir una mayor comprensión y relevancia.")

    if att_score >= 4:
        comments.append("Tu puntuación en asistencia a eventos es excelente. Esto muestra tu compromiso con el aprendizaje y el desarrollo profesional. Mantén esta consistencia participando en eventos relevantes que sigan ampliando tu red de contactos y conocimientos.")
    elif att_score >= 3:
        comments.append("Tu asistencia a eventos es adecuada, pero hay margen para participar más en actividades que refuercen tu aprendizaje y crecimiento profesional.")
    else:
        comments.append("Debes trabajar en tu participación en eventos. La asistencia regular a actividades puede ayudarte a desarrollar habilidades clave y expandir tu red de contactos.")

    if org_score >= 4:
        comments.append("¡Perfecto! Tu desempeño en la organización de eventos es ejemplar. Esto indica habilidades destacadas de planificación, liderazgo y ejecución. Considera compartir tus experiencias con otros miembros para fortalecer el impacto organizacional.")
    elif org_score >= 3:
        comments.append("Tu desempeño en la organización de eventos es bueno, pero podrías centrarte en mejorar la planificación y la ejecución para alcanzar un nivel más destacado.")
    else:
        comments.append("Es importante trabajar en tus habilidades de organización de eventos. Considera involucrarte en proyectos donde puedas asumir un rol de liderazgo y planificación.")

    if prof_score >= 4:
        comments.append("Tu perfil presenta una buena alineación con las expectativas del cargo, destacando competencias clave. Mantén este nivel y continúa fortaleciendo áreas relevantes.")
    elif prof_score >= 3:
        comments.append("El perfil presenta una buena alineación con las expectativas del cargo, aunque hay margen de mejora. Podrías enfocar tus esfuerzos en reforzar áreas específicas relacionadas con las competencias clave del puesto.")
    else:
        comments.append("Tu perfil necesita mejoras para alinearse mejor con las expectativas del cargo. Trabaja en desarrollar habilidades y competencias clave.")

    if round_overall_score >= 4:
        comments.append("La presentación de tu hoja de vida es excelente. Refleja profesionalismo y claridad. Continúa aplicando este enfoque para mantener un alto estándar.")
    elif round_overall_score >= 3:
        comments.append("La presentación de tu hoja de vida es buena, pero puede mejorar en aspectos como coherencia, ortografía o formato general. Dedica tiempo a revisar estos detalles.")
    else:
        comments.append("La presentación de tu hoja de vida necesita mejoras significativas. Asegúrate de revisar la ortografía, la gramática y la coherencia para proyectar una imagen más profesional.")

    if total_score >= 4:
        comments.append("Tu puntaje total indica un desempeño destacado en la mayoría de las áreas. Estás bien posicionado para asumir el rol. Mantén este nivel y busca perfeccionar tus fortalezas.")
    elif total_score >= 3:
        comments.append("Tu puntaje total es sólido, pero hay aspectos que podrían mejorarse. Enfócate en perfeccionar la presentación y el perfil para complementar tus fortalezas en experiencia, eventos y asistencia.")
    else:
        comments.append("El puntaje total muestra áreas importantes por mejorar. Trabaja en fortalecer cada criterio para presentar un perfil más competitivo y completo.")

    # Añadir comentarios al reporte
    elements.append(Paragraph("<b>Comentarios sobre los Resultados:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    for comment in comments:
        elements.append(Paragraph(comment, styles['CenturyGothic']))
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.1 * inch))

    # Conclusión
    elements.append(Paragraph(
        f"Este análisis es generado debido a que es crucial tomar medidas estratégicas para garantizar que  los candidatos estén bien preparados para el rol de {position}. Los aspirantes con alta concordancia deben ser considerados seriamente para el cargo, ya que están en una posición favorable para asumir responsabilidades significativas y contribuir al éxito del Capítulo. Aquellos con buena concordancia deberían continuar desarrollando su experiencia, mientras que los aspirantes con  baja concordancia deberían recibir orientación para mejorar su perfil profesional y acumular más  experiencia relevante. Estas acciones asegurarán que el proceso de selección se base en una evaluación completa y precisa de las capacidades de cada candidato, fortaleciendo la gestión y el  impacto del Capítulo.",
        styles['CenturyGothic']
    ))

    elements.append(Spacer(1, 0.2 * inch))

    # Mensaje de agradecimiento
    elements.append(Paragraph(
        f"Gracias, {candidate_name}, por tu interés en el cargo de {position} ¡Éxitos en tu proceso!",
        styles['CenturyGothic']
    ))

    # Construcción del PDF
    doc.build(elements, onFirstPage=on_first_page, onLaterPages=on_later_pages)

    # Read the PDF file as bytes
    with open(output_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    # Encode PDF bytes to base64 string
    pdf_base64_string = base64.b64encode(pdf_bytes).decode('utf-8')

    return pdf_base64_string, output_path # Return base64 string and report path

def calculate_indicators_for_report_gemini(lines, position, indicator_descriptions): # Añadir indicator_descriptions
    """
    Calcula los porcentajes de relevancia de indicadores para el reporte usando Gemini.
    :param lines: Lista de líneas de la sección relevante del CV.
    :param position: Cargo al que aspira (para obtener las descripciones de indicadores).
    :param indicator_descriptions: Diccionario con descripciones de indicadores para el cargo.
    :return: Diccionario con los porcentajes por indicador y detalles de líneas relevantes.
    """
    indicator_results = {}
    for indicator, description_list in indicator_descriptions.items(): # Iterar sobre descriptions
        if description_list: # Asegurarse de que la lista de descripciones no esté vacía
            indicator_description = description_list[0] # Tomar la primera descripción como ejemplo (puedes ajustarlo)
        else:
            print(f"⚠️ No se encontró descripción para el indicador '{indicator}' en advice.json para el cargo '{position}'.")
            indicator_description = f"Indicador: {indicator}." # Descripción genérica si no se encuentra

        relevant_lines_count = 0
        for line in lines:
            if is_relevant_for_indicator_gemini(line, indicator_description, indicator=indicator, position=position): # Pasar indicator e position
                relevant_lines_count += 1

        total_lines = len(lines)
        percentage = (relevant_lines_count / total_lines) * 100 if total_lines > 0 else 0
        indicator_results[indicator] = {"percentage": percentage, "relevant_lines": relevant_lines_count}
    return indicator_results


def is_relevant_for_indicator_gemini(line, indicator_description, indicator, position): # Añadir indicator y position
    """
    Determina si una línea de texto es semánticamente relevante para un indicador usando Gemini.
    :param line: Línea de texto del CV a evaluar.
    :param indicator_description: Descripción del indicador (desde advice.json).
    :param indicator: Nombre del indicador (para debugging).
    :param position: Cargo (para debugging).
    """
    if not line or not indicator_description:
        return False

    try:
        model = genai.GenerativeModel(MODELO_GEMINI)
        prompt = f"""
            Instrucciones: Eres un evaluador de hojas de vida. Determina si la siguiente línea de texto de una hoja de vida es **relevante** para el siguiente indicador, basándote en su descripción. Responde **'Sí'** o **'No'** solamente.

            Cargo del candidato: {position}
            Indicador a evaluar: {indicator}
            Descripción del indicador: {indicator_description}

            Línea de texto de la hoja de vida:
            {line}

            ¿Es relevante la línea de texto para el indicador? (Responde 'Sí' o 'No'):
            """
        response = model.generate_content([prompt])
        respuesta_texto = response.text.strip().lower()
        return "sí" in respuesta_texto or "yes" in respuesta_texto

    except Exception as e:
        print(f"⚠️ Error al usar Gemini para is_relevant_for_indicator_gemini (Indicador: {indicator}, Cargo: {position}): {e}")
        return False


def generate_report_with_background_api(pdf_path, position, candidate_name,background_path, chapter):
    """
    Genera un reporte con un fondo en cada página for API usage, returns base64 encoded PDF.
    :param pdf_path: Ruta del PDF.
    :param position: Cargo al que aspira.
    :param candidate_name: Nombre del candidato.
    :param background_path: Ruta de la imagen de fondo.
    :param chapter: Capítulo del Candidato
    :return: base64 encoded PDF content and report path
    """
    experience_text = extract_experience_section_with_ocr(pdf_path)
    if not experience_text:
        return None, "No se encontró la sección 'EXPERIENCIA EN ANEIAP' en el PDF."

    org_text = extract_event_section_with_ocr(pdf_path)
    if not org_text:
        return None, "No se encontró la sección 'EVENTOS ORGANIZADOS' en el PDF."

    att_text = extract_attendance_section_with_ocr(pdf_path)
    if not att_text:
        return None, "No se encontró la sección 'Asistencia a Eventos ANEIAP' en el PDF."

    resume_text= evaluate_cv_presentation(pdf_path)
    if not resume_text:
        return None, "No se encontró el texto de la hoja de vida"

    candidate_profile_text= extract_profile_section_with_ocr(pdf_path)
    if not candidate_profile_text:
        return None, "No se encontró la sección 'Perfil' en el PDF."

    # Dividir la experiencia en líneas
    lines = extract_cleaned_lines(experience_text)
    lines= experience_text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]  # Eliminar líneas vacías

    # Dividir los eventos en líneas
    org_lines = extract_cleaned_lines(org_text)
    org_lines= org_text.split("\n")
    org_lines = [line.strip() for line in org_lines if line.strip()]  # Eliminar líneas vacías

    #Dividir lineas de perfil
    candidate_profile_lines = extract_cleaned_lines(candidate_profile_text)
    candidate_profile_lines= candidate_profile_text.split("\n")
    candidate_profile_lines= [line.strip() for line in candidate_profile_lines if line.strip()]

    # Dividir la asistencia en líneas
    att_lines = extract_cleaned_lines(att_text)
    att_lines= att_text.split("\n")
    att_lines = [line.strip() for line in att_lines if line.strip()]  # Eliminar líneas vacías

    # Obtener los indicadores y palabras clave para el cargo seleccionado
    position_indicators = indicators.get(position, {})
    position_advice = advice.get(position, {}) # Cargar advice para el cargo

    #indicator_results = calculate_all_indicators(lines, position_indicators) #REEMPLAZAR POR VERSION GEMINI
    indicator_results = calculate_indicators_for_report_gemini(lines, position, position_advice) # Usar función Gemini para indicadores

    # Cargar funciones y perfil
    try:
        with fitz.open(f"Funciones//F{position}.pdf") as func_doc:
            functions_text = func_doc[0].get_text()
        with fitz.open(f"Perfiles/P{position}.pdf") as profile_doc:
            profile_text = profile_doc[0].get_text()
    except Exception as e:
        return None, f"Error al cargar funciones o perfil: {e}"

    line_results = []
    org_line_results = []
    att_line_results = []

    # Evaluación de renglones de EXPERIENCIA EN ANEIAP
    # Evaluación de renglones
    for line in lines:
        line = line.strip()
        if not line:  # Ignorar líneas vacías
            continue

        # Dividir la experiencia en líneas
        lines = extract_cleaned_lines(experience_text)
        lines = experience_text.split("\n")
        lines = [line.strip() for line in lines if line.strip()]  # Eliminar líneas vacías

        # Obtener los indicadores y palabras clave para el cargo seleccionado
        position_indicators = indicators.get(position, {})
        indicator_results = {}

        # Calcular el porcentaje por cada indicador
        indicator_results = calculate_indicators_for_report(lines, position_indicators)
        for indicator, keywords in position_indicators.items():
            indicator_results = calculate_indicators_for_report(lines, position_indicators)

        # Calcular la presencia total (si es necesario)
        total_presence = sum(result["percentage"] for result in indicator_results.values())

        # Normalizar los porcentajes si es necesario
        if total_presence > 0:
            for indicator in indicator_results:
                indicator_results[indicator]["percentage"] = (indicator_results[indicator]["percentage"] / total_presence) * 100

        # Evaluación general de concordancia
        if any(keyword.lower() in line.lower() for kw_set in position_indicators.values() for keyword in kw_set):
            func_match = 100.0
            profile_match = 100.0
        else:
            # Calcular similitud
            func_match = calculate_similarity(line, functions_text)
            profile_match = calculate_similarity(line, profile_text)

        # Solo agregar al reporte si no tiene 0% en ambas métricas
        if func_match > 0 or profile_match > 0:
            line_results.append((line, func_match, profile_match))

    # Normalización de los resultados de indicadores
    total_presence = sum(indicator["percentage"] for indicator in indicator_results.values())
    if total_presence > 0:
        for indicator in indicator_results:
            indicator_results[indicator]["percentage"] = (indicator_results[indicator]["percentage"] / total_presence) * 100

    # Evaluación de renglones eventos organizados
    for line in org_lines:
        line = line.strip()
        if not line:  # Ignorar líneas vacías
            continue

        # Dividir los eventos en líneas
        org_lines = extract_cleaned_lines(org_text)
        org_lines= att_text.split("\n")
        org_lines = [line.strip() for line in org_lines if line.strip]

        # Evaluación general de concordancia
        if any(keyword.lower() in line.lower() for kw_set in position_indicators.values() for keyword in kw_set):
            org_func_match = 100.0
            org_profile_match = 100.0
        else:
            # Calcular similitud
            org_func_match = calculate_similarity(line, functions_text)
            org_profile_match = calculate_similarity(line, profile_text)

        # Solo agregar al reporte si no tiene 0% en ambas métricas
        if org_func_match > 0 or org_profile_match > 0:
            org_line_results.append((line, org_func_match, org_profile_match))

    # Evaluación de renglones asistencia a eventos
    for line in att_lines:
        line = line.strip()
        if not line:  # Ignorar líneas vacías
            continue

        # Dividir los asistencia en líneas
        att_lines = extract_cleaned_lines(att_text)
        att_lines= att_text.split("\n")
        att_lines = [line.strip() for line in att_lines if line.strip]

        # Evaluación general de concordancia
        if any(keyword.lower() in line.lower() for kw_set in position_indicators.values() for keyword in kw_set):
            att_func_match = 100.0
            att_profile_match = 100.0
        else:
            # Calcular similitud
            att_func_match = calculate_similarity(line, functions_text)
            att_profile_match = calculate_similarity(line, profile_text)

        # Solo agregar al reporte si no tiene 0% en ambas métricas
        if att_func_match > 0 or att_profile_match > 0:
            att_line_results.append((line, att_func_match, att_profile_match))

    # Calcular porcentajes de concordancia con perfil de candidato
    keyword_count = 0
    words = re.findall(r"\b\w+\b", candidate_profile_text)
    total_words = len(words)
    for kw_set in position_indicators.values():
        for keyword in kw_set:
            keyword_count += candidate_profile_text.count(keyword)

    prop_keyword= keyword_count/total_words

    # Evitar división por cero
    if prop_keyword<= 0.01:
        keyword_match_percentage = 0
    elif 0.01 <prop_keyword <= 0.15:
        keyword_match_percentage = 25
    elif 0.15 <prop_keyword <= 0.5:
        keyword_match_percentage = 50
    elif 0.5 <prop_keyword <= 0.75:
        keyword_match_percentage = 75
    else:
        keyword_match_percentage = 100

    # Evaluación de concordancia basada en palabras clave
    if keyword_match_percentage == 100:
        profile_func_match = 100.0
        profile_profile_match = 100.0
    else:
        # Calcular similitud con funciones y perfil del cargo si la coincidencia es baja
        prof_func_match = calculate_similarity(candidate_profile_text, functions_text)
        prof_profile_match = calculate_similarity(candidate_profile_text, profile_text)
        profile_func_match = keyword_match_percentage + prof_func_match
        profile_profile_match = keyword_match_percentage + prof_profile_match

    # Calcular porcentajes parciales respecto a la Experiencia ANEIAP
    if line_results:  # Evitar división por cero si no hay ítems válidos
        parcial_exp_func_match = sum([res[1] for res in line_results]) / len(line_results)
        parcial_exp_profile_match = sum([res[2] for res in line_results]) / len(line_results)
    else:
        parcial_exp_func_match = 0
        parcial_exp_profile_match = 0

    # Calcular porcentajes parciales respecto a los Eventos ANEIAP
    if org_line_results:  # Evitar división por cero si no hay ítems válidos
        parcial_org_func_match = sum([res[1] for res in org_line_results]) / len(org_line_results)
        parcial_org_profile_match = sum([res[2] for res in org_line_results]) / len(org_line_results)
    else:
        parcial_org_func_match = 0
        parcial_org_profile_match = 0

    # Calcular porcentajes parciales respecto a la asistencia a eventos
    if att_line_results:  # Evitar división por cero si no hay ítems válidos
        parcial_att_func_match = sum([res[1] for res in att_line_results]) / len(att_line_results)
        parcial_att_profile_match = sum([res[2] for res in att_line_results]) / len(att_line_results)
    else:
        parcial_att_func_match = 0
        parcial_att_profile_match = 0

    resume_text= evaluate_cv_presentation(pdf_path)

    # Inicializar corrector ortográfico
    spell = SpellChecker(language='es')

    punctuation_errors = 0

    for i, line in enumerate(lines):
        # Verificar si la oración termina con puntuación válida
        if not line.endswith((".", "!", "?")):
            punctuation_errors += 1

    # Limpiar y dividir el texto en líneas
    pres_cleaned_lines = [line.strip() for line in resume_text.split("\n") if line.strip()]
    total_lines = len(pres_cleaned_lines)

    # Métricas
    total_words = 0
    spelling_errors = 0
    missing_capitalization = 0
    incomplete_sentences = 0
    punctuation_marks = 0
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

        # Gramática básica: verificar patrones comunes (ejemplo)
        grammar_errors += len(re.findall(r'\b(?:es|está|son)\b [^\w\s]', line))  # Ejemplo: "es" sin continuación válida

    # Calcular métricas secundarias
    spelling = 1- (spelling_errors / total_words)
    capitalization_score = 1- (missing_capitalization / total_lines)
    sentence_completion_score = 1- (incomplete_sentences / total_lines)
    grammar = 1- (grammar_errors / total_lines)
    punctuation_error_rate = 1- (punctuation_errors / total_lines)

    #Calcular métricas principales
    grammar_score = round(((punctuation_error_rate+ grammar+ sentence_completion_score)/3)*5, 2)
    spelling_score= round(((spelling+ capitalization_score)/2)*5,2)

    if total_lines == 0:
        return 100  # Si no hay oraciones, asumimos coherencia perfecta.

    # Calcular métricas coherencia
    # 1. Repetición de palabras
    def calculate_word_repetition(pres_cleaned_lines):
        repeated_words = Counter()
        for line in pres_cleaned_lines:
            words = line.split()
            repeated_words.update([word.lower() for word in words])

        total_words = sum(repeated_words.values())
        unique_words = len(repeated_words)
        most_common_word_count = repeated_words.most_common(1)[0][1] if repeated_words else 0
        repeated_word_ratio = (most_common_word_count / total_words) if total_words > 0 else 0

        # Una menor repetición indica mayor calidad
        repetition_score = 1 - repeated_word_ratio
        return repetition_score, repeated_words

    # 2. Fluidez entre oraciones
    def calculate_sentence_fluency(pres_cleaned_lines):
        """
        Calcula el puntaje de fluidez de las oraciones basándose en conectores lógicos, puntuación,
        y variabilidad en la longitud de las oraciones.
        :param pres_cleaned_lines: Lista de líneas limpias del texto.
        :return: Puntaje de fluidez de las oraciones entre 0 y 1.
        """
        # Lista de conectores lógicos comunes
        logical_connectors = {
        "adición": [
            "además", "también", "asimismo", "igualmente", "de igual manera",
            "por otro lado", "de la misma forma", "junto con"
        ],
        "causa": [
            "porque", "ya que", "debido a", "dado que", "por motivo de",
            "gracias a", "en razón de", "a causa de"
        ],
        "consecuencia": [
            "por lo tanto", "así que", "en consecuencia", "como resultado",
            "por esta razón", "de modo que", "lo que permitió", "de ahí que"
        ],
        "contraste": [
            "sin embargo", "pero", "aunque", "no obstante", "a pesar de",
            "por el contrario", "en cambio", "si bien", "mientras que"
        ],
        "condición": [
            "si", "en caso de", "a menos que", "siempre que", "con la condición de",
            "a no ser que", "en el supuesto de que"
        ],
        "tiempo": [
            "mientras", "cuando", "después de", "antes de", "al mismo tiempo",
            "posteriormente", "una vez que", "simultáneamente", "en el transcurso de"
        ],
        "descripción de funciones": [
            "encargado de", "responsable de", "mis funciones incluían",
            "lideré", "gestioné", "coordiné", "dirigí", "supervisé",
            "desarrollé", "planifiqué", "ejecuté", "implementé", "organicé"
        ],
        "logros y resultados": [
            "logré", "alcancé", "conseguí", "incrementé", "reduje",
            "optimizé", "mejoré", "aumenté", "potencié", "maximicé",
            "contribuí a", "obtuve", "permitió mejorar", "impactó positivamente en"
        ],
        "secuencia": [
            "primero", "en primer lugar", "a continuación", "luego", "después",
            "seguidamente", "posteriormente", "finalmente", "por último"
        ],
        "énfasis": [
            "sobre todo", "en particular", "especialmente", "principalmente",
            "específicamente", "vale la pena destacar", "conviene resaltar",
            "cabe mencionar", "es importante señalar"
        ],
        "conclusión": [
            "en resumen", "para concluir", "en definitiva", "en síntesis",
            "como conclusión", "por ende", "por consiguiente", "para finalizar"
        ]
    }
        connector_count = 0
        total_lines = len(pres_cleaned_lines)

        # Validación para evitar divisiones por cero
        if total_lines == 0:
            return 0  # Sin líneas, no se puede calcular fluidez

        # Inicialización de métricas
        punctuation_errors = 0
        sentence_lengths = []

        for line in pres_cleaned_lines:
            # Verificar errores de puntuación (oraciones sin punto final)
            if not line.endswith((".", "!", "?")):
                punctuation_errors += 1

            # Almacenar la longitud de cada oración
            sentence_lengths.append(len(line.split()))

            # Contar conectores lógicos en la línea
            for connector in logical_connectors:
                if connector in line.lower():
                    connector_count += 1

        # Calcular métricas individuales
        avg_length = sum(sentence_lengths) / total_lines
        length_variance = sum(
            (len(line.split()) - avg_length) ** 2 for line in pres_cleaned_lines
        ) / total_lines if total_lines > 1 else 0

        # Normalizar métricas entre 0 y 1
        punctuation_score = max(0, 1 - (punctuation_errors / total_lines))  # 1 si no hay errores
        connector_score = min(1, connector_count / total_lines)  # Máximo 1, basado en conectores
        variance_penalty = max(0, 1 - length_variance / avg_length) if avg_length > 0 else 0

        # Calcular puntaje final de fluidez
        fluency_score = (punctuation_score + connector_score + variance_penalty) / 3
        return round(fluency_score, 2)


    # Calcular métricas individuales
    repetition_score, repeated_words = calculate_word_repetition(pres_cleaned_lines)
    fluency_score = calculate_sentence_fluency(pres_cleaned_lines)

    # Asegurar que repetition_score y fluency_score están entre 0 y 1 antes de la conversión
    normalized_repetition_score = min(1, max(0, repetition_score))
    normalized_fluency_score = min(1, max(0, fluency_score))

    # Calcular coherencia asegurando que el resultado final no pase de 5
    coherence_score = round(min(5, (normalized_repetition_score + normalized_fluency_score) * 2.5), 2)

    # Puntaje general ponderado
    overall_score = round((spelling_score  + coherence_score + grammar_score) / 3, 2)

    # Calculo puntajes parciales
    parcial_exp_func_score = round((parcial_exp_func_match * 5) / 100, 2)
    parcial_exp_profile_score = round((parcial_exp_profile_match * 5) / 100, 2)
    parcial_org_func_score = round((parcial_org_func_match * 5) / 100, 2)
    parcial_org_profile_score = round((parcial_org_profile_match * 5) / 100, 2)
    parcial_att_func_score = round((parcial_att_func_match * 5) / 100, 2)
    parcial_att_profile_score = round((parcial_att_profile_match * 5) / 100, 2)
    profile_func_score= round((profile_func_match * 5) / 100, 2)
    profile_profile_score= round((profile_profile_match * 5) / 100, 2)

    #Calcular resultados globales
    global_func_match = (parcial_exp_func_match + parcial_att_func_match + parcial_org_func_match+ profile_func_match) / 4
    global_profile_match = (parcial_exp_profile_match + parcial_att_profile_match + parcial_org_profile_match + profile_profile_match) / 4
    func_score = round((global_func_match * 5) / 100, 2)
    profile_score = round((global_profile_match * 5) / 100, 2)

    #Calculo puntajes totales
    exp_score= (parcial_exp_func_score+ parcial_exp_profile_score)/2
    org_score= (parcial_org_func_score+ parcial_org_profile_score)/2
    att_score= (parcial_att_func_score+ parcial_att_profile_score)/2
    prof_score= (profile_func_score+ profile_profile_score)/2
    total_score= (overall_score+ exp_score+ org_score+ att_score+ profile_score)/5

    # Registrar la fuente personalizada
    pdfmetrics.registerFont(TTFont('CenturyGothic', 'Century_Gothic.ttf'))
    pdfmetrics.registerFont(TTFont('CenturyGothicBold', 'Century_Gothic_Bold.ttf'))

    # Estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CenturyGothic", fontName="CenturyGothic", fontSize=12, leading=14, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name="CenturyGothicBold", fontName="CenturyGothicBold", fontSize=12, leading=14, alignment=TA_JUSTIFY))

    # Crear el documento PDF
    report_path = f"Reporte_analisis_cargo_{candidate_name}_{position}_{chapter}.pdf"
    doc = SimpleDocTemplate(report_path, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=100, bottomMargin=72)

    # Lista de elementos para el reporte
    elements = []

    # 📌 **3️⃣ AGREGAR PORTADA SIN FONDO**
    def on_first_page(canvas, doc):
        """Dibuja una portada que ocupa toda la página."""
        draw_full_page_cover(canvas, portada_path, candidate_name, position, chapter)

    # Título del reporte centrado
    title_style = ParagraphStyle(name='CenteredTitle', fontName='CenturyGothicBold', fontSize=14, leading=16, alignment=1,  # 1 significa centrado, textColor=colors.black
                                )
    # Convertir texto a mayúsculas
    elements.append(PageBreak())
    title_candidate_name = candidate_name.upper()
    title_position = position.upper()
    tittle_chapter= chapter.upper()

    elements.append(Paragraph(f"REPORTE DE ANÁLISIS {title_candidate_name} CARGO {title_position} {tittle_chapter}", title_style))

    elements.append(Spacer(1, 0.2 * inch))

    # Concordancia de items organizada en tabla con ajuste de texto
    elements.append(Paragraph("<b>Análisis de perfil de aspirante:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    # Encabezados de la tabla
    prof_table_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]

    #Agregar resultados parciales
    prof_table_data.append([Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']), f"{profile_func_match:.2f}%", f"{profile_profile_match:.2f}%"])
    prof_table_data.append([Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']), f"{profile_func_score:.2f}", f"{profile_profile_score:.2f}"])

    # Crear la tabla con ancho de columnas ajustado
    prof_item_table = Table(prof_table_data, colWidths=[3 * inch, 2 * inch, 2 * inch])

    # Estilos de la tabla con ajuste de texto
    prof_item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto en encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),  # Fuente para encabezados
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),  # Fuente para el resto de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear texto verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de texto
    ]))

    # Agregar tabla a los elementos
    elements.append(prof_item_table)

    elements.append(Spacer(1, 0.2 * inch))

    # Concordancia de items organizada en tabla con ajuste de texto
    elements.append(Paragraph("<b>Análisis de ítems de asistencia a eventos:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    # Encabezados de la tabla
    att_table_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]

    # Agregar datos de line_results a la tabla
    for line, att_func_match, att_profile_match in att_line_results:
        att_table_data.append([Paragraph(line, styles['CenturyGothic']), f"{att_func_match:.2f}%", f"{att_profile_match:.2f}%"])

    #Agregar resultados parciales
    att_table_data.append([Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']), f"{parcial_att_func_match:.2f}%", f"{parcial_att_profile_match:.2f}%"])
    att_table_data.append([Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']), f"{parcial_att_func_score:.2f}", f"{parcial_att_profile_score:.2f}"])

    # Crear la tabla con ancho de columnas ajustado
    att_item_table = Table(att_table_data, colWidths=[3 * inch, 2 * inch, 2 * inch])

    # Estilos de la tabla con ajuste de texto
    att_item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto en encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),  # Fuente para encabezados
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),  # Fuente para el resto de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear texto verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de texto
    ]))

    # Agregar tabla a los elementos
    elements.append(att_item_table)

    elements.append(Spacer(1, 0.1 * inch))

    # Total de líneas analizadas en ASISTENCIA A EVENTOS ANEIAP
    att_total_lines = len(att_line_results)
    elements.append(Paragraph(f"• Total de asistencias a eventos analizadas: {att_total_lines}", styles['CenturyGothicBold']))

    elements.append(Spacer(1, 0.2 * inch))

    # Concordancia de items organizada en tabla con ajuste de texto
    elements.append(Paragraph("<b>Análisis de ítems de eventos organizados:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    # Encabezados de la tabla
    org_table_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]

    # Agregar datos de line_results a la tabla
    for line, org_func_match, org_profile_match in org_line_results:
        org_table_data.append([Paragraph(line, styles['CenturyGothic']), f"{org_func_match:.2f}%", f"{org_profile_match:.2f}%"])

    #Agregar resultados parciales
    org_table_data.append([Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']), f"{parcial_org_func_match:.2f}%", f"{parcial_org_profile_match:.2f}%"])
    org_table_data.append([Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']), f"{parcial_org_func_score:.2f}", f"{parcial_org_profile_score:.2f}"])

    # Crear la tabla con ancho de columnas ajustado
    org_item_table = Table(org_table_data, colWidths=[3 * inch, 2 * inch, 2 * inch])

    # Estilos de la tabla con ajuste de texto
    org_item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto en encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),  # Fuente para encabezados
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),  # Fuente para el resto de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear texto verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de texto
    ]))

    # Agregar tabla a los elementos
    elements.append(org_item_table)

    elements.append(Spacer(1, 0.1 * inch))

    # Total de líneas analizadas en ASISTENCIA A EVENTOS ANEIAP
    org_total_lines = len(org_line_results)
    elements.append(Paragraph(f"• Total de eventos analizados: {org_total_lines}", styles['CenturyGothicBold']))

    elements.append(Spacer(1, 0.2 * inch))

    # Concordancia de items organizada en tabla con ajuste de texto
    elements.append(Paragraph("<b>Análisis de ítems:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    # Encabezados de la tabla
    table_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]

    # Agregar datos de line_results a la tabla
    for line, exp_func_match, exp_profile_match in line_results:
        table_data.append([Paragraph(line, styles['CenturyGothic']), f"{exp_func_match:.2f}%", f"{exp_profile_match:.2f}%"])

    #Agregar resultados parciales
    table_data.append([Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']), f"{parcial_exp_func_match:.2f}%", f"{parcial_exp_profile_match:.2f}%"])
    table_data.append([Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']), f"{parcial_exp_func_score:.2f}", f"{parcial_exp_profile_score:.2f}"])

    # Crear la tabla con ancho de columnas ajustado
    item_table = Table(table_data, colWidths=[3 * inch, 2 * inch, 2 * inch])

    # Estilos de la tabla con ajuste de texto
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto en encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),  # Fuente para encabezados
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),  # Fuente para el resto de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear texto verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de texto
    ]))

    # Agregar tabla a los elementos
    elements.append(item_table)

    elements.append(Spacer(1, 0.2 * inch))

    # Total de líneas analizadas en EXPERIENCIA EN ANEIAP
    total_lines = len(line_results)
    elements.append(Paragraph(f"• Total de experiencias analizadas: {total_lines}", styles['CenturyGothicBold']))

    elements.append(Spacer(1, 0.2 * inch))

    # Añadir resultados al reporte
    elements.append(Paragraph("<b>Evaluación de la Presentación:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    # Crear tabla de evaluación de presentación
    presentation_table = Table(
        [
            ["Criterio", "Puntaje"],
            ["Coherencia", f"{coherence_score:.2f}"],
            ["Ortografía", f"{spelling_score:.2f}"],
            ["Gramática", f"{grammar_score:.2f}"],
            ["Puntaje Total", f"{overall_score:.2f}"]
        ],
        colWidths=[3 * inch, 2 * inch]
    )

    # Estilo de la tabla
    presentation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(presentation_table)

    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("<b>Consejos para mejorar la presentación de la hoja de vida:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Spacer(1, 0.2 * inch))
    # Concordancia de items organizada en tabla con ajuste de texto
    elements.append(Paragraph("<b>Resultados de indicadores:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    # Encabezados de la tabla
    table_indicator = [["Indicador", "Concordancia (%)"]]

    # Agregar datos de line_results a la tabla
    for indicator, data in indicator_results.items():
        relevant_lines = sum(
            any(keyword.lower() in line.lower() for keyword in keywords) for line in lines
        )
        total_lines = len(line_results)
        percentage = (relevant_lines / total_lines) * 100 if total_lines > 0 else 0
        if isinstance(percentage, (int, float)):  # Validar que sea un número
            table_indicator.append([Paragraph(indicator, styles['CenturyGothic']), f"{percentage:.2f}%"])

    # Crear la tabla con ancho de columnas ajustado
    indicator_table = Table(table_indicator, colWidths=[3 * inch, 2 * inch, 2 * inch])

    # Estilos de la tabla con ajuste de texto
    indicator_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto en encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),  # Fuente para encabezados
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),  # Fuente para el resto de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear texto verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de texto
    ]))

    # Agregar tabla a los elementos
    elements.append(indicator_table)

    elements.append(Spacer(1, 0.2 * inch))

    # Consejos para mejorar indicadores con baja presencia
    low_performance_indicators = {k: v for k, v in indicator_results.items() if (relevant_lines/ total_lines) * 100 < 60.0}
    if low_performance_indicators:
        elements.append(Paragraph("<b>Consejos para Mejorar:</b>", styles['CenturyGothicBold']))
        elements.append(Spacer(1, 0.05 * inch))
        for indicator, result in low_performance_indicators.items():
            percentage = (relevant_lines/ total_lines)*100
            elements.append(Paragraph(f" {indicator}: ({percentage:.2f}%)", styles['CenturyGothicBold']))
            elements.append(Spacer(1, 0.05 * inch))
            for tip in advice[position].get(indicator, []):
                elements.append(Paragraph(f"  • {tip}", styles['CenturyGothic']))
                elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.2 * inch))

   # Concordancia de items organizada en tabla global con ajuste de texto
    elements.append(Paragraph("<b>Resultados globales:</b>", styles['CenturyGothicBold']))

    elements.append(Spacer(1, 0.2 * inch))

    # Encabezados de la tabla global
    global_table_data = [["Criterio","Funciones del Cargo", "Perfil del Cargo"]]

    # Agregar datos de global_results a la tabla
    global_table_data.append([Paragraph("<b>Concordancia Global</b>", styles['CenturyGothicBold']), f"{global_func_match:.2f}%", f"{global_profile_match:.2f}%"])
    global_table_data.append([Paragraph("<b>Puntaje Global</b>", styles['CenturyGothicBold']), f"{func_score:.2f}", f"{profile_score:.2f}"])

    # Crear la tabla con ancho de columnas ajustado
    global_table = Table(global_table_data, colWidths=[3 * inch, 2 * inch, 2 * inch])

    # Estilos de la tabla con ajuste de texto
    global_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Fondo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Color de texto en encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),  # Fuente para encabezados
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),  # Fuente para el resto de la tabla
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear texto verticalmente al centro
        ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de texto
    ]))

    # Agregar tabla a los elementos
    elements.append(global_table)

    elements.append(Spacer(1, 0.2 * inch))

    # Interpretación de resultados
    elements.append(Paragraph("<b>Interpretación de resultados globales:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.1 * inch))
    if global_profile_match > 75 and global_func_match > 75:
        elements.append(Paragraph(
            f" Alta Concordancia (> 0.75): El análisis revela que {candidate_name} tiene una excelente adecuación con las funciones del cargo de {position} y el perfil buscado. La experiencia detallada en su hoja de vida está estrechamente alineada con las responsabilidades y competencias requeridas para este rol crucial en la prevalencia del Capítulo. La alta concordancia indica que {candidate_name} está bien preparado para asumir este cargo y contribuir significativamente al éxito y la misión del Capítulo. Se recomienda proceder con el proceso de selección y considerar a {candidate_name} como una opción sólida para el cargo.",
            styles['CenturyGothic']
        ))
    elif 60 < global_profile_match <= 75 or 60 < global_func_match <= 75:
        elements.append(Paragraph(
            f" Buena Concordancia (> 0.60): El análisis muestra que {candidate_name} tiene una buena correspondencia con las funciones del cargo de {position} y el perfil deseado. Aunque su experiencia en la asociación es relevante, existe margen para mejorar. {candidate_name} muestra potencial para cumplir con el rol crucial en la prevalencia del Capítulo, pero se recomienda que continúe desarrollando sus habilidades y acumulando más experiencia relacionada con el cargo objetivo. Su candidatura debe ser considerada con la recomendación de enriquecimiento adicional.",
            styles['CenturyGothic']
        ))
    elif 60 < global_profile_match or 60 < global_func_match:
        elements.append(Paragraph(
            f" Baja Concordancia (< 0.60): El análisis indica que {candidate_name} tiene una baja concordancia con los requisitos del cargo de {position} y el perfil buscado. Esto sugiere que aunque el aspirante posee algunas experiencias relevantes, su historial actual no cubre adecuadamente las competencias y responsabilidades necesarias para este rol crucial en la prevalencia del Capítulo. Se aconseja a {candidate_name} enfocarse en mejorar su perfil profesional y desarrollar las habilidades necesarias para el cargo. Este enfoque permitirá a {candidate_name} alinear mejor su perfil con los requisitos del puesto en futuras oportunidades.",
            styles['CenturyGothic']
        ))

    elements.append(Spacer(1, 0.2 * inch))

    # Añadir resultados al reporte
    elements.append(Paragraph("<b>Puntajes totales:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))

    total_score= (exp_score+ att_score+ org_score+ round_overall_score+ profile_score)/5

    # Crear tabla de evaluación de presentación
    total_table = Table(
        [
            ["Criterio", "Puntaje"],
            ["Experiencia en ANEIAP", f"{exp_score:.2f}"],
            ["Asistencia a eventos", f"{att_score:.2f}"],
            ["Eventos organizados", f"{org_score:.2f}"],
            ["Perfil", f"{prof_score:.2f}"],
            ["Presentación", f"{round_overall_score:.2f}"],
            ["Puntaje Total", f"{total_score:.2f}"]
        ],
        colWidths=[3 * inch, 2 * inch]
    )

    # Estilo de la tabla
    total_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(total_table)

    elements.append(Spacer(1, 0.2 * inch))

    # Generar comentarios para los resultados
    comments = []

    if exp_score >= 4:
        comments.append("Tu experiencia en ANEIAP refleja un nivel destacado, lo que demuestra un conocimiento sólido de la organización y tus contribuciones en actividades clave. Continúa fortaleciendo tu participación para mantener este nivel y destacar aún más.")
    elif exp_score >= 3:
        comments.append("Tu experiencia en ANEIAP es buena, pero podrías enfocarte en profundizar tus contribuciones y participación en actividades clave.")
    else:
        comments.append("Es importante fortalecer tu experiencia en ANEIAP. Considera involucrarte en más actividades y proyectos para adquirir una mayor comprensión y relevancia.")

    if att_score >= 4:
        comments.append("Tu puntuación en asistencia a eventos es excelente. Esto muestra tu compromiso con el aprendizaje y el desarrollo profesional. Mantén esta consistencia participando en eventos relevantes que sigan ampliando tu red de contactos y conocimientos.")
    elif att_score >= 3:
        comments.append("Tu asistencia a eventos es adecuada, pero hay margen para participar más en actividades que refuercen tu aprendizaje y crecimiento profesional.")
    else:
        comments.append("Debes trabajar en tu participación en eventos. La asistencia regular a actividades puede ayudarte a desarrollar habilidades clave y expandir tu red de contactos.")

    if org_score >= 4:
        comments.append("¡Perfecto! Tu desempeño en la organización de eventos es ejemplar. Esto indica habilidades destacadas de planificación, liderazgo y ejecución. Considera compartir tus experiencias con otros miembros para fortalecer el impacto organizacional.")
    elif org_score >= 3:
        comments.append("Tu desempeño en la organización de eventos es bueno, pero podrías centrarte en mejorar la planificación y la ejecución para alcanzar un nivel más destacado.")
    else:
        comments.append("Es importante trabajar en tus habilidades de organización de eventos. Considera involucrarte en proyectos donde puedas asumir un rol de liderazgo y planificación.")

    if prof_score >= 4:
        comments.append("Tu perfil presenta una buena alineación con las expectativas del cargo, destacando competencias clave. Mantén este nivel y continúa fortaleciendo áreas relevantes.")
    elif prof_score >= 3:
        comments.append("El perfil presenta una buena alineación con las expectativas del cargo, aunque hay margen de mejora. Podrías enfocar tus esfuerzos en reforzar áreas específicas relacionadas con las competencias clave del puesto.")
    else:
        comments.append("Tu perfil necesita mejoras para alinearse mejor con las expectativas del cargo. Trabaja en desarrollar habilidades y competencias clave.")

    if round_overall_score >= 4:
        comments.append("La presentación de tu hoja de vida es excelente. Refleja profesionalismo y claridad. Continúa aplicando este enfoque para mantener un alto estándar.")
    elif round_overall_score >= 3:
        comments.append("La presentación de tu hoja de vida es buena, pero puede mejorar en aspectos como coherencia, ortografía o formato general. Dedica tiempo a revisar estos detalles.")
    else:
        comments.append("La presentación de tu hoja de vida necesita mejoras significativas. Asegúrate de revisar la ortografía, la gramática y la coherencia para proyectar una imagen más profesional.")

    if total_score >= 4:
        comments.append("Tu puntaje total indica un desempeño destacado en la mayoría de las áreas. Estás bien posicionado para asumir el rol. Mantén este nivel y busca perfeccionar tus fortalezas.")
    elif total_score >= 3:
        comments.append("Tu puntaje total es sólido, pero hay aspectos que podrían mejorarse. Enfócate en perfeccionar la presentación y el perfil para complementar tus fortalezas en experiencia, eventos y asistencia.")
    else:
        comments.append("El puntaje total muestra áreas importantes por mejorar. Trabaja en fortalecer cada criterio para presentar un perfil más competitivo y completo.")

    # Añadir comentarios al reporte
    elements.append(Paragraph("<b>Comentarios sobre los Resultados:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    for comment in comments:
        elements.append(Paragraph(comment, styles['CenturyGothic']))
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.1 * inch))

    # Conclusión
    elements.append(Paragraph(
        f"Este análisis es generado debido a que es crucial tomar medidas estratégicas para garantizar que  los candidatos estén bien preparados para el rol de {position}. Los aspirantes con alta concordancia deben ser considerados seriamente para el cargo, ya que están en una posición favorable para asumir responsabilidades significativas y contribuir al éxito del Capítulo. Aquellos con buena concordancia deberían continuar desarrollando su experiencia, mientras que los aspirantes con  baja concordancia deberían recibir orientación para mejorar su perfil profesional y acumular más  experiencia relevante. Estas acciones asegurarán que el proceso de selección se base en una evaluación completa y precisa de las capacidades de cada candidato, fortaleciendo la gestión y el  impacto del Capítulo.",
        styles['CenturyGothic']
    ))

    elements.append(Spacer(1, 0.2 * inch))

    # Mensaje de agradecimiento
    elements.append(Paragraph(
        f"Gracias, {candidate_name}, por tu interés en el cargo de {position} ¡Éxitos en tu proceso!",
        styles['CenturyGothic']
    ))

    # Construcción del PDF
    doc.build(elements, onFirstPage=on_first_page, onLaterPages=on_later_pages)

    # Read the PDF file as bytes
    with open(output_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    # Encode PDF bytes to base64 string
    pdf_base64_string = base64.b64encode(pdf_bytes).decode('utf-8')

    return pdf_base64_string, output_path # Return base64 string and report path


def analyze_and_generate_descriptive_report_with_background_api(pdf_path, position, candidate_name, advice, indicators, background_path, chapter):
    """
    Analiza un CV descriptivo y genera un reporte PDF con fondo, usando Gemini para indicadores.
    """
    # ... (código existente para extracción de texto, carga de datos, etc. - SE MANTIENE IGUAL) ...

    position_advice = advice.get(position, {}) # Cargar advice para el cargo

    # REEMPLAZAR LA LLAMADA A calculate_indicators_for_report (o calculate_all_indicators)
    # indicator_results = calculate_indicators_for_report(...) # Función anterior (keyword-based)
    indicator_results = calculate_indicators_for_report_gemini(lines, position, position_advice) # Usar función Gemini para indicadores


    # ... (resto del código de generación del reporte -  TABLAS, PÁRRAFOS, ESTILOS, ETC. - SE MANTIENE IGUAL) ...
    # ... (Asegúrate de INTEGRAR la tabla de PRESENTACIÓN basada en Gemini como en la respuesta anterior) ...

    # Evaluación de la PRESENTACIÓN usando Gemini (INTEGRAR CÓDIGO DE RESPUESTA ANTERIOR aquí si aún no lo has hecho)
    resume_text = "" # Inicializar variable para el texto de la hoja de vida para la evaluación de presentación
    text_data = extract_text_with_headers_and_details(pdf_path) # Extraer texto con encabezados y detalles
    if text_data: # Si se extrajo texto con encabezados y detalles (para descriptive version)
        resume_text = " ".join([" ".join(details) for details in text_data.values()]) # Unir todos los detalles para la evaluación de presentación
    else: # Si no se pudo extraer con encabezados y detalles (fallback - usar extracción OCR general)
        resume_text= evaluate_cv_presentation(pdf_path) # Usar texto OCR general como fallback
        if not resume_text:
            return None, "No se pudo extraer el texto de la hoja de vida para la evaluación de presentación."

    presentation_scores = evaluate_presentation_gemini(resume_text, position) # Llama a Gemini para evaluar la presentación

    if not presentation_scores: # Manejar el caso de error en la llamada a Gemini
        clarity_score = 0  # Puntajes por defecto si falla la API de Gemini
        professionalism_score = 0
        impact_score = 0
        round_overall_score = 0 # Usar round_overall_score para consistencia en la función
    else:
        clarity_score = presentation_scores.get("clarity_score", 0)
        professionalism_score = presentation_scores.get("professionalism_score", 0)
        impact_score = presentation_scores.get("impact_score", 0)
        round_overall_score = presentation_scores.get("overall_presentation_score", 0) # Usar round_overall_score para consistencia

    # Añadir resultados al reporte (TABLA DE PRESENTACIÓN ADAPTADA - COPIA EL CÓDIGO DE LA RESPUESTA ANTERIOR AQUÍ)
    elements.append(Paragraph("<b>Evaluación de la Presentación:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    presentation_table = Table(
        [
            ["Criterio", "Puntaje (Escala 1-5)"],
            ["Claridad y Concisión", f"{clarity_score:.2f}"],
            ["Profesionalismo", f"{professionalism_score:.2f}"],
            ["Impacto y Persuasión", f"{impact_score:.2f}"],
            ["Puntaje Total de Presentación", f"{round_overall_score:.2f}"]
        ],
        colWidths=[4 * inch, 2 * inch]
    )
    presentation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(presentation_table)
    elements.append(Spacer(1, 0.2 * inch))


    # Construcción del PDF (se mantiene igual)
    doc.build(elements, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    # Read the PDF file as bytes and Encode to base64 (se mantiene igual)
    with open(output_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    pdf_base64_string = base64.b64encode(pdf_bytes).decode('utf-8')
    return pdf_base64_string, output_path
```
