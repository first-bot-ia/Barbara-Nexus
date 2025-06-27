# 📧 Configuración del Sistema de Email - Barbara

## Descripción General

Barbara ahora puede enviar cotizaciones SOAT por correo electrónico con templates HTML profesionales y funcionalidad completa de gestión de emails.

## 🔧 Configuración Inicial

### 1. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Configuración de Email
SENDER_EMAIL=tu-email@gmail.com
SENDER_PASSWORD=tu-app-password-de-gmail
```

### 2. Configuración de Gmail

Para usar Gmail como servidor SMTP:

1. **Habilitar autenticación de 2 factores** en tu cuenta de Gmail
2. **Generar contraseña de aplicación**:
   - Ve a tu cuenta de Google
   - Seguridad → Autenticación de 2 factores
   - Contraseñas de aplicación
   - Selecciona "Correo" y "Otro"
   - Copia la contraseña generada

3. **Configurar variables**:
   ```env
   SENDER_EMAIL=barbara@autofondoalese.com
   SENDER_PASSWORD=abcd-efgh-ijkl-mnop
   ```

### 3. Instalación de Dependencias

```bash
pip install -r config/requirements.txt
```

## 🎯 Funcionalidades Implementadas

### 1. Envío Automático de Cotizaciones

Barbara detecta automáticamente cuando un cliente solicita envío por email:

```
Cliente: "Envíame la cotización por correo"
Barbara: "¡Perfecto! Para enviarte la cotización, ¿cuál es tu email?"
Cliente: "maria@email.com"  
Barbara: "¡Excelente! Te estoy enviando la cotización a maria@email.com"
```

### 2. Templates Profesionales

Los emails incluyen:
- ✅ Diseño HTML responsivo
- ✅ Branding de Autofondo Alese
- ✅ Detalles completos de la cotización
- ✅ Información de cobertura SOAT
- ✅ Call-to-action para finalizar compra
- ✅ Versión de texto plano alternativa

### 3. Extracción Inteligente de Emails

Barbara puede extraer emails de mensajes como:
- "Mi email es juan@gmail.com"
- "Envía a maria.lopez@empresa.com"
- "juan.perez123@hotmail.com"

## 🔍 Flujo de Conversación Mejorado

### Flujo Completo con Email:

1. **Saludo Inicial**
   ```
   Cliente: "Hola"
   Barbara: "¡Hola! Soy Barbara, asesora digital de Autofondo Alese 👋"
   ```

2. **Captura de Nombre** (ARREGLADO)
   ```
   Cliente: "Mi nombre es Carlos Rodriguez"
   Barbara: "¡Mucho gusto, Carlos! Es un placer atenderte 😊"
   ```

3. **Solicitud de Cotización**
   ```
   Cliente: "Quiero cotizar SOAT"
   Barbara: "¡Perfecto, Carlos! ¿Qué tipo de vehículo tienes?"
   ```

4. **Información de Vehículo**
   ```
   Cliente: "Para mi auto"
   Barbara: "¡Excelente! Voy a generar tu cotización personalizada..."
   ```

5. **Cotización Generada**
   ```
   Barbara: "📋 COTIZACIÓN SOAT 2024
   👤 Cliente: Carlos Rodriguez
   💰 PRECIO FINAL: S/ 165.00
   📧 También puedo enviarte esta cotización por correo electrónico"
   ```

6. **Solicitud de Email**
   ```
   Cliente: "Envíamela por email"
   Barbara: "¡Perfecto! ¿Cuál es tu email?"
   ```

7. **Envío Confirmado**
   ```
   Cliente: "carlos@email.com"
   Barbara: "¡Perfecto! Te estoy enviando la cotización a carlos@email.com"
   ```

## 🚀 Mejoras Implementadas

### ✅ Problemas Resueltos:

1. **Extracción de Nombres**: Ahora funciona correctamente con patrones regex mejorados
2. **Flujo Lógico**: Orden de operaciones corregido para captura de nombres
3. **Memoria Conversacional**: Sistema de etapas optimizado sin redundancias
4. **Envío de Email**: Sistema completo con templates profesionales

### ✅ Nuevas Funcionalidades:

1. **Gestión de Email**: Captura, validación y envío automático
2. **Templates HTML**: Emails profesionales con diseño responsive
3. **Validación de Datos**: Verificación de emails y nombres
4. **Logs Detallados**: Seguimiento completo del flujo de email

## 🧪 Pruebas del Sistema

### Ejecutar Pruebas:

```bash
python tests/test_email_integration.py
```

### Verificar Funcionalidad:

1. **Extracción de nombres**
2. **Flujo conversacional completo**
3. **Configuración de email**
4. **Generación de templates**

## 📞 Soporte y Contacto

Para configuración adicional o problemas:
- 📧 info@autofondoalese.com
- 📞 +51 999 888 777

## 🔒 Seguridad

- ✅ Credenciales de email en variables de entorno
- ✅ Conexión SMTP segura con TLS
- ✅ Validación de emails antes del envío
- ✅ Logs de auditoría para envíos

---

**Barbara v2.0** - Sistema de Email Implementado ✨ 