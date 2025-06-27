"""
📧 EmailJS Service - Servicio de envío usando EmailJS (GRATIS)
Usa las credenciales existentes del usuario
"""

import requests
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class EmailJSService:
    """
    Servicio de envío de correos usando EmailJS (100% GRATIS)
    Usa las credenciales ya configuradas del usuario
    """
    
    def __init__(self):
        # Credenciales existentes del usuario
        self.service_id = "service_07w2v5c"
        self.template_id = "template_u4pwglv"
        self.public_key = "X-95hw1AjZ84R4LjG"
        self.api_url = "https://api.emailjs.com/api/v1.0/email/send"
        
    def send_quotation_email(self, 
                           recipient_email: str,
                           client_name: str,
                           cotizacion: Dict[str, Any]) -> bool:
        """
        Envía cotización por correo electrónico usando EmailJS
        
        Args:
            recipient_email: Email del destinatario
            client_name: Nombre del cliente
            cotizacion: Datos de la cotización
            
        Returns:
            bool: True si se envió exitosamente
        """
        
        try:
            # Generar mensaje personalizado
            message = self._generate_email_message(client_name, cotizacion)
            
            # Preparar datos para EmailJS
            template_params = {
                'to_email': recipient_email,
                'to_name': client_name,
                'from_name': 'Barbara - Autofondo Alese',
                'reply_to': 'info@autofondoalese.com',
                'subject': f'Tu Cotización SOAT - {cotizacion.get("numero_cotizacion", "AF2024")}',
                'message': message,
                'vehicle_type': cotizacion.get('tipo_vehiculo', 'Auto particular'),
                'price_final': cotizacion.get('precio_final', 'S/ 165.00'),
                'quotation_number': cotizacion.get('numero_cotizacion', 'AF2024001'),
                'company_phone': '+51 999 888 777',
                'company_email': 'info@autofondoalese.com'
            }
            
            # Payload para EmailJS
            payload = {
                'service_id': self.service_id,
                'template_id': self.template_id,
                'user_id': self.public_key,
                'template_params': template_params
            }
            
            # Enviar request a EmailJS
            headers = {
                'Content-Type': 'application/json',
            }
            
            response = requests.post(
                self.api_url, 
                data=json.dumps(payload), 
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"📧 Cotización enviada por EmailJS a {recipient_email}")
                return True
            else:
                logger.error(f"❌ Error EmailJS: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error enviando email con EmailJS: {e}")
            return False
    
    def _generate_email_message(self, client_name: str, cotizacion: Dict[str, Any]) -> str:
        """Genera mensaje de email personalizado"""
        
        return f"""Estimado/a {client_name},

¡Gracias por tu interés en nuestros seguros SOAT!

Te enviamos tu cotización personalizada generada por Barbara:

🚗 DATOS DE TU COTIZACIÓN:
• Cliente: {client_name}
• Vehículo: {cotizacion.get('tipo_vehiculo', 'Auto particular')}
• Cotización N°: {cotizacion.get('numero_cotizacion', 'AF2024001')}
• Fecha: {datetime.now().strftime('%d/%m/%Y')}

💰 PRECIO FINAL: {cotizacion.get('precio_final', 'S/ 165.00')}

✅ COBERTURA SOAT 2024:
• Muerte por accidente: 4 UIT (S/ 20,400)
• Gastos médicos: Hasta 5 UIT (S/ 25,500)
• Invalidez permanente: Hasta 4 UIT (S/ 20,400)
• Gastos de sepelio: Hasta 1 UIT (S/ 5,100)

🏆 ASEGURADORAS DISPONIBLES:
• Interseguro • RIMAC • Pacífico • MAPFRE • La Positiva

⏰ OFERTA VÁLIDA POR 15 DÍAS

📞 FINALIZAR COMPRA:
• Teléfono: +51 999 888 777
• WhatsApp: 999-919-133
• Email: info@autofondoalese.com

¿Listo para proteger tu vehículo?
¡Contactanos para finalizar tu SOAT!

Saludos cordiales,
Barbara & Equipo Autofondo Alese
Líderes en seguros vehiculares

---
Este email fue generado automáticamente por Barbara, tu asesora digital.
Si tienes alguna pregunta, no dudes en contactarnos."""
    
    def send_test_email(self, recipient_email: str) -> bool:
        """Envía un email de prueba"""
        
        try:
            template_params = {
                'to_email': recipient_email,
                'to_name': 'Cliente Prueba',
                'from_name': 'Barbara - Autofondo Alese',
                'subject': 'Prueba - Sistema Barbara',
                'message': 'Este es un email de prueba del sistema Barbara usando EmailJS.',
                'company_phone': '+51 999 888 777'
            }
            
            payload = {
                'service_id': self.service_id,
                'template_id': self.template_id,
                'user_id': self.public_key,
                'template_params': template_params
            }
            
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(
                self.api_url, 
                data=json.dumps(payload), 
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"📧 Email de prueba enviado a {recipient_email}")
                return True
            else:
                logger.error(f"❌ Error en prueba EmailJS: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error enviando email de prueba: {e}")
            return False
    
    def get_service_status(self) -> Dict[str, Any]:
        """Obtiene el estado del servicio EmailJS"""
        return {
            'service': 'EmailJS Service',
            'status': 'active',
            'provider': 'EmailJS',
            'service_id': self.service_id,
            'template_id': self.template_id,
            'public_key': self.public_key[:10] + '...',  # Ocultar key completa
            'api_url': self.api_url,
            'cost': 'FREE',
            'monthly_limit': '200 emails/mes GRATIS'
        } 