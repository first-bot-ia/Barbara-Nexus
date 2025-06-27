"""
📧 Mailtrap SMTP Sending Service - CREDENCIALES REALES
====================================================
Usando las credenciales de envío real de Mailtrap del usuario:
- Host: live.smtp.mailtrap.io
- API Token: 3ad4786fc1d172fb1f2bac6a8ee017c2
- Username: smtp@mailtrap.io
- Port: 587 con STARTTLS
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Any, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class MailtrapSendingService:
    """
    Servicio de envío real usando Mailtrap SMTP Sending
    Con las credenciales reales del usuario para enviar emails
    """
    
    def __init__(self):
        # Credenciales reales de Mailtrap Sending del usuario
        self.smtp_host = "live.smtp.mailtrap.io"
        self.smtp_port = 587
        self.smtp_username = "smtp@mailtrap.io"
        self.smtp_password = "3ad4786fc1d172fb1f2bac6a8ee017c2"  # Su API Token
        
        # Configuración del remitente
        self.sender_name = "Barbara - Autofondo Alese"
        self.sender_email = "barbara@demomailtrap.co"  # Usando el dominio verificado
        
        logger.info("🚀 Mailtrap Sending Service inicializado con credenciales reales")
    
    def send_quotation_email(self, 
                           recipient_email: str,
                           client_name: str,
                           cotizacion: Dict[str, Any],
                           attach_pdf: bool = True) -> bool:
        """
        Envía cotización por correo usando Mailtrap SMTP Sending REAL
        
        Args:
            recipient_email: Email del destinatario
            client_name: Nombre del cliente
            cotizacion: Datos de la cotización (DEBE tener todos los valores requeridos)
            attach_pdf: Si debe adjuntar PDF (default: True)
            
        Returns:
            bool: True si se envió exitosamente
        """
        
        try:
            # Validar datos de entrada
            if not self._validate_cotizacion_data(cotizacion):
                logger.error("❌ Cotización inválida - faltan datos requeridos")
                return False
            
            # Crear mensaje
            msg = MIMEMultipart('mixed')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = recipient_email
            msg['Subject'] = f"Tu Cotización SOAT - {cotizacion['numero_cotizacion']}"
            
            # Crear parte alternativa para texto/HTML
            msg_alternative = MIMEMultipart('alternative')
            
            # Generar contenido HTML y texto
            html_content = self._generate_html_content(client_name, cotizacion)
            text_content = self._generate_text_content(client_name, cotizacion)
            
            # Adjuntar contenido texto/HTML
            msg_alternative.attach(MIMEText(text_content, 'plain', 'utf-8'))
            msg_alternative.attach(MIMEText(html_content, 'html', 'utf-8'))
            msg.attach(msg_alternative)
            
            # Generar y adjuntar PDF si se solicita
            if attach_pdf:
                try:
                    from infrastructure.external_apis.pdf_generator_service import PDFGeneratorService
                    pdf_service = PDFGeneratorService()
                    pdf_path = pdf_service.generate_quotation_pdf(client_name, cotizacion)
                    
                    # Adjuntar PDF
                    with open(pdf_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    filename = f"Cotizacion_SOAT_{cotizacion['numero_cotizacion']}.pdf"
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {filename}'
                    )
                    msg.attach(part)
                    
                    logger.info(f"📎 PDF adjuntado: {filename}")
                    
                except Exception as pdf_error:
                    logger.warning(f"⚠️ Error adjuntando PDF: {pdf_error}")
                    # Continuar enviando email sin PDF
            
            # Conectar y enviar
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()  # Habilitar STARTTLS como es requerido
            server.login(self.smtp_username, self.smtp_password)
            
            # Enviar email
            text = msg.as_string()
            server.sendmail(self.sender_email, recipient_email, text)
            server.quit()
            
            attachment_info = " con PDF adjunto" if attach_pdf else ""
            logger.info(f"📧 Email REAL enviado exitosamente{attachment_info} a {recipient_email} via Mailtrap Sending")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando email con Mailtrap Sending: {e}")
            return False
    
    def _generate_html_content(self, client_name: str, cotizacion: Dict[str, Any]) -> str:
        """Genera contenido HTML profesional para el email"""
        
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tu Cotización SOAT</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f4f4f4; }}
        .container {{ background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 40px 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: bold; }}
        .header p {{ margin: 10px 0 0 0; font-size: 16px; opacity: 0.9; }}
        .content {{ padding: 40px 30px; }}
        .greeting {{ font-size: 20px; color: #1e3a8a; margin-bottom: 20px; }}
        .cotizacion-box {{ background: #f8fafc; border: 2px solid #e2e8f0; border-radius: 10px; padding: 25px; margin: 25px 0; }}
        .cotizacion-box h3 {{ color: #1e3a8a; margin-top: 0; font-size: 18px; }}
        .detail-row {{ display: flex; justify-content: space-between; margin: 12px 0; padding: 8px 0; border-bottom: 1px solid #e2e8f0; }}
        .detail-label {{ font-weight: bold; color: #64748b; }}
        .detail-value {{ color: #334155; }}
        .precio-destacado {{ background: linear-gradient(135deg, #059669 0%, #10b981 100%); color: white; padding: 25px; border-radius: 10px; text-align: center; margin: 25px 0; }}
        .precio-destacado .amount {{ font-size: 32px; font-weight: bold; margin: 10px 0; }}
        .beneficios {{ background: #ecfdf5; border-left: 4px solid #10b981; padding: 20px; margin: 25px 0; border-radius: 0 8px 8px 0; }}
        .beneficios h3 {{ color: #059669; margin-top: 0; }}
        .beneficios ul {{ margin: 10px 0; padding-left: 20px; }}
        .beneficios li {{ margin: 8px 0; color: #374151; }}
        .cta-section {{ text-align: center; margin: 30px 0; }}
        .cta-button {{ background: #1e3a8a; color: white; padding: 16px 32px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: bold; font-size: 16px; transition: background 0.3s; }}
        .cta-button:hover {{ background: #1e40af; }}
        .footer {{ background: #f8fafc; padding: 25px; text-align: center; color: #64748b; border-top: 1px solid #e2e8f0; }}
        .footer .company {{ font-weight: bold; color: #1e3a8a; margin-bottom: 10px; }}
        .footer .contact {{ font-size: 14px; line-height: 1.8; }}
        .urgency {{ background: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 15px; margin: 20px 0; text-align: center; }}
        .urgency strong {{ color: #92400e; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Tu Cotización SOAT</h1>
            <p>Protección completa para tu vehículo</p>
        </div>
        
        <div class="content">
            <div class="greeting">¡Hola {client_name}!</div>
            
            <p>Barbara ha preparado tu cotización personalizada de SOAT. Aquí tienes todos los detalles:</p>
            
            <div class="cotizacion-box">
                <h3>📋 Detalles de tu Cotización</h3>
                <div class="detail-row">
                    <span class="detail-label">Cliente:</span>
                    <span class="detail-value">{client_name}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Vehículo:</span>
                    <span class="detail-value">{cotizacion['tipo_vehiculo']}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Cotización N°:</span>
                    <span class="detail-value">{cotizacion['numero_cotizacion']}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Fecha:</span>
                    <span class="detail-value">{datetime.now().strftime('%d/%m/%Y')}</span>
                </div>
            </div>
            
            <div class="precio-destacado">
                <div>💰 Precio Final</div>
                <div class="amount">{cotizacion['precio_final']}</div>
                <div>Incluye IGV y cobertura completa</div>
            </div>
            
            <div class="beneficios">
                <h3>✅ Tu SOAT Incluye:</h3>
                <ul>
                    <li><strong>Gastos médicos:</strong> Hasta 5 UIT (S/ 25,500)</li>
                    <li><strong>Muerte por accidente:</strong> Hasta 4 UIT (S/ 20,400)</li>
                    <li><strong>Invalidez permanente:</strong> Hasta 4 UIT (S/ 20,400)</li>
                    <li><strong>Gastos de sepelio:</strong> Hasta 1 UIT (S/ 5,100)</li>
                    <li><strong>Cobertura 24/7</strong> todos los días del año</li>
                    <li><strong>Atención médica inmediata</strong> en caso de accidente</li>
                </ul>
            </div>
            
            <div class="urgency">
                <strong>⏰ Oferta válida por 15 días.</strong> No dejes pasar esta oportunidad de proteger tu vehículo al mejor precio.
            </div>
            
            <div class="cta-section">
                <a href="tel:+51999888777" class="cta-button">
                    📞 Finalizar Compra: +51 999 888 777
                </a>
            </div>
            
            <p style="text-align: center; color: #64748b; margin-top: 30px;">
                ¿Listo para proteger tu vehículo?<br>
                ¡Contactanos para finalizar tu SOAT!
            </p>
        </div>
        
        <div class="footer">
            <div class="company">Barbara & Equipo Autofondo Alese</div>
            <div class="contact">
                Tu compañía de seguros de confianza<br>
                📧 info@autofondoalese.com | 📞 +51 999 888 777<br>
                WhatsApp: 999-919-133
            </div>
            <p style="font-size: 12px; margin-top: 15px; opacity: 0.7;">
                Este email fue generado automáticamente por Barbara, tu asesora digital.<br>
                Si tienes alguna pregunta, no dudes en contactarnos.
            </p>
        </div>
    </div>
</body>
</html>
        """
    
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
- Muerte por accidente: Hasta 4 UIT (S/ 20,400)
- Invalidez permanente: Hasta 4 UIT (S/ 20,400)
- Gastos de sepelio: Hasta 1 UIT (S/ 5,100)
- Cobertura 24/7 todos los días del año
- Atención médica inmediata en caso de accidente

