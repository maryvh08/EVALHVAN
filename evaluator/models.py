from django.db import models
import os
import uuid

def get_report_path(instance, filename):
    # Generar una ruta única para el reporte
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('reports', filename)

def get_temp_path(instance, filename):
    # Generar una ruta única para archivos temporales
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('temp', filename)

class Evaluation(models.Model):
    """Modelo para almacenar información de las evaluaciones"""
    POSITION_CHOICES = [
        ('DCA', 'Director Capitular Académico'),
        ('DCC', 'Director Capitular de Comunicaciones'),
        ('DCD', 'Director Capitular de Desarrollo'),
        ('DCF', 'Director Capitular de Finanzas'),
        ('DCM', 'Director Capitular de Mercadeo'),
        ('CCP', 'Coordinador Capitular de Proyectos'),
        ('IC', 'Interventor Capitular'),
        ('PC', 'Presidente Capitular'),
    ]
    
    CHAPTER_CHOICES = [
        ('UNIGUAJIRA', 'Universidad de La Guajira'),
        ('UNIMAGDALENA', 'Universidad del Magdalena'),
        ('UNINORTE', 'Universidad del Norte'),
        ('UNIATLÁNTICO', 'Universidad del Atlántico'),
        ('CUC', 'Corporación Universidad de la Costa'),
        ('UNISIMÓN', 'Universidad Simón Bolívar'),
        ('LIBREQUILLA', 'Universidad Libre Barranquilla'),
        ('UTB', 'Universidad Tecnológica de Bolívar'),
        ('UFPS', 'Universidad Francisco de Paula Santander'),
        ('UNALMED', 'Universidad Nacional Sede Medellín'),
        ('UPBMED', 'Universidad Pontificia Bolivariana'),
        ('UDEA', 'Universidad de Antioquia'),
        ('UTP', 'Universidad Tecnológica de Pereira'),
        ('UNALMA', 'Universidad Nacional Sede Manizales'),
        ('LIBRECALI', 'Universidad Libre Cali'),
        ('UNIVALLE', 'Universidad del Valle'),
        ('ICESI', 'Universidad ICESI'),
        ('USC', 'Universidad Santiago de Cali'),
        ('UDISTRITAL', 'Universidad Distrital Francisco José de Caldas'),
        ('UNALBOG', 'Universidad Nacional Sede Bogotá'),
        ('UPBMONTERÍA', 'Universidad Pontificia Bolivariana Sede Montería'),
        ('AREANDINA', 'Fundación Universitaria del Área Andina'),
        ('UNICÓDOBA', 'Universidad de Córdoba'),
    ]

    candidate_name = models.CharField(max_length=255, verbose_name="Nombre del candidato")
    position = models.CharField(max_length=3, choices=POSITION_CHOICES, verbose_name="Cargo al que aspira")
    chapter = models.CharField(max_length=20, choices=CHAPTER_CHOICES, verbose_name="Capítulo")
    resume_file = models.FileField(upload_to=get_temp_path, verbose_name="Hoja de vida")
    format_type = models.CharField(max_length=20, choices=[
        ('simple', 'Formato Simplificado'), 
        ('descriptive', 'Formato Descriptivo')
    ], verbose_name="Tipo de formato")
    report_file = models.FileField(upload_to=get_report_path, null=True, blank=True, verbose_name="Reporte generado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    score = models.FloatField(null=True, blank=True, verbose_name="Puntaje total")
    
    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.candidate_name} - {self.get_position_display()} - {self.get_chapter_display()}"
    
    def delete(self, *args, **kwargs):
        # Eliminar archivos al eliminar el registro
        if self.resume_file:
            if os.path.isfile(self.resume_file.path):
                os.remove(self.resume_file.path)
        if self.report_file:
            if os.path.isfile(self.report_file.path):
                os.remove(self.report_file.path)
        super().delete(*args, **kwargs)
