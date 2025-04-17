import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from django.conf import settings

# Registrar las fuentes personalizadas
def register_fonts():
    font_path = os.path.join(settings.STATIC_ROOT, 'fonts')
    pdfmetrics.registerFont(TTFont('CenturyGothic', os.path.join(font_path, 'Century_Gothic.ttf')))
    pdfmetrics.registerFont(TTFont('CenturyGothicBold', os.path.join(font_path, 'Century_Gothic_Bold.ttf')))

# Funciones para dibujar la portada y el fondo
def draw_full_page_cover(canvas, portada_path, candidate_name, position, chapter):
    """Dibuja la portada con una imagen a página completa y el título"""
    # Obtener el tamaño de la página (Carta)
    page_width, page_height = letter

    # Cargar la imagen de la portada
    img = ImageReader(portada_path)
    img_width, img_height = img.getSize()

    # Ajustar la imagen proporcionalmente para que llene la página
    scale_factor = max(page_width / img_width, page_height / img_height)
    new_width = img_width * scale_factor
    new_height = img_height * scale_factor

    # Centrar la imagen en la página
    x_offset = (page_width - new_width) / 2
    y_offset = (page_height - new_height) / 2

    # Dibujar la imagen de portada en toda la página
    canvas.drawImage(portada_path, x_offset, y_offset, width=new_width, height=new_height)

    # Configurar el título del reporte en el centro
    canvas.setFont("CenturyGothicBold", 36)
    canvas.setFillColor(colors.black)

    title_text = f"REPORTE DE ANÁLISIS\n{candidate_name.upper()}\nCARGO: {position.upper()}\nCAPÍTULO: {chapter.upper()}"

    # Medir el ancho y alto del texto
    text_width = max(canvas.stringWidth(line, "CenturyGothicBold", 36) for line in title_text.split("\n"))
    text_height = 36 * len(title_text.split("\n"))

    # Centrar el texto
    text_x = (page_width - text_width) / 2
    text_y = (page_height - text_height) / 2

    # Dibujar cada línea del título centrado
    for i, line in enumerate(title_text.split("\n")):
        line_width = canvas.stringWidth(line, "CenturyGothicBold", 36)
        line_x = (page_width - line_width) / 2
        canvas.drawString(line_x, text_y - (i * 30), line)

def add_background(canvas, background_path):
    """Dibuja una imagen de fondo en cada página del PDF"""
    canvas.saveState()
    canvas.drawImage(background_path, 0, 0, width=letter[0], height=letter[1])
    canvas.restoreState()

# Funciones para generar reportes PDF

