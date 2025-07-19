# 🤖 Agente Legal Inteligente

Sistema modular desarrollado en Python para responder consultas legales utilizando múltiples Modelos de Lenguaje (LLMs) locales con enrutamiento inteligente, clasificación temática y fallback automático. Compatible con modelos como **LLaMA3**, **Mistral** (a través de [Ollama](https://ollama.com/) Y listo para entrar en fujo automático con Zapier.

---

## ⚙️ Características principales

- 📚 **Clasificación temática** automática (Civil, Penal, Laboral).
- 🧠 **Integración paralela de múltiples LLMs locales** (LLaMA3, Mistral).
- 🧭 **Enrutamiento inteligente** según la categoría legal detectada.
- 🔁 **Sistema de fallback** si la clasificación tiene baja confianza.
- 📄 Simulación de documentos legales (normativas, políticas internas, contratos).
- 🧾 **Historial de decisiones** registradas automáticamente.
- 📡 Preparado para escalar con arquitectura RAG + LangChain (futuro).

---

## 🏗️ Arquitectura General

- Python como lenguaje base.
- `requests`, `concurrent.futures`, `logging`, `dataclasses` para operaciones principales.
- Ollama para servir múltiples LLMs en local.
- Modularidad clara para añadir nuevas categorías, modelos o reglas.

> 💡 Para una implementación en la nube (Fase 2), se propone el uso de Azure + LangChain + LangGraph.

---

## 📦 Estructura del Proyecto
📁 Agente legal
├── agente_legal.py # Código principal del agente
├── README.md # Este archivo

---

## ▶️ Cómo ejecutar el agente legal

### 1. Clonar el repositorio desde github
- git clone https://github.com/RaulParamo/agente-legal-inteligente.git
- cd agente-legal-inteligente  pip install requests
### 2. Tener [Ollama](https://ollama.com) instalado y corriendo:

``bash
- ollama run llama3
- ollama run mistral

### ## 🔁 Integración con Zapier

Este proyecto incluye una API construida con Flask que se conecta con un formulario web mediante **Zapier**.



## 🔁 Flujo de trabajo: Automatización con Zapier y Mistral (Ollama)

Este flujo permite recibir preguntas legales mediante un formulario y obtener respuestas automáticas generadas por IA local (Mistral en Ollama), integradas con herramientas como Google Forms, Gmail o Google Sheets vía **Zapier**.

### 📌 Descripción paso a paso:

1. 📝 **El usuario llena un formulario**
   Un Google Form donde introduce una consulta legal.

2. 🚀 **Zapier detecta una nueva respuesta**
   Zapier se activa mediante el trigger correspondiente (Responder una pregunta de google forms.).

3. 🔗 **Zapier envía un Webhook POST a la API Flask**
   Se envía la pregunta legal al endpoint `POST /responder`.

4. 🤖 **La app Flask reenvía la pregunta al modelo Mistral (Ollama)**
   Ollama genera una respuesta legal basada en el contexto proporcionado.

5. 📬 **La respuesta generada es devuelta a Zapier**
   La API responde con la información legal generada.

6. 📢 **Zapier entrega la respuesta**
  Se notifica la respuesta al usuario por:

   * 📧 Correo electrónico 
 

---

### 📊 Diagrama de flujo:

```text
[📝 Google Form / App / Gmail / etc.]
              ↓
     ⚡ Zapier (Trigger detecta entrada)
              ↓
    🔗 Webhook POST a API Flask (/responder)
              ↓
 🧠 Ollama ejecuta modelo Mistral localmente
              ↓
 🧾 Respuesta legal generada (devuelta a Zapier)
              ↓
 ✉️ Notificación / 📄 Guardado / 📢 Alerta
```


