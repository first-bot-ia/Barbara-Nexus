"""
📄 PDF Generator Service - Generación de cotizaciones en PDF
===========================================================
Genera PDFs profesionales de las cotizaciones SOAT para:
- Envío por email como adjunto
- Envío por WhatsApp
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PDFGeneratorService:
    """
    Servicio para generar PDFs profesionales de cotizaciones SOAT
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Configura estilos personalizados para el PDF"""
        
        # Estilo para el título principal
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1e3a8a')
        )
        
        # Estilo para subtítulos
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#3b82f6')
        )
        
        # Estilo para texto normal
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_LEFT
        )
        
        # Estilo para precios destacados
        self.price_style = ParagraphStyle(
            'CustomPrice',
            parent=self.styles['Normal'],
            fontSize=18,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#059669'),
            fontName='Helvetica-Bold'
        )
    
    def generate_quotation_pdf(self, 
                             client_name: str,
                             cotizacion: Dict[str, Any],
                             output_path: Optional[str] = None) -> str:
        """
        Genera PDF de cotización SOAT
        
        Args:
            client_name: Nombre del cliente
            cotizacion: Datos de la cotización (DEBE tener todos los valores requeridos)
            output_path: Ruta donde guardar el PDF (opcional)
            
        Returns:
            str: Ruta del archivo PDF generado
        """
        
        try:
            # Validar datos de entrada
            if not self._validate_cotizacion_data(cotizacion):
                raise ValueError("Cotización inválida - faltan datos requeridos")
            
            # Definir ruta de salida usando datos reales
            if not output_path:
                filename = f"cotizacion_{cotizacion['numero_cotizacion']}.pdf"
                output_path = os.path.join("assets", filename)
            
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Crear documento PDF
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Crear contenido
            story = []
            
            # Header con logo y título
            self._add_header(story, cotizacion)
            
            # Información del cliente
            self._add_client_info(story, client_name, cotizacion)
            
            # Detalles de la cotización
            self._add_quotation_details(story, cotizacion)
            
            # Precio destacado
            self._add_price_section(story, cotizacion)
            
            # Cobertura y beneficios
            self._add_coverage_section(story)
            
            # Información de contacto
            self._add_contact_info(story)
            
            # Footer
            self._add_footer(story)
            
            # Generar PDF
            doc.build(story)
            
            logger.info(f"📄 PDF generado exitosamente: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Error generando PDF: {e}")
            raise
    
    def _add_header(self, story, cotizacion):
        """Añade header con logo y título"""
        
        # Título principal
        title = Paragraph("🛡️ COTIZACIÓN SOAT 2024", self.title_style)
        story.append(title)
        
        subtitle = Paragraph("Autofondo Alese - Tu protección vehicular", self.normal_style)
        story.append(subtitle)
        story.append(Spacer(1, 20))
    
    def _add_client_info(self, story, client_name, cotizacion):
        """Añade información del cliente con datos reales"""
        
        story.append(Paragraph("INFORMACIÓN DEL CLIENTE", self.subtitle_style))
        
        client_data = [
            ['Cliente:', client_name],
            ['Fecha:', datetime.now().strftime('%d/%m/%Y')],
            ['Cotización N°:', cotizacion['numero_cotizacion']],
            ['Validez:', '15 días']
        ]
        
        client_table = Table(client_data, colWidths=[2*inch, 3*inch])
        client_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 11),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 1, colors.lightgrey)
        ]))
        
        story.append(client_table)
        story.append(Spacer(1, 20))
    
    def _add_quotation_details(self, story, cotizacion):
        """Añade detalles de la cotización con datos reales"""
        
        story.append(Paragraph("DETALLES DEL VEHÍCULO", self.subtitle_style))
        
        vehicle_data = [
            ['Tipo de vehículo:', cotizacion['tipo_vehiculo']],
            ['Vigencia:', '1 año'],
            ['Cobertura:', 'Completa contra terceros'],
            ['Modalidad:', 'SOAT Obligatorio']
        ]
        
        vehicle_table = Table(vehicle_data, colWidths=[2*inch, 3*inch])
        vehicle_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 11),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 1, colors.lightgrey)
        ]))
        
        story.append(vehicle_table)
        story.append(Spacer(1, 20))
    
    def _add_price_section(self, story, cotizacion):
        """Añade sección de precio con datos reales"""
        
        story.append(Paragraph("PRECIO FINAL", self.subtitle_style))
        
        price_text = f"💰 {cotizacion['precio_final']}"
        price_para = Paragraph(price_text, self.price_style)
        story.append(price_para)
        
        included_text = "Incluye IGV y todos los beneficios"
        included_para = Paragraph(included_text, self.normal_style)
        story.append(included_para)
        story.append(Spacer(1, 20))
    
    def _add_coverage_section(self, story):
        """Añade sección de cobertura y beneficios"""
        
        story.append(Paragraph("TU SOAT INCLUYE", self.subtitle_style))
        
        benefits_data = [
            ['Beneficio', 'Cobertura'],
            ['Gastos médicos', 'Hasta 5 UIT (S/ 25,500)'],
            ['Muerte por accidente', 'Hasta 4 UIT (S/ 20,400)'],
            ['Invalidez permanente', 'Hasta 4 UIT (S/ 20,400)'],
            ['Gastos de sepelio', 'Hasta 1 UIT (S/ 5,100)'],
            ['Atención médica', '24/7 todos los días'],
            ['Cobertura geográfica', 'Todo el territorio peruano']
        ]
        
        benefits_table = Table(benefits_data, colWidths=[2.5*inch, 2.5*inch])
        benefits_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        
        story.append(benefits_table)
        story.append(Spacer(1, 20))
    
    def _add_contact_info(self, story):
        """Añade información de contacto"""
        
        story.append(Paragraph("INFORMACIÓN DE CONTACTO", self.subtitle_style))
        
        contact_text = """
        <b>Autofondo Alese</b><br/>
        📞 Teléfono: +51 999 888 777<br/>
        📧 Email: info@autofondoalese.com<br/>
        💬 WhatsApp: 999-919-133<br/>
        🌐 Tu compañía de seguros de confianza
        """
        
        contact_para = Paragraph(contact_text, self.normal_style)
        story.append(contact_para)
        story.append(Spacer(1, 20))
    
    def _add_footer(self, story):
        """Añade footer con términos y condiciones"""
        
        footer_text = """
        <b>Términos y Condiciones:</b><br/>
        • Esta cotización es válida por 15 días calendarios<br/>
        • Precios incluyen IGV y están sujetos a cambios sin previo aviso<br/>
        • Para finalizar la compra, contacta a nuestros asesores<br/>
        • SOAT generado automáticamente por Barbara, tu asesora digital<br/>
        """
        
        footer_para = Paragraph(footer_text, ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_LEFT,
            textColor=colors.grey
        ))
        
        story.append(Spacer(1, 30))
        story.append(footer_para)
    
    def get_service_status(self) -> Dict[str, Any]:
        """Obtiene estado del servicio PDF"""
        return {
            'service': 'PDF Generator Service',
            'status': 'active',
            'library': 'ReportLab',
            'formats': ['PDF'],
            'features': [
                'Cotizaciones profesionales',
                'Diseño corporativo',
                'Tablas estructuradas',
                'Listo para adjuntar'
            ]
        }
    
    def _validate_cotizacion_data(self, cotizacion: Dict[str, Any]) -> bool:
        """
        Valida que la cotización tenga todos los datos necesarios
        NO PERMITE valores None o vacíos
        """
        required_fields = ['numero_cotizacion', 'tipo_vehiculo', 'precio_final']
        
        for field in required_fields:
            if field not in cotizacion or not cotizacion[field]:
                logger.error(f"❌ Campo requerido faltante o vacío en PDF: {field}")
                return False
        
        return True 