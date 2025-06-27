"""
📧 Mailtrap Service - Servicio de envío GRATUITO para Python
1,000 emails/mes gratis - Perfecto para Barbara
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class MailtrapService:
    """
    Servicio de envío usando Mailtrap (1,000 emails/mes GRATIS)
    Perfecto para aplicaciones Python como Barbara
    """
    
    def __init__(self):
        # Configuración Mailtrap GRATUITA
        self.smtp_server = "sandbox.smtp.mailtrap.io"
        self.smtp_port = 2525
        
        # Credenciales Mailtrap (configúralas en .env)
        self.username = os.getenv("MAILTRAP_USERNAME", "tu_mailtrap_username")
        self.password = os.getenv("MAILTRAP_PASSWORD", "tu_mailtrap_password")
        
        self.sender_name = "Barbara - Autofondo Alese"
        self.sender_email = "barbara@autofondoalese.com"
        
    def send_quotation_email(self, 
                           recipient_email: str,
                           client_name: str,
                           cotizacion: Dict[str, Any]) -> bool:
        """
        Envía cotización por correo usando Mailtrap
        
        Args:
            recipient_email: Email del destinatario
            client_name: Nombre del cliente
            cotizacion: Datos de la cotización (DEBE tener todos los valores requeridos)
            
        Returns:
            bool: True si se envió exitosamente
        """
        
        try:
            # Validar datos de entrada
            if not self._validate_cotizacion_data(cotizacion):
                logger.error("❌ Cotización inválida - faltan datos requeridos")
                return False
            
            # Crear mensaje
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Tu Cotización SOAT - {cotizacion['numero_cotizacion']}"
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = recipient_email
            
            # Generar contenido
            text_content = self._generate_text_content(client_name, cotizacion)
            html_content = self._generate_html_content(client_name, cotizacion)
            
            # Crear partes del mensaje
            text_part = MIMEText(text_content, "plain", "utf-8")
            html_part = MIMEText(html_content, "html", "utf-8")
            
            # Adjuntar partes
            message.attach(text_part)
            message.attach(html_part)
            
            # Enviar email con Mailtrap
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            logger.info(f"📧 Cotización enviada por Mailtrap a {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando email con Mailtrap: {e}")
            return False
    
    def _generate_text_content(self, client_name: str, cotizacion: Dict[str, Any]) -> str:
        """Genera contenido de texto plano con datos reales"""
        
        return f"""🛡️ TU COTIZACIÓN SOAT - AUTOFONDO ALESE

¡Hola {client_name}!

Te enviamos tu cotización personalizada generada por Barbara:

📋 DETALLES DE TU COTIZACIÓN
================================
Cliente: {client_name}
Vehículo: {cotizacion['tipo_vehiculo']}
Cotización N°: {cotizacion['numero_cotizacion']}
Fecha: {datetime.now().strftime('%d/%m/%Y')}

💰 PRECIO FINAL: {cotizacion['precio_final']}

✅ TU SOAT INCLUYE:
- Gastos médicos: Hasta 5 UIT (S/ 25,500)
- Muerte: Hasta 4 UIT (S/ 20,400)  
- Invalidez permanente: Hasta 4 UIT (S/ 20,400)
- Gastos de sepelio: Hasta 1 UIT (S/ 5,100)
- Cobertura las 24 horas todos los días del año
- Atención médica inmediata en caso de accidente

⏰ OFERTA VÁLIDA POR 15 DÍAS

Para finalizar tu compra, contacta:
📞 +51 999 888 777
📧 info@autofondoalese.com

---
Barbara & Equipo Autofondo Alese
Tu compañía de seguros de confianza"""
    
    def _generate_html_content(self, client_name: str, cotizacion: Dict[str, Any]) -> str:
        """Genera contenido HTML profesional con datos reales"""
        
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tu Cotización SOAT</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #1e3a8a; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .cotizacion-box {{ background: white; padding: 25px; border-radius: 8px; margin: 20px 0; }}
        .precio {{ font-size: 24px; font-weight: bold; color: #1e3a8a; text-align: center; background: #e8f4f8; padding: 20px; border-radius: 8px; }}
        .cta {{ background: #1e3a8a; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Tu Cotización SOAT</h1>
        <p>Autofondo Alese - Protección completa</p>
    </div>
    
    <div class="content">
        <h2>¡Hola {client_name}!</h2>
        
        <p>Barbara ha preparado tu cotización personalizada:</p>
        
        <div class="cotizacion-box">
            <h3>📋 Detalles de tu Cotización</h3>
            <p><strong>Cliente:</strong> {client_name}</p>
            <p><strong>Vehículo:</strong> {cotizacion['tipo_vehiculo']}</p>
            <p><strong>Cotización N°:</strong> {cotizacion['numero_cotizacion']}</p>
            <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y')}</p>
        </div>
        
        <div class="precio">
            💰 Precio Final: {cotizacion['precio_final']}
        </div>
        
        <h3>✅ Tu SOAT Incluye:</h3>
        <ul>
            <li>Gastos médicos: Hasta 5 UIT (S/ 25,500)</li>
            <li>Muerte: Hasta 4 UIT (S/ 20,400)</li>
            <li>Invalidez permanente: Hasta 4 UIT (S/ 20,400)</li>
            <li>Gastos de sepelio: Hasta 1 UIT (S/ 5,100)</li>
        </ul>
        
        <p style="text-align: center;">
            <a href="tel:+51999888777" class="cta">📞 Finalizar Compra: +51 999 888 777</a>
        </p>
        
        <p><strong>⏰ Oferta válida por 15 días</strong></p>
    </div>
    
    <div style="text-align: center; margin-top: 20px; color: #666;">
        <p>Barbara & Equipo Autofondo Alese<br>
        📧 info@autofondoalese.com | 📞 +51 999 888 777</p>
    </div>
</body>
</html>
        """
    
    def _validate_cotizacion_data(self, cotizacion: Dict[str, Any]) -> bool:
        """
        Valida que la cotización tenga todos los datos necesarios
        NO PERMITE valores None o vacíos
        """
        required_fields = ['numero_cotizacion', 'tipo_vehiculo', 'precio_final']
        
        for field in required_fields:
            if field not in cotizacion or not cotizacion[field]:
                logger.error(f"❌ Campo requerido faltante o vacío en Mailtrap: {field}")
                return False
        
        return True
    
    def get_service_status(self) -> Dict[str, Any]:
        """Obtiene el estado del servicio Mailtrap"""
        return {
            'service': 'Mailtrap Service',
            'status': 'active',
            'provider': 'Mailtrap',
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'username_configured': bool(self.username and self.username != 'tu_mailtrap_username'),
            'cost': 'FREE',
            'monthly_limit': '1,000 emails/mes GRATIS',
            'perfect_for': 'Python applications like Barbara'
        } 