def generate_simple_format_report(analysis_results, candidate_name, position, chapter):
    """Genera un reporte PDF para el formato simplificado"""
    # Registrar fuentes personalizadas
    register_fonts()
    
    # Definir rutas de imágenes
    portada_path = os.path.join(settings.STATIC_ROOT, 'images', 'Portada_Analizador.png')
    background_path = os.path.join(settings.STATIC_ROOT, 'images', 'Fondo_Reporte.png')
    
    # Crear un archivo en memoria
    buffer = BytesIO()
    
    # Definir el documento
    report_path = os.path.join(settings.MEDIA_ROOT, 'reports', f"Reporte_Simple_{candidate_name}_{position}_{chapter}.pdf")
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=100, bottomMargin=72)
    
    # Crear estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CenturyGothic", 
        fontName="CenturyGothic", 
        fontSize=12, 
        leading=14, 
        alignment=TA_JUSTIFY
    ))
    styles.add(ParagraphStyle(
        name="CenturyGothicBold", 
        fontName="CenturyGothicBold", 
        fontSize=12, 
        leading=14, 
        alignment=TA_JUSTIFY
    ))
    styles.add(ParagraphStyle(
        name="CenteredTitle", 
        fontName="CenturyGothicBold", 
        fontSize=14, 
        leading=16, 
        alignment=TA_CENTER
    ))
    
    # Lista para los elementos del reporte
    elements = []
    
    # Definir funciones para las primeras y siguientes páginas
    def on_first_page(canvas, doc):
        draw_full_page_cover(canvas, portada_path, candidate_name, position, chapter)
    
    def on_later_pages(canvas, doc):
        add_background(canvas, background_path)
    
    # Añadir primera página en blanco (la portada se dibujará en on_first_page)
    elements.append(PageBreak())
    
    # Título del reporte
    elements.append(Paragraph(
        f"REPORTE DE ANÁLISIS {candidate_name.upper()} CARGO {position.upper()} {chapter.upper()}", 
        styles["CenteredTitle"]
    ))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Sección de Análisis de Perfil
    elements.append(Paragraph("<b>Análisis de perfil de aspirante:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de perfil
    profile_data = [
        ["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"],
        [
            Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']),
            f"{analysis_results['profile']['func_match']:.2f}%", 
            f"{analysis_results['profile']['profile_match']:.2f}%"
        ],
        [
            Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']),
            f"{analysis_results['scores']['partial']['profile']['func_score']:.2f}", 
            f"{analysis_results['scores']['partial']['profile']['profile_score']:.2f}"
        ]
    ]
    
    profile_table = Table(profile_data, colWidths=[3 * inch, 2 * inch, 2 * inch])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1)),
    ]))
    elements.append(profile_table)
    elements.append(Spacer(1, 0.2 * inch))
    
    # Asistencia a eventos
    elements.append(Paragraph("<b>Análisis de ítems de asistencia a eventos:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de asistencia a eventos
    att_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]
    
    for item in analysis_results['attendance']:
        att_data.append([
            Paragraph(item['line'], styles['CenturyGothic']),
            f"{item['func_match']:.2f}%",
            f"{item['profile_match']:.2f}%"
        ])
    
    att_data.append([
        Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']),
        f"{analysis_results['scores']['partial']['attendance']['func_match']:.2f}%",
        f"{analysis_results['scores']['partial']['attendance']['profile_match']:.2f}%"
    ])
    
    att_data.append([
        Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']),
        f"{analysis_results['scores']['partial']['attendance']['func_score']:.2f}",
        f"{analysis_results['scores']['partial']['attendance']['profile_score']:.2f}"
    ])
    
    att_table = Table(att_data, colWidths=[3 * inch, 2 * inch, 2 * inch])
    att_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1)),
    ]))
    
    elements.append(att_table)
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph(f"• Total de asistencias a eventos analizadas: {len(analysis_results['attendance'])}", styles['CenturyGothicBold']))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    # Eventos organizados
    elements.append(Paragraph("<b>Análisis de ítems de eventos organizados:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de eventos organizados
    org_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]
    
    for item in analysis_results['events']:
        org_data.append([
            Paragraph(item['line'], styles['CenturyGothic']),
            f"{item['func_match']:.2f}%",
            f"{item['profile_match']:.2f}%"
        ])
    
    org_data.append([
        Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']),
        f"{analysis_results['scores']['partial']['events']['func_match']:.2f}%",
        f"{analysis_results['scores']['partial']['events']['profile_match']:.2f}%"
    ])
    
    org_data.append([
        Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']),
        f"{analysis_results['scores']['partial']['events']['func_score']:.2f}",
        f"{analysis_results['scores']['partial']['events']['profile_score']:.2f}"
    ])
    
    org_table = Table(org_data, colWidths=[3 * inch, 2 * inch, 2 * inch])
    org_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1)),
    ]))
    
    elements.append(org_table)
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph(f"• Total de eventos analizados: {len(analysis_results['events'])}", styles['CenturyGothicBold']))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    # Experiencia en ANEIAP
    elements.append(Paragraph("<b>Análisis de ítems de experiencia en ANEIAP:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de experiencia
    exp_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]
    
    for item in analysis_results['experience']:
        exp_data.append([
            Paragraph(item['line'], styles['CenturyGothic']),
            f"{item['func_match']:.2f}%",
            f"{item['profile_match']:.2f}%"
        ])
    
    exp_data.append([
        Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']),
        f"{analysis_results['scores']['partial']['experience']['func_match']:.2f}%",
        f"{analysis_results['scores']['partial']['experience']['profile_match']:.2f}%"
    ])
    
    exp_data.append([
        Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']),
        f"{analysis_results['scores']['partial']['experience']['func_score']:.2f}",
        f"{analysis_results['scores']['partial']['experience']['profile_score']:.2f}"
    ])
    
    exp_table = Table(exp_data, colWidths=[3 * inch, 2 * inch, 2 * inch])
    exp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1)),
    ]))
    
    elements.append(exp_table)
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"• Total de experiencias analizadas: {len(analysis_results['experience'])}", styles['CenturyGothicBold']))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    # Presentación
    elements.append(Paragraph("<b>Evaluación de la Presentación:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de presentación
    pres_data = [
        ["Criterio", "Puntaje"],
        ["Coherencia", f"{analysis_results['presentation']['coherence_score']:.2f}"],
        ["Ortografía", f"{analysis_results['presentation']['spelling_score']:.2f}"],
        ["Gramática", f"{analysis_results['presentation']['grammar_score']:.2f}"],
        ["Puntaje Total", f"{analysis_results['presentation']['overall_score']:.2f}"]
    ]
    
    pres_table = Table(pres_data, colWidths=[3 * inch, 2 * inch])
    pres_table.setStyle(TableStyle([
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
    
    elements.append(pres_table)
    elements.append(Spacer(1, 0.2 * inch))
# Consejos para mejorar la presentación
    elements.append(Paragraph("<b>Consejos para mejorar la presentación de la hoja de vida:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Consejos para coherencia
    coherence_score = analysis_results['presentation']['coherence_score']
    if coherence_score < 3:
        elements.append(Paragraph(
            "• Mejora la redacción de las frases en tu hoja de vida. Asegúrate de que sean completas, coherentes y claras.",
            styles['CenturyGothic']
        ))
    elif 3 <= coherence_score <= 4:
        elements.append(Paragraph(
            "• La redacción de tus frases es adecuada, pero revisa la fluidez entre oraciones para mejorar la coherencia general.",
            styles['CenturyGothic']
        ))
    else:
        elements.append(Paragraph(
            "• La redacción de las frases en tu hoja de vida es clara y coherente. Excelente trabajo.",
            styles['CenturyGothic']
        ))
    elements.append(Spacer(1, 0.1 * inch))
    
    # Consejos para ortografía
    spelling_score = analysis_results['presentation']['spelling_score']
    if spelling_score < 3:
        elements.append(Paragraph(
            "• Revisa cuidadosamente la ortografía de tu hoja de vida. Considera utilizar herramientas automáticas para detectar errores de escritura.",
            styles['CenturyGothic']
        ))
    elif 3 <= spelling_score <= 4:
        elements.append(Paragraph(
            "• Tu ortografía es buena, pero aún puede mejorar. Lee tu hoja de vida en voz alta para identificar errores menores.",
            styles['CenturyGothic']
        ))
    else:
        elements.append(Paragraph(
            "• Tu ortografía es excelente. Continúa manteniendo este nivel de detalle en tus documentos.",
            styles['CenturyGothic']
        ))
    elements.append(Spacer(1, 0.1 * inch))
    
    # Consejos para gramática
    grammar_score = analysis_results['presentation']['grammar_score']
    if grammar_score < 3:
        elements.append(Paragraph(
            "• Corrige el uso de mayúsculas. Asegúrate de que nombres propios, títulos y principios de frases estén correctamente capitalizados.",
            styles['CenturyGothic']
        ))
    elif 3 <= grammar_score <= 4:
        elements.append(Paragraph(
            "• Tu uso de mayúsculas es aceptable, pero puede perfeccionarse. Revisa los encabezados y títulos para asegurarte de que estén bien escritos.",
            styles['CenturyGothic']
        ))
    else:
        elements.append(Paragraph(
            "• El uso de mayúsculas en tu hoja de vida es excelente. Continúa aplicando este estándar.",
            styles['CenturyGothic']
        ))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    # Resultados de indicadores
    elements.append(Paragraph("<b>Resultados de indicadores:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de indicadores
    ind_data = [["Indicador", "Concordancia (%)"]]
    
    for indicator, data in analysis_results['indicators'].items():
        if isinstance(data, dict) and 'percentage' in data:
            percentage = data['percentage']
        else:
            percentage = data
        
        ind_data.append([
            Paragraph(indicator, styles['CenturyGothic']),
            f"{percentage:.2f}%"
        ])
    
    ind_table = Table(ind_data, colWidths=[4 * inch, 2 * inch])
    ind_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1)),
    ]))
    
    elements.append(ind_table)
    elements.append(Spacer(1, 0.2 * inch))
    
    # Resultados globales
    elements.append(Paragraph("<b>Resultados globales:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de resultados globales
    global_data = [["Criterio", "Funciones del Cargo", "Perfil del Cargo"]]
    
    global_data.append([
        Paragraph("<b>Concordancia Global</b>", styles['CenturyGothicBold']),
        f"{analysis_results['scores']['global']['func_match']:.2f}%",
        f"{analysis_results['scores']['global']['profile_match']:.2f}%"
    ])
    
    global_data.append([
        Paragraph("<b>Puntaje Global</b>", styles['CenturyGothicBold']),
        f"{analysis_results['scores']['global']['func_score']:.2f}",
        f"{analysis_results['scores']['global']['profile_score']:.2f}"
    ])
    
    global_table = Table(global_data, colWidths=[3 * inch, 2 * inch, 2 * inch])
    global_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1)),
    ]))
    
    elements.append(global_table)
    elements.append(Spacer(1, 0.2 * inch))
    
    # Interpretación de resultados
    elements.append(Paragraph("<b>Interpretación de resultados globales:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.1 * inch))
    
    func_match = analysis_results['scores']['global']['func_match']
    profile_match = analysis_results['scores']['global']['profile_match']
    
    if func_match > 75 and profile_match > 75:
        elements.append(Paragraph(
            f" Alta Concordancia (> 75%): El análisis revela que {candidate_name} tiene una excelente adecuación con las funciones del cargo de {position} y el perfil buscado. La experiencia detallada en su hoja de vida está estrechamente alineada con las responsabilidades y competencias requeridas para este rol crucial en la prevalencia del Capítulo. La alta concordancia indica que {candidate_name} está bien preparado para asumir este cargo y contribuir significativamente al éxito y la misión del Capítulo. Se recomienda proceder con el proceso de selección y considerar a {candidate_name} como una opción sólida para el cargo.",
            styles['CenturyGothic']
        ))
    elif func_match > 60 or profile_match > 60:
        elements.append(Paragraph(
            f" Buena Concordancia (> 60%): El análisis muestra que {candidate_name} tiene una buena correspondencia con las funciones del cargo de {position} y el perfil deseado. Aunque su experiencia en la asociación es relevante, existe margen para mejorar. {candidate_name} muestra potencial para cumplir con el rol crucial en la prevalencia del Capítulo, pero se recomienda que continúe desarrollando sus habilidades y acumulando más experiencia relacionada con el cargo objetivo. Su candidatura debe ser considerada con la recomendación de enriquecimiento adicional.",
            styles['CenturyGothic']
        ))
    else:
        elements.append(Paragraph(
            f" Baja Concordancia (< 60%): El análisis indica que {candidate_name} tiene una baja concordancia con los requisitos del cargo de {position} y el perfil buscado. Esto sugiere que aunque el aspirante posee algunas experiencias relevantes, su historial actual no cubre adecuadamente las competencias y responsabilidades necesarias para este rol crucial en la prevalencia del Capítulo. Se aconseja a {candidate_name} enfocarse en mejorar su perfil profesional y desarrollar las habilidades necesarias para el cargo. Este enfoque permitirá a {candidate_name} alinear mejor su perfil con los requisitos del puesto en futuras oportunidades.",
            styles['CenturyGothic']
        ))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    # Puntajes totales
    elements.append(Paragraph("<b>Puntajes totales:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de puntajes totales
    scores = analysis_results['scores']
    total_data = [
        ["Criterio", "Puntaje"],
        ["Experiencia en ANEIAP", f"{scores['partial']['experience']['score']:.2f}"],
        ["Asistencia a eventos", f"{scores['partial']['attendance']['score']:.2f}"],
        ["Eventos organizados", f"{scores['partial']['events']['score']:.2f}"],
        ["Perfil", f"{scores['partial']['profile']['score']:.2f}"],
        ["Presentación", f"{analysis_results['presentation']['overall_score']:.2f}"],
        ["Puntaje Total", f"{scores['total']:.2f}"]
    ]
    
    total_table = Table(total_data, colWidths=[3 * inch, 2 * inch])
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
    
    # Comentarios sobre los resultados
    elements.append(Paragraph("<b>Comentarios sobre los Resultados:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Generar comentarios
    comments = []
    exp_score = scores['partial']['experience']['score']
    att_score = scores['partial']['attendance']['score']
    org_score = scores['partial']['events']['score']
    prof_score = scores['partial']['profile']['score']
    overall_score = analysis_results['presentation']['overall_score']
    total_score = scores['total']
    
    # Experiencia en ANEIAP
    if exp_score >= 4:
        comments.append("Tu experiencia en ANEIAP refleja un nivel destacado, lo que demuestra un conocimiento sólido de la organización y tus contribuciones en actividades clave. Continúa fortaleciendo tu participación para mantener este nivel y destacar aún más.")
    elif exp_score >= 3:
        comments.append("Tu experiencia en ANEIAP es buena, pero podrías enfocarte en profundizar tus contribuciones y participación en actividades clave.")
    else:
        comments.append("Es importante fortalecer tu experiencia en ANEIAP. Considera involucrarte en más actividades y proyectos para adquirir una mayor comprensión y relevancia.")
    
    # Asistencia a eventos
    if att_score >= 4:
        comments.append("Tu puntuación en asistencia a eventos es excelente. Esto muestra tu compromiso con el aprendizaje y el desarrollo profesional. Mantén esta consistencia participando en eventos relevantes que sigan ampliando tu red de contactos y conocimientos.")
    elif att_score >= 3:
        comments.append("Tu asistencia a eventos es adecuada, pero hay margen para participar más en actividades que refuercen tu aprendizaje y crecimiento profesional.")
    else:
        comments.append("Debes trabajar en tu participación en eventos. La asistencia regular a actividades puede ayudarte a desarrollar habilidades clave y expandir tu red de contactos.")
    
    # Eventos organizados
    if org_score >= 4:
        comments.append("¡Perfecto! Tu desempeño en la organización de eventos es ejemplar. Esto indica habilidades destacadas de planificación, liderazgo y ejecución. Considera compartir tus experiencias con otros miembros para fortalecer el impacto organizacional.")
    elif org_score >= 3:
        comments.append("Tu desempeño en la organización de eventos es bueno, pero podrías centrarte en mejorar la planificación y la ejecución para alcanzar un nivel más destacado.")
    else:
        comments.append("Es importante trabajar en tus habilidades de organización de eventos. Considera involucrarte en proyectos donde puedas asumir un rol de liderazgo y planificación.")
    
    # Perfil
    if prof_score >= 4:
        comments.append("Tu perfil presenta una buena alineación con las expectativas del cargo, destacando competencias clave. Mantén este nivel y continúa fortaleciendo áreas relevantes.")
    elif prof_score >= 3:
        comments.append("El perfil presenta una buena alineación con las expectativas del cargo, aunque hay margen de mejora. Podrías enfocar tus esfuerzos en reforzar áreas específicas relacionadas con las competencias clave del puesto.")
    else:
        comments.append("Tu perfil necesita mejoras para alinearse mejor con las expectativas del cargo. Trabaja en desarrollar habilidades y competencias clave.")
    
    # Presentación
    if overall_score >= 4:
        comments.append("La presentación de tu hoja de vida es excelente. Refleja profesionalismo y claridad. Continúa aplicando este enfoque para mantener un alto estándar.")
    elif overall_score >= 3:
        comments.append("La presentación de tu hoja de vida es buena, pero puede mejorar en aspectos como coherencia, ortografía o formato general. Dedica tiempo a revisar estos detalles.")
    else:
        comments.append("La presentación de tu hoja de vida necesita mejoras significativas. Asegúrate de revisar la ortografía, la gramática y la coherencia para proyectar una imagen más profesional.")
    
    # Puntaje total
    if total_score >= 4:
        comments.append("Tu puntaje total indica un desempeño destacado en la mayoría de las áreas. Estás bien posicionado para asumir el rol. Mantén este nivel y busca perfeccionar tus fortalezas.")
    elif total_score >= 3:
        comments.append("Tu puntaje total es sólido, pero hay aspectos que podrían mejorarse. Enfócate en perfeccionar la presentación y el perfil para complementar tus fortalezas en experiencia, eventos y asistencia.")
    else:
        comments.append("El puntaje total muestra áreas importantes por mejorar. Trabaja en fortalecer cada criterio para presentar un perfil más competitivo y completo.")
    
    # Agregar comentarios al reporte
    for comment in comments:
        elements.append(Paragraph(comment, styles['CenturyGothic']))
        elements.append(Spacer(1, 0.1 * inch))
    
    elements.append(Spacer(1, 0.1 * inch))
    
    # Conclusión
    elements.append(Paragraph(
        f"Este análisis es generado debido a que es crucial tomar medidas estratégicas para garantizar que los candidatos estén bien preparados para el rol de {position}. Los aspirantes con alta concordancia deben ser considerados seriamente para el cargo, ya que están en una posición favorable para asumir responsabilidades significativas y contribuir al éxito del Capítulo. Aquellos con buena concordancia deberían continuar desarrollando su experiencia, mientras que los aspirantes con baja concordancia deberían recibir orientación para mejorar su perfil profesional y acumular más experiencia relevante. Estas acciones asegurarán que el proceso de selección se base en una evaluación completa y precisa de las capacidades de cada candidato, fortaleciendo la gestión y el impacto del Capítulo.",
        styles['CenturyGothic']
    ))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    # Mensaje de agradecimiento
    elements.append(Paragraph(
        f"Gracias, {candidate_name}, por tu interés en el cargo de {position} ¡Éxitos en tu proceso!",
        styles['CenturyGothic']
    ))
    
    # Construir el PDF
    doc.build(elements, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    
    # Obtener el contenido del buffer
    pdf_content = buffer.getvalue()
    buffer.close()
    
    # Guardar el PDF y devolver el contenido
    with open(report_path, 'wb') as f:
        f.write(pdf_content)
    
    return pdf_content, report_path

def generate_descriptive_format_report(analysis_results, candidate_name, position, chapter):
    """Genera un reporte PDF para el formato descriptivo"""
    # Registrar fuentes personalizadas
    register_fonts()
    
    # Definir rutas de imágenes
    portada_path = os.path.join(settings.STATIC_ROOT, 'images', 'Portada_Analizador.png')
    background_path = os.path.join(settings.STATIC_ROOT, 'images', 'Fondo_Reporte.png')
    
    # Crear un archivo en memoria
    buffer = BytesIO()
    
    # Definir el documento
    report_path = os.path.join(settings.MEDIA_ROOT, 'reports', f"Reporte_Descriptivo_{candidate_name}_{position}_{chapter}.pdf")
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=100, bottomMargin=72)
    
    # Crear estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CenturyGothic", 
        fontName="CenturyGothic", 
        fontSize=12, 
        leading=14, 
        alignment=TA_JUSTIFY
    ))
    styles.add(ParagraphStyle(
        name="CenturyGothicBold", 
        fontName="CenturyGothicBold", 
        fontSize=12, 
        leading=14, 
        alignment=TA_JUSTIFY
    ))
    styles.add(ParagraphStyle(
        name="CenteredTitle", 
        fontName="CenturyGothicBold", 
        fontSize=14, 
        leading=16, 
        alignment=TA_CENTER
    ))
    
    # Lista para los elementos del reporte
    elements = []
    
    # Definir funciones para las primeras y siguientes páginas
    def on_first_page(canvas, doc):
        draw_full_page_cover(canvas, portada_path, candidate_name, position, chapter)
    
    def on_later_pages(canvas, doc):
        add_background(canvas, background_path)
    
    # Añadir primera página en blanco (la portada se dibujará en on_first_page)
    elements.append(PageBreak())
    
    # Título del reporte
    elements.append(Paragraph(
        f"REPORTE DE ANÁLISIS DESCRIPTIVO {candidate_name.upper()} CARGO {position.upper()} {chapter.upper()}", 
        styles["CenteredTitle"]
    ))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Sección de Análisis de Perfil
    elements.append(Paragraph("<b>Análisis de perfil de aspirante:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de perfil
    profile_data = [
        ["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"],
        [
            Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']),
            f"{analysis_results['profile']['func_match']:.2f}%", 
            f"{analysis_results['profile']['profile_match']:.2f}%"
        ],
        [
            Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']),
            f"{analysis_results['scores']['partial']['profile']['func_score']:.2f}", 
            f"{analysis_results['scores']['partial']['profile']['profile_score']:.2f}"
        ]
    ]
    
    profile_table = Table(profile_data, colWidths=[3 * inch, 2 * inch, 2 * inch])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1)),
    ]))
    elements.append(profile_table)
    elements.append(Spacer(1, 0.2 * inch))
    
    # Eventos organizados
    elements.append(Paragraph("<b>Análisis de eventos organizados:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de eventos organizados
    org_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]
    
    for item in analysis_results['events']:
        header = item.get('header', '')
        org_data.append([
            Paragraph(header, styles['CenturyGothic']),
            f"{item['func_match']:.2f}%",
            f"{item['profile_match']:.2f}%"
        ])
    
    org_data.append([
        Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']),
        f"{analysis_results['scores']['partial']['events']['func_match']:.2f}%",
        f"{analysis_results['scores']['partial']['events']['profile_match']:.2f}%"
    ])
    
    org_data.append([
        Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']),
        f"{analysis_results['scores']['partial']['events']['func_score']:.2f}",
        f"{analysis_results['scores']['partial']['events']['profile_score']:.2f}"
    ])
    
    org_table = Table(org_data, colWidths=[3 * inch, 2 * inch, 2 * inch])
    org_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1)),
    ]))
    
    elements.append(org_table)
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"• Total de eventos analizados: {len(analysis_results['events'])}", styles['CenturyGothicBold']))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    # Asistencia a eventos
    elements.append(Paragraph("<b>Análisis de eventos asistidos:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de asistencia a eventos
    att_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]
    
    for item in analysis_results['attendance']:
        header = item.get('header', '')
        att_data.append([
            Paragraph(header, styles['CenturyGothic']),
            f"{item['func_match']:.2f}%",
            f"{item['profile_match']:.2f}%"
        ])
    
    att_data.append([
        Paragraph("<b>Concordancia Parcial</b>", styles['CenturyGothicBold']),
        f"{analysis_results['scores']['partial']['attendance']['func_match']:.2f}%",
        f"{analysis_results['scores']['partial']['attendance']['profile_match']:.2f}%"
    ])
    
    att_data.append([
        Paragraph("<b>Puntaje Parcial</b>", styles['CenturyGothicBold']),
        f"{analysis_results['scores']['partial']['attendance']['func_score']:.2f}",
        f"{analysis_results['scores']['partial']['attendance']['profile_score']:.2f}"
    ])
    
    att_table = Table(att_data, colWidths=[3 * inch, 2 * inch, 2 * inch])
    att_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CenturyGothicBold'),
        ('FONTNAME', (0, 1), (-1, -1), 'CenturyGothic'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1)),
    ]))
    
    elements.append(att_table)
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"• Total de asistencias analizadas: {len(analysis_results['attendance'])}", styles['CenturyGothicBold']))
    
    elements.append(Spacer(1, 0.2 * inch))
    
    # Experiencia en ANEIAP
    elements.append(Paragraph("<b>Análisis de Experiencia en ANEIAP:</b>", styles['CenturyGothicBold']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Tabla de experiencia
    exp_data = [["Ítem", "Funciones del Cargo (%)", "Perfil del Cargo (%)"]]
    
    for item in analysis_results['experience']:
        header = item.get('header', '')
        exp_data.append([
            Paragraph(header, styles['CenturyGothic']),
            f"{item['func_match']:.
