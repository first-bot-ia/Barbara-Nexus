"""
📱 WhatsApp PDF Service - Envío de PDFs por WhatsApp
==================================================
Servicio para enviar cotizaciones PDF por WhatsApp usando Twilio
"""

from twilio.rest import Client
import os
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin
import requests

logger = logging.getLogger(__name__)

class WhatsAppPDFService:
    """
    Servicio para enviar PDFs por WhatsApp usando Twilio
    """
    
    def __init__(self):
        # Configuración de Twilio desde variables de entorno
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN') 
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        
        # Inicializar client como None por defecto para evitar AttributeError
        self.client = None
        
        if not all([self.account_sid, self.auth_token]):
            logger.warning("⚠️ Credenciales de Twilio no configuradas completamente")
        else:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                logger.info("📱 WhatsApp PDF Service inicializado")
            except Exception as e:
                logger.error(f"❌ Error inicializando Twilio client: {e}")
                self.client = None
                
    
    def send_quotation_pdf(self, 
                          phone_number: str,
                          client_name: str,
                          cotizacion: Dict[str, Any],
                          pdf_url: Optional[str] = None) -> bool:
        """
        Envía cotización PDF por WhatsApp
        
        Args:
            phone_number: Número de teléfono del cliente
            client_name: Nombre del cliente
            cotizacion: Datos de la cotización
            pdf_url: URL del PDF (si no se proporciona, se genera)
            
        Returns:
            bool: True si se envió exitosamente
        """
        
        try:
            if not self.client:
                logger.error("❌ Cliente Twilio no inicializado")
                return False
            
            # Generar PDF si no se proporciona URL
            if not pdf_url:
                try:
                    from infrastructure.external_apis.pdf_generator_service import PDFGeneratorService
                    pdf_service = PDFGeneratorService()
                    pdf_path = pdf_service.generate_quotation_pdf(client_name, cotizacion)
                    
                    # Convertir a URL accesible (esto requiere servidor web)
                    # Para desarrollo, asumimos que el PDF está en assets/
                    pdf_filename = os.path.basename(pdf_path)
                    # En producción, esto debería ser una URL real del servidor
                    pdf_url = f"http://127.0.0.1:5000/assets/{pdf_filename}"
                    
                except Exception as e:
                    logger.error(f"❌ Error generando PDF: {e}")
                    return False
            
            # Formatear número de teléfono
            if not phone_number.startswith('whatsapp:'):
                if not phone_number.startswith('+'):
                    phone_number = f"+51{phone_number}"  # Asumir Perú si no hay código
                phone_number = f"whatsapp:{phone_number}"
            
            # Crear mensaje con PDF
            message_body = self._create_pdf_message(client_name, cotizacion)
            
            # Enviar mensaje con adjunto
            message = self.client.messages.create(
                body=message_body,
                from_=self.whatsapp_number,
                to=phone_number,
                media_url=[pdf_url]  # Adjuntar PDF
            )
            
            logger.info(f"📱 PDF enviado por WhatsApp a {phone_number} - SID: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando PDF por WhatsApp: {e}")
            return False
    
    def send_simple_pdf_message(self, 
                               phone_number: str,
                               client_name: str,
                               cotizacion: Dict[str, Any]) -> bool:
        """
        Envía mensaje simple con información de que el PDF va por email
        (Para cuando no se pueda adjuntar PDF directamente)
        """
        
        try:
            if not self.client:
                logger.error("❌ Cliente Twilio no inicializado")
                return False
            
            # Formatear número
            if not phone_number.startswith('whatsapp:'):
                if not phone_number.startswith('+'):
                    phone_number = f"+51{phone_number}"
                phone_number = f"whatsapp:{phone_number}"
            
            # Validar cotización ANTES de usar
            if not self._validate_cotizacion(cotizacion):
                logger.error("❌ Cotización inválida - faltan datos requeridos")
                return False
            
            # Mensaje informativo con datos reales - SIN valores estáticos
            message_body = f"""📋 ¡Hola {client_name}!

Tu cotización SOAT está lista:

🚗 Vehículo: {cotizacion['tipo_vehiculo']}
💰 Precio: {cotizacion['precio_final']}
📄 Cotización N°: {cotizacion['numero_cotizacion']}

📧 Te estoy enviando el PDF completo por correo electrónico.

¿Tienes alguna pregunta sobre tu cotización?"""
            
            message = self.client.messages.create(
                body=message_body,
                from_=self.whatsapp_number,
                to=phone_number
            )
            
            logger.info(f"📱 Mensaje PDF info enviado por WhatsApp a {phone_number}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando mensaje WhatsApp: {e}")
            return False
    
    def _create_pdf_message(self, client_name: str, cotizacion: Dict[str, Any]) -> str:
        """Crea mensaje para acompañar el PDF"""
        
        # Validar cotización ANTES de usar
        if not self._validate_cotizacion(cotizacion):
            return f"❌ Error: Cotización incompleta para {client_name}"
        
        return f"""📋 ¡Hola {client_name}!

Tu cotización SOAT completa está adjunta en PDF:

🚗 Vehículo: {cotizacion['tipo_vehiculo']}
💰 Precio Final: {cotizacion['precio_final']}
📄 Cotización N°: {cotizacion['numero_cotizacion']}
⏰ Válida por 15 días

📎 PDF adjunto con todos los detalles

¿Listo para proteger tu vehículo? ¡Contáctame para finalizar!"""
    
    def _validate_cotizacion(self, cotizacion: Dict[str, Any]) -> bool:
        """
        Valida que la cotización tenga todos los campos requeridos
        NO permite valores None o vacíos - TODO DEBE SER DINÁMICO
        """
        required_fields = ['tipo_vehiculo', 'precio_final', 'numero_cotizacion']
        
        for field in required_fields:
            if field not in cotizacion or not cotizacion[field] or cotizacion[field] == '':
                logger.error(f"❌ Campo requerido faltante o vacío: {field}")
                return False
        
        return True
    
    def get_service_status(self) -> Dict[str, Any]:
        """Obtiene estado del servicio WhatsApp"""
        return {
            'service': 'WhatsApp PDF Service',
            'status': 'active' if hasattr(self, 'client') and self.client else 'inactive',
            'provider': 'Twilio',
            'whatsapp_number': self.whatsapp_number,
            'features': [
                'Envío de PDF por WhatsApp',
                'Mensajes informativos',
                'Integración con Twilio',
                'Soporte multimedia'
            ],
            'configured': bool(self.account_sid and self.auth_token)
        } 