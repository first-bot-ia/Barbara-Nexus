"""
🧠 ADVANCED NER SERVICE - SPACY
===============================

Named Entity Recognition avanzado para extraer nombres 
de cualquier texto usando spaCy y técnicas de NLP modernas.

Basado en las mejores prácticas de:
- Width.ai NLP techniques
- Kommunicate entity extraction
- spaCy pre-trained models
"""

import spacy
import re
import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ExtractedEntity:
    """Entidad extraída con metadatos"""
    text: str
    label: str
    confidence: float
    start_char: int
    end_char: int

class SpacyNERService:
    """
    Servicio avanzado de Named Entity Recognition
    
    Utiliza spaCy para extraer nombres de personas de cualquier texto,
    incluso cuando no siguen patrones específicos de presentación.
    """
    
    def __init__(self):
        self.nlp = None
        self.fallback_nlp = None
        self._initialize_models()
        
        # Palabras que definitivamente NO son nombres
        self.forbidden_words = {
            'auto', 'moto', 'soat', 'cotizar', 'quiero', 'para', 'precio', 
            'lima', 'peru', 'si', 'no', 'ok', 'gracias', 'taxi', 'carro', 
            'información', 'info', 'ayuda', 'hola', 'buenos', 'días',
            'tardes', 'noches', 'barbara', 'alese', 'autofondo', 'email',
            'correo', 'telefono', 'celular', 'necesito', 'quieres', 'puedes',
            'seguro', 'vehicular', 'completo', 'todo', 'riesgo'
        }
        
        # Nombres comunes para verificación (EXTENDIDA)
        self.common_spanish_names = {
            'carlos', 'ana', 'pedro', 'maria', 'luis', 'jose', 'juan', 'sofia',
            'alejandro', 'alexander', 'rodriguez', 'martinez', 'silva', 'garcia',
            'lopez', 'gonzalez', 'hernandez', 'perez', 'sanchez', 'ramirez',
            'torres', 'flores', 'rivera', 'gomez', 'diaz', 'morales', 'cruz',
            'jimenez', 'vargas', 'castro', 'ortega', 'romero', 'soto', 'contreras',
            # 🔥 AÑADIDOS: Nombres que faltaban
            'jairo', 'jair', 'adrian', 'daniel', 'david', 'miguel', 'diego',
            'fernando', 'ricardo', 'jorge', 'manuel', 'antonio', 'francisco',
            'pablo', 'gabriel', 'rafael', 'ivan', 'santiago', 'nicolas', 'andres',
            'claudia', 'patricia', 'elena', 'cristina', 'alejandra', 'andrea',
            'monica', 'jessica', 'jennifer', 'paola', 'carla', 'martha', 'rosa',
            'gloria', 'beatriz', 'teresa', 'luz', 'carmen', 'mercedes', 'laura'
        }
    
    def _initialize_models(self):
        """Inicializa modelos de spaCy con fallbacks"""
        try:
            # Modelo español preferido
            self.nlp = spacy.load("es_core_news_sm")
            logger.info("✅ Modelo spaCy español cargado: es_core_news_sm")
        except OSError:
            try:
                # Fallback a modelo multilenguaje
                self.nlp = spacy.load("xx_ent_wiki_sm")
                logger.info("⚠️ Usando modelo multilenguaje: xx_ent_wiki_sm")
            except OSError:
                try:
                    # Último fallback: modelo inglés
                    self.nlp = spacy.load("en_core_web_sm")
                    logger.info("⚠️ Usando modelo inglés como fallback: en_core_web_sm")
                except OSError:
                    logger.error("❌ No se pudo cargar ningún modelo de spaCy")
                    self.nlp = None
    
    def extract_person_names(self, text: str) -> List[ExtractedEntity]:
        """
        Extrae nombres de personas usando NER avanzado
        
        Args:
            text: Texto para analizar
            
        Returns:
            Lista de entidades de personas encontradas
        """
        
        if not self.nlp:
            logger.warning("⚠️ spaCy no disponible, usando fallback regex")
            return self._regex_fallback(text)
        
        # Procesar texto con spaCy
        doc = self.nlp(text)
        
        # Extraer entidades de personas
        person_entities = []
        
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'PER']:  # Diferentes modelos usan diferentes labels
                # Validar que es realmente un nombre
                if self._is_valid_person_name(ent.text):
                    entity = ExtractedEntity(
                        text=ent.text.strip(),
                        label=ent.label_,
                        confidence=self._calculate_confidence(ent, text),
                        start_char=ent.start_char,
                        end_char=ent.end_char
                    )
                    person_entities.append(entity)
                    logger.info(f"🎯 NER extrajo nombre: '{ent.text}' (confianza: {entity.confidence:.2f})")
        
        # Si no encuentra nada, usar análisis contextual
        if not person_entities:
            person_entities = self._contextual_analysis(text)
        
        return person_entities
    
    def extract_best_name(self, text: str) -> Optional[str]:
        """
        Extrae el mejor nombre encontrado en el texto
        
        Args:
            text: Texto para analizar
            
        Returns:
            Mejor nombre encontrado o None
        """
        
        logger.info(f"🔍 Analizando texto con NER avanzado: '{text}'")
        
        # Extraer todas las entidades de personas
        entities = self.extract_person_names(text)
        
        if not entities:
            logger.info("❌ NER no encontró nombres válidos")
            return None
        
        # Ordenar por confianza y seleccionar el mejor
        best_entity = max(entities, key=lambda e: e.confidence)
        
        # Capitalizar correctamente
        best_name = self._capitalize_name(best_entity.text)
        
        logger.info(f"🎉 MEJOR NOMBRE EXTRAÍDO: '{best_name}' (confianza: {best_entity.confidence:.2f})")
        return best_name
    
    def _contextual_analysis(self, text: str) -> List[ExtractedEntity]:
        """
        Análisis contextual cuando spaCy no encuentra entidades
        
        Busca patrones de presentación y palabras que parecen nombres
        """
        
        logger.info("🔍 Realizando análisis contextual...")
        
        entities = []
        
        # 1. Patrones de presentación conocidos
        presentation_patterns = [
            r'\bsoy\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+(?:\s+[A-Za-záéíóúÁÉÍÓÚñÑ]+)*)',
            r'\bme\s+llamo\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+(?:\s+[A-Za-záéíóúÁÉÍÓÚñÑ]+)*)',
            r'\bmi\s+nombre\s+es\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+(?:\s+[A-Za-záéíóúÁÉÍÓÚñÑ]+)*)',
        ]
        
        for pattern in presentation_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                name_candidate = match.group(1).strip()
                if self._is_valid_person_name(name_candidate):
                    entity = ExtractedEntity(
                        text=name_candidate,
                        label='PERSON_PATTERN',
                        confidence=0.9,  # Alta confianza para patrones explícitos
                        start_char=match.start(1),
                        end_char=match.end(1)
                    )
                    entities.append(entity)
                    logger.info(f"📝 Patrón de presentación encontrado: '{name_candidate}'")
        
        # 2. Buscar nombres simples (una sola palabra que parece nombre)
        if not entities and len(text.strip().split()) == 1:
            word = text.strip()
            if self._is_valid_person_name(word):
                entity = ExtractedEntity(
                    text=word.title(),
                    label='PERSON_SIMPLE',
                    confidence=0.85,  # Alta confianza para nombres simples válidos
                    start_char=0,
                    end_char=len(word)
                )
                entities.append(entity)
                logger.info(f"📝 Nombre simple encontrado: '{word}'")
        
        # 3. Buscar palabras capitalizadas que parezcan nombres
        if not entities:
            words = text.split()
            for i, word in enumerate(words):
                word_clean = re.sub(r'[^A-Za-záéíóúÁÉÍÓÚñÑ]', '', word)
                if (len(word_clean) >= 2 and 
                    word_clean.lower() in self.common_spanish_names):
                    
                    # Buscar apellido siguiente
                    full_name = word_clean
                    if i + 1 < len(words):
                        next_word = re.sub(r'[^A-Za-záéíóúÁÉÍÓÚñÑ]', '', words[i + 1])
                        if (len(next_word) >= 2 and 
                            next_word.lower() not in self.forbidden_words):
                            full_name = f"{word_clean} {next_word}"
                    
                    entity = ExtractedEntity(
                        text=full_name.title(),
                        label='PERSON_CAPITALIZED',
                        confidence=0.7,  # Confianza media para nombres capitalizados
                        start_char=text.find(word),
                        end_char=text.find(word) + len(full_name)
                    )
                    entities.append(entity)
                    logger.info(f"📝 Nombre capitalizado encontrado: '{full_name}'")
                    break
        
        return entities
    
    def _regex_fallback(self, text: str) -> List[ExtractedEntity]:
        """Fallback usando regex cuando spaCy no está disponible"""
        
        logger.info("🔧 Usando fallback regex...")
        
        entities = []
        
        # Patrones regex básicos
        patterns = [
            r'\bsoy\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+\s+[A-Za-záéíóúÁÉÍÓÚñÑ]+)',
            r'\bme\s+llamo\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+\s+[A-Za-záéíóúÁÉÍÓÚñÑ]+)',
            r'\bmi\s+nombre\s+es\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+\s+[A-Za-záéíóúÁÉÍÓÚñÑ]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name_candidate = match.group(1).strip()
                if self._is_valid_person_name(name_candidate):
                    entity = ExtractedEntity(
                        text=name_candidate,
                        label='PERSON_REGEX',
                        confidence=0.8,
                        start_char=match.start(1),
                        end_char=match.end(1)
                    )
                    entities.append(entity)
                    break
        
        return entities
    
    def _is_valid_person_name(self, name: str) -> bool:
        """
        Validación INTELIGENTE de nombres - Rechaza saludos y frases incorrectas
        """
        
        if not name or len(name.strip()) < 2:
            logger.info(f"❌ NER: Nombre muy corto: '{name}'")
            return False
        
        name_clean = name.strip().lower()
        
        # Debe tener estructura de nombre (solo letras y espacios)
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ\s]+$', name):
            logger.info(f"❌ NER: Caracteres inválidos: '{name}'")
            return False
        
        # 🚨 FILTRO CRÍTICO: Rechazar saludos dirigidos a Barbara
        barbara_greetings = [
            'hola barbara', 'hola', 'buenos días barbara', 'buenas tardes barbara',
            'buenas noches barbara', 'hi barbara', 'hello barbara', 'barbara',
            'buenos días', 'buenas tardes', 'buenas noches', 'buen día'
        ]
        
        if name_clean in barbara_greetings:
            logger.info(f"❌ NER: Saludo a Barbara rechazado: '{name}'")
            return False
        
        # 🚨 FILTRO: Rechazar frases que contienen Barbara
        if 'barbara' in name_clean:
            logger.info(f"❌ NER: Contiene 'barbara': '{name}'")
            return False
        
        # SOLO rechazar si es UNA palabra prohibida EXACTA
        words = name_clean.split()
        if len(words) == 1 and words[0] in self.forbidden_words:
            logger.info(f"❌ NER: Palabra prohibida exacta: '{name}'")
            return False
        
        # ✅ ACEPTAR TODO LO DEMÁS
        logger.info(f"✅ NER: Nombre válido: '{name}'")
        return True
    
    def _calculate_confidence(self, entity, full_text: str) -> float:
        """Calcula confianza basada en contexto"""
        
        base_confidence = 0.8
        
        # Mayor confianza si está en patrón de presentación
        presentation_words = ['soy', 'llamo', 'nombre']
        if any(word in full_text.lower() for word in presentation_words):
            base_confidence += 0.15
        
        # Mayor confianza si es nombre común
        entity_words = entity.text.lower().split()
        if any(word in self.common_spanish_names for word in entity_words):
            base_confidence += 0.1
        
        # Menor confianza si está cerca de palabras técnicas
        technical_words = ['auto', 'moto', 'soat', 'email']
        context_window = full_text.lower()
        if any(word in context_window for word in technical_words):
            base_confidence -= 0.05
        
        return min(1.0, max(0.0, base_confidence))
    
    def _capitalize_name(self, name: str) -> str:
        """Capitaliza nombre correctamente"""
        return ' '.join(word.capitalize() for word in name.split())
    
    def get_service_status(self) -> Dict[str, Any]:
        """Estado del servicio NER"""
        return {
            'service': 'Advanced NER with spaCy',
            'spacy_available': self.nlp is not None,
            'model_loaded': self.nlp.meta['name'] if self.nlp else 'None',
            'fallback_available': True,
            'supported_languages': ['es', 'en', 'multilingual'],
            'entities_supported': ['PERSON', 'PER'],
            'confidence_threshold': 0.5
        } 