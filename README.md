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