⏰ OFERTA VÁLIDA POR 15 DÍAS

Para finalizar tu compra, contacta:
📞 +51 999 888 777
📧 info@autofondoalese.com
WhatsApp: 999-919-133

¿Listo para proteger tu vehículo?
¡Contactanos para finalizar tu SOAT!

---
Barbara & Equipo Autofondo Alese
Tu compañía de seguros de confianza

Este email fue generado automáticamente por Barbara, tu asesora digital.
Si tienes alguna pregunta, no dudes en contactarnos."""
    
    def _validate_cotizacion_data(self, cotizacion: Dict[str, Any]) -> bool:
        """
        Valida que la cotización tenga todos los datos necesarios
        NO PERMITE valores None o vacíos
        """
        required_fields = ['numero_cotizacion', 'tipo_vehiculo', 'precio_final']
        
        for field in required_fields:
            if field not in cotizacion or not cotizacion[field]:
                logger.error(f"❌ Campo requerido faltante o vacío en Mailtrap Sending: {field}")
                return False
        
        return True
    
    def get_service_status(self) -> Dict[str, Any]:
        """Obtiene el estado del servicio Mailtrap Sending"""
        return {
            'service': 'Mailtrap SMTP Sending Service',
            'status': 'active',
            'provider': 'Mailtrap SMTP Sending (REAL)',
            'host': self.smtp_host,
            'port': self.smtp_port,
            'username': self.smtp_username,
            'api_token': self.smtp_password[:10] + '...',  # Ocultar token completo
            'sender_email': self.sender_email,
            'cost': 'FREE',
            'monthly_limit': '1,000 emails/mes GRATIS',
            'email_type': 'EMAILS REALES a direcciones reales',
            'perfect_for': 'Barbara enviando cotizaciones SOAT'
        } 