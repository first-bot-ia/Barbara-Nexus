"""
📧 Mailtrap API Service - Usando API Key del usuario
API Key: 1d7cb5e1a481fd392258b77261b63bea
Host: sandbox.api.mailtrap.io
"""

import requests
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class MailtrapAPIService:
    """
    Servicio de envío usando Mailtrap API
    Usa la API Key proporcionada por el usuario
    """
    
    def __init__(self):
        # Credenciales del usuario - Sandbox Email Testing
        self.api_token = "1d7cb5e1a481fd392258b77261b63bea"
        self.host = "mailtrap.io"
        # Usar endpoint correcto para Mailtrap API
        self.api_url = "https://send.api.mailtrap.io/api/send"
        
        self.sender_name = "Barbara - Autofondo Alese"
        self.sender_email = "barbara@autofondoalese.com"
        
    def send_quotation_email(self, 
                           recipient_email: str,
                           client_name: str,
                           cotizacion: Dict[str, Any]) -> bool:
        """
        Envía cotización por correo usando Mailtrap API
        
        Args:
            recipient_email: Email del destinatario
            client_name: Nombre del cliente
            cotizacion: Datos de la cotización
            
        Returns:
            bool: True si se envió exitosamente
        """
        
        try:
            # Preparar headers
            headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': 'application/json'
            }
            
            # Generar contenido del email
            html_content = self._generate_html_content(client_name, cotizacion)
            text_content = self._generate_text_content(client_name, cotizacion)
            
            # Preparar payload para Mailtrap API
            payload = {
                "from": {
                    "email": self.sender_email,
                    "name": self.sender_name
                },
                "to": [
                    {
                        "email": recipient_email,
                        "name": client_name
                    }
                ],
                "subject": f"Tu Cotización SOAT - {cotizacion.get('numero_cotizacion', 'AF2024')}",
                "html": html_content,
                "text": text_content,
                "category": "Barbara SOAT Quotations"
            }
            
            # Enviar request a Mailtrap API
            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"📧 Cotización enviada por Mailtrap API a {recipient_email}")
                return True
            else:
                logger.error(f"❌ Error Mailtrap API: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error enviando email con Mailtrap API: {e}")
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
                    <span class="detail-value">{cotizacion.get('tipo_vehiculo', 'Auto particular')}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Cotización N°:</span>
                    <span class="detail-value">{cotizacion.get('numero_cotizacion', 'AF2024001')}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Fecha:</span>
                    <span class="detail-value">{datetime.now().strftime('%d/%m/%Y')}</span>
                </div>
            </div>
            
            <div class="precio-destacado">
                <div>💰 Precio Final</div>
                <div class="amount">{cotizacion.get('precio_final', 'S/ 165.00')}</div>
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
        """Genera contenido de texto plano"""
        
        return f"""🛡️ TU COTIZACIÓN SOAT - AUTOFONDO ALESE

¡Hola {client_name}!

Te enviamos tu cotización personalizada generada por Barbara:

📋 DETALLES DE TU COTIZACIÓN
================================
Cliente: {client_name}
Vehículo: {cotizacion.get('tipo_vehiculo', 'Auto particular')}
Cotización N°: {cotizacion.get('numero_cotizacion', 'AF2024001')}
Fecha: {datetime.now().strftime('%d/%m/%Y')}

💰 PRECIO FINAL: {cotizacion.get('precio_final', 'S/ 165.00')}

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
    
    def get_service_status(self) -> Dict[str, Any]:
        """Obtiene el estado del servicio Mailtrap API"""
        return {
            'service': 'Mailtrap API Service',
            'status': 'active',
            'provider': 'Mailtrap API',
            'host': self.host,
            'api_token': self.api_token[:10] + '...',  # Ocultar token completo
            'api_url': self.api_url,
            'cost': 'FREE',
            'monthly_limit': '1,000 emails/mes GRATIS',
            'perfect_for': 'Python applications like Barbara'
        } 