"""
📧 Email Service - Servicio de envío de correos electrónicos
Integrado con la arquitectura DDD de Barbara
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import os
from jinja2 import Template

logger = logging.getLogger(__name__)

class EmailService:
    """
    Servicio de envío de correos electrónicos para cotizaciones SOAT
    """
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("SENDER_EMAIL", "tu-email@gmail.com")
        self.sender_password = os.getenv("SENDER_PASSWORD", "tu-app-password")
        self.sender_name = "Barbara - Autofondo Alese"
        
    def send_quotation_email(self, 
                           recipient_email: str,
                           client_name: str,
                           cotizacion: Dict[str, Any]) -> bool:
        """
        Envía cotización por correo electrónico
        
        Args:
            recipient_email: Email del destinatario
            client_name: Nombre del cliente
            cotizacion: Datos de la cotización
            
        Returns:
            bool: True si se envió exitosamente
        """
        
        try:
            # Crear mensaje
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Tu Cotización SOAT - {cotizacion['numero_cotizacion']}"
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = recipient_email
            
            # Generar contenido HTML
            html_content = self._generate_html_content(client_name, cotizacion)
            
            # Generar contenido de texto plano
            text_content = self._generate_text_content(client_name, cotizacion)
            
            # Crear partes del mensaje
            text_part = MIMEText(text_content, "plain", "utf-8")
            html_part = MIMEText(html_content, "html", "utf-8")
            
            # Adjuntar partes
            message.attach(text_part)
            message.attach(html_part)
            
            # Enviar email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            logger.info(f"📧 Cotización enviada por email a {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando email: {e}")
            return False
    
    def _generate_html_content(self, client_name: str, cotizacion: Dict[str, Any]) -> str:
        """Genera contenido HTML para el email"""
        
        template_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tu Cotización SOAT</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }
        .content {
            background: #f9f9f9;
            padding: 30px;
            border-radius: 0 0 10px 10px;
        }
        .cotizacion-box {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .precio-destacado {
            font-size: 28px;
            font-weight: bold;
            color: #1e3c72;
            text-align: center;
            background: #e8f4f8;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .beneficios {
            background: #e8f5e8;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .beneficios ul {
            margin: 0;
            padding-left: 20px;
        }
        .cta-button {
            background: #2a5298;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            margin: 20px 0;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
        }
        .highlight {
            color: #2a5298;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Tu Cotización SOAT</h1>
        <p>Protección completa para tu vehículo</p>
    </div>
    
    <div class="content">
        <h2>¡Hola {{ client_name }}!</h2>
        
        <p>Te enviamos tu cotización personalizada de SOAT. Barbara ha preparado la mejor opción para ti:</p>
        
        <div class="cotizacion-box">
            <h3>📋 Detalles de tu Cotización</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Cliente:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #eee;">{{ client_name }}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Vehículo:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #eee;">{{ cotizacion.tipo_vehiculo }}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Vigencia:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #eee;">1 año completo</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Cotización N°:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #eee;">{{ cotizacion.numero_cotizacion }}</td>
                </tr>
                <tr>
                    <td style="padding: 10px;"><strong>Válida hasta:</strong></td>
                    <td style="padding: 10px;">{{ cotizacion.fecha_vencimiento }}</td>
                </tr>
            </table>
        </div>
        
        <div class="precio-destacado">
            💰 Precio Final: {{ cotizacion.precio_final }}
        </div>
        
        <div class="beneficios">
            <h3>✅ Tu SOAT Incluye:</h3>
            <ul>
                <li><strong>Gastos médicos:</strong> Hasta 5 UIT (S/ 25,500)</li>
                <li><strong>Muerte:</strong> Hasta 4 UIT (S/ 20,400)</li>
                <li><strong>Invalidez permanente:</strong> Hasta 4 UIT (S/ 20,400)</li>
                <li><strong>Gastos de sepelio:</strong> Hasta 1 UIT (S/ 5,100)</li>
                <li><strong>Cobertura las 24 horas</strong> todos los días del año</li>
                <li><strong>Atención médica inmediata</strong> en caso de accidente</li>
            </ul>
        </div>
        
        <div style="text-align: center;">
            <a href="tel:+51999888777" class="cta-button">
                📞 Finalizar Compra: +51 999 888 777
            </a>
        </div>
        
        <p style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <strong>⏰ Oferta válida por 15 días.</strong> No dejes pasar esta oportunidad de proteger tu vehículo al mejor precio.
        </p>
        
    </div>
    
    <div class="footer">
        <p>
            <strong>Autofondo Alese</strong><br>
            Tu compañía de seguros de confianza<br>
            📧 info@autofondoalese.com | 📞 +51 999 888 777
        </p>
        <p style="font-size: 12px; color: #999; margin-top: 15px;">
            Este email fue generado automáticamente por Barbara, tu asesora digital.<br>
            Si tienes alguna pregunta, no dudes en contactarnos.
        </p>
    </div>
</body>
</html>
        """
        
        template = Template(template_html)
        return template.render(client_name=client_name, cotizacion=cotizacion)
    
    def _generate_text_content(self, client_name: str, cotizacion: Dict[str, Any]) -> str:
        """Genera contenido de texto plano para el email"""
        
        return f"""
🛡️ TU COTIZACIÓN SOAT - AUTOFONDO ALESE

¡Hola {client_name}!

Te enviamos tu cotización personalizada de SOAT:

📋 DETALLES DE TU COTIZACIÓN
================================
Cliente: {client_name}
Vehículo: {cotizacion.get('tipo_vehiculo', 'Auto particular')}
Vigencia: 1 año completo
Cotización N°: {cotizacion.get('numero_cotizacion', 'N/A')}
Válida hasta: {cotizacion.get('fecha_vencimiento', 'N/A')}

💰 PRECIO FINAL: {cotizacion.get('precio_final', 'N/A')}

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

---
Autofondo Alese
Tu compañía de seguros de confianza
📧 info@autofondoalese.com
        """
    
    def send_test_email(self, recipient_email: str) -> bool:
        """Envía un email de prueba"""
        
        try:
            message = MIMEText("Este es un email de prueba del sistema Barbara.")
            message["Subject"] = "Prueba - Sistema Barbara"
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = recipient_email
            
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            logger.info(f"📧 Email de prueba enviado a {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando email de prueba: {e}")
            return False
    
    def get_service_status(self) -> Dict[str, Any]:
        """Obtiene el estado del servicio de email"""
        return {
            'service': 'Email Service',
            'status': 'active',
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'sender_configured': bool(self.sender_email and self.sender_password)
        } 