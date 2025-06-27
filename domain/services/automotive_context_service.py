"""
🚗 Automotive Context Service
Servicio especializado de contexto automotriz para Barbara

Basado en investigación de:
- Mejores prácticas de concesionarios automotrices
- Patrones de conversación de asesores digitales
- Conocimiento especializado del sector seguros vehiculares
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass
import logging
import re
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class VehicleCategory(Enum):
    """Categorías de vehículos"""
    AUTO_PARTICULAR = "auto_particular"
    TAXI = "taxi"
    MOTOCICLETA = "motocicleta"
    CAMIONETA = "camioneta"
    SUV = "suv"
    PICKUP = "pickup"
    COMERCIAL = "comercial"
    CLASICO = "clasico"

class InsuranceType(Enum):
    """Tipos de seguros"""
    SOAT = "soat"
    VEHICULAR = "vehicular"
    CONTRA_TERCEROS = "contra_terceros"
    TODO_RIESGO = "todo_riesgo"

class CustomerProfile(Enum):
    """Perfiles de cliente"""
    FIRST_TIME_BUYER = "first_time_buyer"
    EXPERIENCED_DRIVER = "experienced_driver"
    FLEET_OWNER = "fleet_owner"
    YOUNG_DRIVER = "young_driver"
    SENIOR_DRIVER = "senior_driver"
    BUSINESS_OWNER = "business_owner"

@dataclass
class VehicleInfo:
    """Información detallada del vehículo"""
    categoria: VehicleCategory
    marca: Optional[str] = None
    modelo: Optional[str] = None
    año: Optional[int] = None
    placa: Optional[str] = None
    uso: Optional[str] = None  # particular, taxi, comercial
    valor_comercial: Optional[float] = None
    ciudad: Optional[str] = "Lima"
    
class AutomotiveContextService:
    """
    Servicio especializado en contexto automotriz
    
    Proporciona:
    - Reconocimiento avanzado de vehículos
    - Contexto especializado de seguros
    - Perfilado inteligente de clientes
    - Recomendaciones personalizadas
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Base de conocimiento automotriz
        self.vehicle_database = self._initialize_vehicle_database()
        self.insurance_knowledge = self._initialize_insurance_knowledge()
        self.customer_personas = self._initialize_customer_personas()
        
        # Patrones de reconocimiento
        self.vehicle_patterns = self._initialize_vehicle_patterns()
        self.price_ranges = self._initialize_price_ranges()
    
    def _initialize_vehicle_database(self) -> Dict[str, Any]:
        """Inicializa base de datos de vehículos populares en Perú"""
        return {
            "marcas_populares": {
                "toyota": {
                    "modelos": ["corolla", "yaris", "rav4", "hilux", "prius", "camry"],
                    "segmento": "confiable",
                    "precio_soat_promedio": {"2024": 153, "2023": 145, "2022": 138}
                },
                "hyundai": {
                    "modelos": ["accent", "elantra", "tucson", "santa fe", "grand i10"],
                    "segmento": "economico",
                    "precio_soat_promedio": {"2024": 148, "2023": 140, "2022": 133}
                },
                "kia": {
                    "modelos": ["rio", "cerato", "sportage", "sorento", "picanto"],
                    "segmento": "moderno",
                    "precio_soat_promedio": {"2024": 150, "2023": 142, "2022": 135}
                },
                "nissan": {
                    "modelos": ["sentra", "altima", "x-trail", "frontier", "march"],
                    "segmento": "versatil",
                    "precio_soat_promedio": {"2024": 152, "2023": 144, "2022": 137}
                },
                "chevrolet": {
                    "modelos": ["sail", "cruze", "tracker", "colorado", "spark"],
                    "segmento": "americano",
                    "precio_soat_promedio": {"2024": 155, "2023": 147, "2022": 140}
                },
                "honda": {
                    "modelos": ["civic", "accord", "cr-v", "hr-v", "fit"],
                    "segmento": "premium",
                    "precio_soat_promedio": {"2024": 158, "2023": 150, "2022": 143}
                }
            },
            "categorias_especiales": {
                "taxi": {
                    "modelos_populares": ["toyota yaris", "nissan sentra", "hyundai accent"],
                    "consideraciones": "Requiere SOAT comercial, mayor desgaste, revisiones frecuentes"
                },
                "delivery": {
                    "vehiculos": ["motos lineales", "scooters", "autos compactos"],
                    "consideraciones": "Alto riesgo, seguro especializado recomendado"
                }
            }
        }
    
    def _initialize_insurance_knowledge(self) -> Dict[str, Any]:
        """Inicializa conocimiento especializado de seguros"""
        return {
            "soat_2024": {
                "auto_particular": {
                    "precio_base": 153,
                    "cobertura": "Lesiones: S/4 UIT, Muerte: S/4 UIT, Incapacidad: S/1 UIT, Gastos médicos: S/5 UIT",
                    "vigencia": "1 año",
                    "descuentos": {
                        "buen_conductor": 0.05,
                        "cliente_recurrente": 0.03,
                        "pago_anual": 0.02
                    }
                },
                "taxi": {
                    "precio_base": 298,
                    "consideraciones": "Tarifa comercial, mayor cobertura requerida",
                    "documentos_adicionales": ["licencia profesional", "certificado municipalidad"]
                },
                "moto": {
                    "precio_base": 89,
                    "cobertura_reducida": "Menor cobertura que autos",
                    "riesgo_alto": "Mayor accidentalidad estadística"
                }
            },
            "seguros_adicionales": {
                "vehicular_completo": {
                    "beneficios": "Choque, robo, incendio, fenómenos naturales",
                    "costo_promedio": "3-5% valor comercial vehículo",
                    "recomendado_para": "vehículos nuevos o de alto valor"
                },
                "contra_terceros": {
                    "beneficios": "Daños a terceros hasta $50,000",
                    "costo_promedio": "$200-400 anuales",
                    "recomendado_para": "conductores experimentados"
                }
            }
        }
    
    def _initialize_customer_personas(self) -> Dict[str, Any]:
        """Inicializa perfiles de cliente"""
        return {
            CustomerProfile.FIRST_TIME_BUYER: {
                "caracteristicas": "Nervioso, necesita explicaciones detalladas, precio sensible",
                "approach": "Educativo, paciente, paso a paso",
                "concerns": ["precio", "cobertura básica", "proceso simple"],
                "recommendations": "SOAT básico, explicar beneficios claramente"
            },
            CustomerProfile.EXPERIENCED_DRIVER: {
                "caracteristicas": "Conoce el proceso, busca eficiencia, compara precios",
                "approach": "Directo, profesional, destacar valor",
                "concerns": ["mejor precio", "servicio rápido", "beneficios adicionales"],
                "recommendations": "Ofertas especiales, descuentos por lealtad"
            },
            CustomerProfile.FLEET_OWNER: {
                "caracteristicas": "Múltiples vehículos, busca descuentos por volumen",
                "approach": "Empresarial, enfoque en ahorro total",
                "concerns": ["descuentos por volumen", "gestión centralizada", "facturación empresarial"],
                "recommendations": "Paquetes empresariales, gestión dedicada"
            },
            CustomerProfile.YOUNG_DRIVER: {
                "caracteristicas": "Digital nativo, precio sensible, busca conveniencia",
                "approach": "Moderno, digital, rápido",
                "concerns": ["precio accesible", "proceso online", "pagos flexibles"],
                "recommendations": "Promociones jóvenes, pago en cuotas"
            }
        }
    
    def _initialize_vehicle_patterns(self) -> Dict[str, List[str]]:
        """Inicializa patrones de reconocimiento de vehículos"""
        return {
            "marcas": [
                r"\btoyota\b", r"\thyundai\b", r"\tkia\b", r"\tnissan\b", 
                r"\tchevrolet\b", r"\thonda\b", r"\tford\b", r"\tmazda\b",
                r"\tsubaru\b", r"\tmitsubishi\b", r"\tvolkswagen\b", r"\tbmw\b"
            ],
            "tipos_vehiculo": [
                r"\bauto\b", r"\bcarro\b", r"\tvehículo\b", r"\tmoto\b",
                r"\bmotocicleta\b", r"\tcamioneta\b", r"\tsuv\b", r"\ttaxi\b"
            ],
            "años": [
                r"\b(19|20)\d{2}\b",  # Años 1900-20XX
                r"\b(nuevo|nueva)\b", r"\b(usado|usada)\b"
            ],
            "placas": [
                r"\b[A-Z]{3}-\d{3}\b",  # Placas nuevas ABC-123
                r"\b[A-Z]{2}-\d{4}\b",  # Placas antiguas AB-1234
                r"\b\d{3}-\d{3}\b"     # Solo números
            ]
        }
    
    def _initialize_price_ranges(self) -> Dict[str, Dict[str, float]]:
        """Inicializa rangos de precios por categoría"""
        return {
            "soat_2024": {
                "auto_particular": {"min": 145, "max": 165, "promedio": 153},
                "taxi": {"min": 280, "max": 320, "promedio": 298},
                "moto_hasta_250cc": {"min": 75, "max": 95, "promedio": 89},
                "moto_mas_250cc": {"min": 105, "max": 125, "promedio": 115},
                "camioneta": {"min": 160, "max": 190, "promedio": 175}
            }
        }
    
    def analyze_vehicle_mention(self, message: str) -> VehicleInfo:
        """
        Analiza menciones de vehículos en el mensaje
        """
        message_lower = message.lower()
        
        # Detectar categoría
        categoria = self._detect_vehicle_category(message_lower)
        
        # Detectar marca y modelo
        marca, modelo = self._detect_brand_and_model(message_lower)
        
        # Detectar año
        año = self._detect_year(message)
        
        # Detectar placa
        placa = self._detect_plate(message)
        
        # Detectar uso
        uso = self._detect_usage(message_lower)
        
        vehicle_info = VehicleInfo(
            categoria=categoria,
            marca=marca,
            modelo=modelo,
            año=año,
            placa=placa,
            uso=uso
        )
        
        self.logger.info(f"🚗 Vehículo detectado: {vehicle_info}")
        return vehicle_info
    
    def _detect_vehicle_category(self, message: str) -> VehicleCategory:
        """Detecta la categoría del vehículo"""
        if any(word in message for word in ["taxi", "colectivo"]):
            return VehicleCategory.TAXI
        elif any(word in message for word in ["moto", "motocicleta", "scooter"]):
            return VehicleCategory.MOTOCICLETA
        elif any(word in message for word in ["camioneta", "pickup", "4x4"]):
            return VehicleCategory.CAMIONETA
        elif any(word in message for word in ["suv", "todoterreno"]):
            return VehicleCategory.SUV
        else:
            return VehicleCategory.AUTO_PARTICULAR
    
    def _detect_brand_and_model(self, message: str) -> Tuple[Optional[str], Optional[str]]:
        """Detecta marca y modelo del vehículo"""
        marca_detectada = None
        modelo_detectado = None
        
        for marca, info in self.vehicle_database["marcas_populares"].items():
            if marca in message:
                marca_detectada = marca.title()
                
                # Buscar modelo específico
                for modelo in info["modelos"]:
                    if modelo in message:
                        modelo_detectado = modelo.title()
                        break
                break
        
        return marca_detectada, modelo_detectado
    
    def _detect_year(self, message: str) -> Optional[int]:
        """Detecta el año del vehículo"""
        import re
        year_pattern = r'\b(19|20)\d{2}\b'
        matches = re.findall(year_pattern, message)
        
        if matches:
            years = [int(match[0] + match[1:]) for match in matches]
            # Filtrar años válidos para vehículos (1980-2025)
            valid_years = [y for y in years if 1980 <= y <= 2025]
            if valid_years:
                return max(valid_years)  # Retornar el año más reciente mencionado
        
        return None
    
    def _detect_plate(self, message: str) -> Optional[str]:
        """Detecta la placa del vehículo"""
        import re
        plate_patterns = [
            r'\b[A-Z]{3}-\d{3}\b',  # ABC-123
            r'\b[A-Z]{2}-\d{4}\b',  # AB-1234
        ]
        
        for pattern in plate_patterns:
            match = re.search(pattern, message.upper())
            if match:
                return match.group()
        
        return None
    
    def _detect_usage(self, message: str) -> Optional[str]:
        """Detecta el uso del vehículo"""
        if any(word in message for word in ["taxi", "colectivo", "comercial"]):
            return "comercial"
        elif any(word in message for word in ["particular", "personal", "familia"]):
            return "particular"
        elif any(word in message for word in ["delivery", "reparto", "trabajo"]):
            return "trabajo"
        
        return "particular"  # Por defecto
    
    def get_price_estimate(self, vehicle_info: VehicleInfo) -> Dict[str, Any]:
        """
        Calcula estimación de precio basada en la información del vehículo
        """
        categoria_key = self._map_category_to_price_key(vehicle_info.categoria)
        price_info = self.price_ranges["soat_2024"].get(categoria_key, 
                                                       self.price_ranges["soat_2024"]["auto_particular"])
        
        # Ajustes por marca (si aplica)
        precio_base = price_info["promedio"]
        if vehicle_info.marca and vehicle_info.marca.lower() in self.vehicle_database["marcas_populares"]:
            marca_info = self.vehicle_database["marcas_populares"][vehicle_info.marca.lower()]
            if vehicle_info.año:
                año_str = str(vehicle_info.año)
                if año_str in marca_info["precio_soat_promedio"]:
                    precio_base = marca_info["precio_soat_promedio"][año_str]
        
        # Ajustes por uso
        if vehicle_info.uso == "comercial":
            precio_base *= 1.8  # SOAT comercial es más caro
        
        return {
            "precio_estimado": precio_base,
            "rango_min": price_info["min"],
            "rango_max": price_info["max"],
            "categoria": categoria_key,
            "ajustes_aplicados": {
                "marca": vehicle_info.marca if vehicle_info.marca else None,
                "uso_comercial": vehicle_info.uso == "comercial",
                "año": vehicle_info.año
            }
        }
    
    def _map_category_to_price_key(self, categoria: VehicleCategory) -> str:
        """Mapea categoría de vehículo a clave de precio"""
        mapping = {
            VehicleCategory.AUTO_PARTICULAR: "auto_particular",
            VehicleCategory.TAXI: "taxi", 
            VehicleCategory.MOTOCICLETA: "moto_hasta_250cc",
            VehicleCategory.CAMIONETA: "camioneta",
            VehicleCategory.SUV: "camioneta"
        }
        return mapping.get(categoria, "auto_particular")
    
    def detect_customer_profile(self, conversation_history: List[str], 
                              vehicle_info: VehicleInfo) -> CustomerProfile:
        """
        Detecta el perfil del cliente basado en la conversación y vehículo
        """
        conversation_text = " ".join(conversation_history).lower()
        
        # Indicadores de diferentes perfiles
        if any(phrase in conversation_text for phrase in 
               ["primera vez", "no sé", "nunca he", "ayuda", "no entiendo"]):
            return CustomerProfile.FIRST_TIME_BUYER
        
        if any(phrase in conversation_text for phrase in 
               ["tengo varios", "flota", "empresa", "múltiples vehículos"]):
            return CustomerProfile.FLEET_OWNER
        
        if any(phrase in conversation_text for phrase in 
               ["joven", "estudiante", "universidad", "económico", "barato"]):
            return CustomerProfile.YOUNG_DRIVER
        
        if any(phrase in conversation_text for phrase in 
               ["rápido", "ya sé", "como siempre", "renovar"]):
            return CustomerProfile.EXPERIENCED_DRIVER
        
        # Por defecto, basarse en el vehículo
        if vehicle_info.categoria == VehicleCategory.TAXI:
            return CustomerProfile.BUSINESS_OWNER
        
        return CustomerProfile.EXPERIENCED_DRIVER
    
    def generate_personalized_recommendation(self, 
                                           vehicle_info: VehicleInfo,
                                           customer_profile: CustomerProfile,
                                           price_estimate: Dict[str, Any]) -> str:
        """
        Genera recomendación personalizada basada en contexto completo
        """
        persona_info = self.customer_personas[customer_profile]
        
        recommendation = f"""
**RECOMENDACIÓN PERSONALIZADA PARA TU {vehicle_info.categoria.value.upper().replace('_', ' ')}**

🚗 **Tu Vehículo:** {vehicle_info.marca or 'Vehículo'} {vehicle_info.modelo or ''} {vehicle_info.año or ''}

💰 **Precio SOAT 2024:** S/ {price_estimate['precio_estimado']:.0f}
   (Rango: S/ {price_estimate['rango_min']:.0f} - S/ {price_estimate['rango_max']:.0f})

🎯 **Perfil Detectado:** {customer_profile.value.replace('_', ' ').title()}

📋 **Recomendaciones Específicas:**
{persona_info['recommendations']}

✅ **Cobertura SOAT 2024:**
- Lesiones y muerte: S/ 16,800 (4 UIT)
- Incapacidad permanente: S/ 4,200 (1 UIT)  
- Gastos médicos: S/ 21,000 (5 UIT)
- Gastos de sepelio: S/ 2,100

🔥 **Beneficios Autofondo Alese:**
- Emisión inmediata 24/7
- Pago online seguro
- Descargable al instante
- Soporte especializado

¿Te gustaría proceder con la cotización formal?
        """
        
        return recommendation.strip()
    
    def get_contextual_prompts(self, 
                             vehicle_info: VehicleInfo,
                             customer_profile: CustomerProfile) -> str:
        """
        Genera prompts contextuales para mejorar las respuestas de Barbara
        """
        persona_info = self.customer_personas[customer_profile]
        
        context = f"""
CONTEXTO AUTOMOTRIZ ESPECIALIZADO:

🚗 VEHÍCULO DEL CLIENTE:
- Categoría: {vehicle_info.categoria.value}
- Marca: {vehicle_info.marca or 'No especificada'}
- Modelo: {vehicle_info.modelo or 'No especificado'}
- Año: {vehicle_info.año or 'No especificado'}
- Uso: {vehicle_info.uso or 'particular'}

👤 PERFIL CLIENTE: {customer_profile.value.upper()}
- Características: {persona_info['caracteristicas']}
- Approach recomendado: {persona_info['approach']}
- Preocupaciones típicas: {', '.join(persona_info['concerns'])}

📝 INSTRUCCIONES ESPECÍFICAS:
- Adapta tu lenguaje al perfil del cliente
- Menciona información específica del vehículo cuando sea relevante
- Destaca beneficios que resuenen con sus preocupaciones
- Usa el enfoque comunicacional recomendado
- Sé específica con precios y coberturas

🎯 OBJETIVO: Convertir consulta en cotización exitosa
        """
        
        return context 