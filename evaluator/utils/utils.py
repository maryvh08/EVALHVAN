import os
import json
import re
import fitz
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from io import BytesIO
import pytesseract
from django.conf import settings
from spellchecker import SpellChecker
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar datos
def load_indicators():
    """Cargar indicadores desde archivo JSON"""
    filepath = os.path.join(settings.DATA_DIR, 'indicators.json')
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def load_advice():
    """Cargar consejos desde archivo JSON"""
    filepath = os.path.join(settings.DATA_DIR, 'advice.json')
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

# Preprocesamiento de imágenes
def preprocess_image(image):
    """Preprocesar imagen para OCR"""
    # Convertir la imagen a escala de grises
    image = image.convert("L")

    # Mejorar el contraste
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # Aplicar umbral para binarización
    image = ImageOps.autocontrast(image)

    return image

# Extracción de texto
def extract_text_with_ocr(pdf_path):
    """Extraer texto de un PDF usando PyMuPDF y OCR con preprocesamiento optimizado"""
    extracted_text = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            # Intentar extraer texto directamente
            page_text = page.get_text("text").strip()
            
            # Si no hay texto, usar OCR
            if not page_text:
                pix = page.get_pixmap(dpi=300)  # Aumentar DPI para mejorar OCR
                img_data = pix.tobytes(output="png")
                img = Image.open(BytesIO(img_data))
                
                # Preprocesamiento de imagen
                img = img.convert("L")  # Convertir a escala de grises
                img = img.filter(ImageFilter.MedianFilter())  # Reducir ruido
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(2)  # Aumentar contraste
                
                # Aplicar OCR
                page_text = pytesseract.image_to_string(img, config="--psm 3").strip()
            
            extracted_text.append(page_text)

    return "\n".join(extracted_text)

def extract_cleaned_lines(text):
    """Extrae y limpia líneas de texto"""
    if isinstance(text, list):
        text = "\n".join(text)

    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        # Filtrar líneas vacías y no imprimibles
        if not line or not any(char.isalnum() for char in line):
            continue

        # Remover líneas con solo números (ejemplo: números de página)
        if re.fullmatch(r"\d+", line):
            continue

        # Ignorar líneas con muy pocos caracteres (posibles errores OCR)
        if len(line) < 3:
            continue

        cleaned_lines.append(line)

    return cleaned_lines

def calculate_similarity(text1, text2):
    """Calcula similitud entre dos textos usando TF-IDF y similitud de coseno"""
    
    if not isinstance(text1, str) or not isinstance(text2, str):
        return 0  # Evitar errores si los valores son incorrectos

    def clean_text(text):
        """Limpia el texto eliminando caracteres especiales y espacios extra"""
        if not isinstance(text, str):
            return ""
        text = re.sub(r"[^\w\s]", "", text)  # Eliminar puntuación
        text = re.sub(r"\s+", " ", text).strip().lower()  # Normalizar espacios y minúsculas
        return text
    
    text1, text2 = clean_text(text1), clean_text(text2)

    if not text1 or not text2:  # Si después de limpiar los textos están vacíos
        return 0

    try:
        vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(similarity * 100, 2)
    except Exception:
        return 0

def calculate_word_repetition(lines):
    """Calcula el score de repetición de palabras en un texto"""
    repeated_words = Counter()
    for line in lines:
        words = line.split()
        repeated_words.update([word.lower() for word in words])

    total_words = sum(repeated_words.values())
    most_common_word_count = repeated_words.most_common(1)[0][1] if repeated_words else 0
    repeated_word_ratio = (most_common_word_count / total_words) if total_words > 0 else 0

    # Una menor repetición indica mayor calidad
    repetition_score = 1 - repeated_word_ratio
    return repetition_score, repeated_words

def calculate_sentence_fluency(lines):
    """Calcula la fluidez de las oraciones basada en indicadores de coherencia"""
    logical_connectors = {
        "adición": ["además", "también", "asimismo", "igualmente", "de igual manera"],
        "causa": ["porque", "ya que", "debido a", "dado que", "por motivo de"],
        "consecuencia": ["por lo tanto", "así que", "en consecuencia", "como resultado"],
        "contraste": ["sin embargo", "pero", "aunque", "no obstante", "a pesar de"],
        "condición": ["si", "en caso de", "a menos que", "siempre que"],
        "tiempo": ["mientras", "cuando", "después de", "antes de", "al mismo tiempo"],
        "funciones": ["encargado de", "responsable de", "lideré", "gestioné", "coordiné"],
        "logros": ["logré", "alcancé", "conseguí", "incrementé", "reduje", "mejoré"],
        "secuencia": ["primero", "a continuación", "luego", "después", "finalmente"],
        "énfasis": ["sobre todo", "en particular", "especialmente", "principalmente"],
    }
    
    total_lines = len(lines)
    if total_lines == 0:
        return 0  # Sin líneas, no se puede calcular fluidez

    connector_count = 0
    punctuation_errors = 0
    sentence_lengths = []

    for line in lines:
        # Verificar errores de puntuación (oraciones sin punto final)
        if not line.endswith((".", "!", "?")):
            punctuation_errors += 1

        # Almacenar la longitud de cada oración
        sentence_lengths.append(len(line.split()))

        # Contar conectores lógicos en la línea
        for connector_type, connectors in logical_connectors.items():
            for connector in connectors:
                if connector in line.lower():
                    connector_count += 1

    # Calcular métricas individuales
    avg_length = sum(sentence_lengths) / total_lines if total_lines > 0 else 0
    length_variance = sum(
        (len(line.split()) - avg_length) ** 2 for line in lines
    ) / total_lines if total_lines > 1 and avg_length > 0 else 0

    # Normalizar métricas entre 0 y 1
    punctuation_score = max(0, 1 - (punctuation_errors / total_lines)) if total_lines > 0 else 0
    connector_score = min(1, connector_count / total_lines) if total_lines > 0 else 0
    variance_penalty = max(0, 1 - length_variance / avg_length) if avg_length > 0 else 0

    # Calcular puntaje final de fluidez
    fluency_score = (punctuation_score + connector_score + variance_penalty) / 3
    return round(fluency_score, 2)
