"""
AGENTE LEGAL INTELIGENTE
=========================
Sistema modular para responder preguntas sobre documentos legales
con enrutamiento inteligente, sistema de fallback y soporte para LLM locales (Ollama,mistral).

Autor: Raul Paramo
Fecha: 2025
"""

import logging
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod
import hashlib
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


# CONFIGURACIÓN Y CONSTANTES


class LegalCategory(Enum):
    CIVIL = "civil"
    PENAL = "penal"
    LABORAL = "laboral"
    COMERCIAL = "comercial"
    CONSTITUCIONAL = "constitucional"
    ADMINISTRATIVO = "administrativo"
    TRIBUTARIO = "tributario"
    DESCONOCIDO = "desconocido"

class DecisionType(Enum):
    CLASSIFICATION = "classification"
    ROUTING = "routing"
    PROCESSING = "processing"
    FALLBACK = "fallback"
    ERROR = "error"

@dataclass
class DecisionLog:
    timestamp: str
    decision_type: DecisionType
    category: LegalCategory
    confidence: float
    reasoning: str
    input_hash: str
    output_preview: str

# RESPONDEDOR MULTIMODELO


class MultiModelResponder:
    def __init__(self, models: List[str], base_url: str = "http://localhost:11434"):
        self.models = models
        self.base_url = base_url

    def ask_model(self, model: str, question: str, context: str = "") -> Tuple[str, str]:
        prompt = f"""Eres un abogado experto en derecho latinoamericano.

Pregunta: {question}

Contexto legal:
{context}

Responde de forma clara y precisa:"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False}
            )
            response.raise_for_status()
            return model, response.json()["response"].strip()
        except Exception as e:
            return model, f"[ERROR usando {model}]: {str(e)}"

    def ask_all(self, question: str, context: str = "") -> Dict[str, str]:
        results = {}
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.ask_model, model, question, context) for model in self.models]
            for future in as_completed(futures):
                model, response = future.result()
                results[model] = response
        return results

# CONFIGURACIÓN DE LOGGING


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('legal_agent.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('LegalAgent')


# DOCUMENTOS LEGALES SIMULADOS


LEGAL_DOCUMENTS = {
    "codigo_civil": {
        "title": "Código Civil",
        "category": LegalCategory.CIVIL,
        "content": """
        POLÍTICAS INTERNAS - DERECHO CIVIL

        Artículo 1. Toda persona tiene derecho al libre desarrollo de la personalidad.
        Artículo 2. Los derechos civiles son irrenunciables y no pueden ser objeto de transacción.

        CONTRATOS:
        Artículo 100. El contrato es el acuerdo de voluntades para crear, modificar o extinguir obligaciones.
        Artículo 101. Los contratos deben cumplirse de buena fe y producen efectos entre las partes.
        """
    },
    "codigo_penal": {
        "title": "Código Penal",
        "category": LegalCategory.PENAL,
        "content": """
        NORMATIVAS INTERNAS - DERECHO PENAL

        Artículo 1. Nadie puede ser sancionado por un hecho que no esté tipificado como delito.
        Artículo 2. Las penas deben ser proporcionales al delito cometido.

        DELITOS CONTRA LA VIDA:
        Artículo 50. Homicidio: Quien mate a otro será sancionado con 15 a 25 años de prisión.
        Artículo 51. Lesiones: Quien cause lesiones será sancionado según gravedad.
        """
    },
    "codigo_laboral": {
        "title": "Código de Trabajo",
        "category": LegalCategory.LABORAL,
        "content": """
        POLÍTICAS INTERNAS - DERECHO LABORAL

        Artículo 1. El trabajo es un derecho y deber social.
        Artículo 2. Se prohíbe cualquier discriminación laboral.

        CONTRATO DE TRABAJO:
        Artículo 20. Contrato de trabajo es el acuerdo entre empleador y trabajador.
        Artículo 21. Debe contener: identificación, cargo, salario, jornada y lugar de trabajo.
        """
    }
}


# CLASIFICADOR Y ENRUTADOR


class LegalClassifier:
    def classify(self, question: str) -> Tuple[LegalCategory, float, str]:
        q = question.lower()
        if any(term in q for term in ["contrato", "obligación", "política"]):
            return LegalCategory.CIVIL, 0.9, "Palabras clave civiles encontradas"
        elif any(term in q for term in ["delito", "prisión", "sanción"]):
            return LegalCategory.PENAL, 0.92, "Palabras clave penales encontradas"
        elif any(term in q for term in ["trabajo", "empleador", "jornada", "indemnización"]):
            return LegalCategory.LABORAL, 0.95, "Palabras clave laborales encontradas"
        else:
            return LegalCategory.DESCONOCIDO, 0.4, "No se identificaron palabras clave claras"

class LegalRouter:
    def route(self, category: LegalCategory, documents: Dict[str, Dict]) -> str:
        matching_docs = [doc for doc in documents.values() if doc["category"] == category]
        if not matching_docs:
            return "No se encontró un documento correspondiente a esa categoría."
        return "\n\n".join(doc["content"] for doc in matching_docs)


# AGENTE LEGAL PRINCIPAL


class LegalAgent:
    def __init__(self):
        self.logger = setup_logging()
        self.classifier = LegalClassifier()
        self.router = LegalRouter()
        self.documents = LEGAL_DOCUMENTS
        self.decision_history = []
        self.llm = MultiModelResponder(models=["llama3", "mistral"])
        self.logger.info("Agente Legal inicializado correctamente")

    def _log_decision(self, decision_type: DecisionType, category: LegalCategory, confidence: float, reasoning: str, input_hash: str, output_preview: str):
        log = DecisionLog(
            timestamp=datetime.now().isoformat(),
            decision_type=decision_type,
            category=category,
            confidence=confidence,
            reasoning=reasoning,
            input_hash=input_hash,
            output_preview=output_preview
        )
        self.decision_history.append(log)

    def _get_input_hash(self, question: str) -> str:
        return hashlib.md5(question.encode()).hexdigest()

    def _format_response(self, question: str, category: LegalCategory, confidence: float, responses: Dict[str, str]) -> str:
        all_responses = "\n\n".join(f" Modelo: {model}\n{resp}" for model, resp in responses.items())
        return f"""
Pregunta: {question}
Categoría detectada: {category.value}
Confianza: {confidence:.2f}

Respuestas:
{all_responses}
"""

    def _handle_low_confidence(self, question: str, category: LegalCategory, input_hash: str) -> str:
        context = "\n".join(doc["content"] for doc in self.documents.values())
        responses = self.llm.ask_all(question, context)
        preview = next(iter(responses.values()))[:50] if responses else ""
        self._log_decision(
            DecisionType.FALLBACK,
            category,
            0.0,
            "Confianza baja en clasificación, redirigido a múltiples modelos",
            input_hash,
            preview
        )
        return self._format_response(question, LegalCategory.DESCONOCIDO, 0.0, responses)

    def ask(self, question: str) -> str:
        input_hash = self._get_input_hash(question)
        category, confidence, reasoning = self.classifier.classify(question)

        if confidence < 0.5:
            return self._handle_low_confidence(question, category, input_hash)

        context = self.router.route(category, self.documents)
        responses = self.llm.ask_all(question, context)

        preview = next(iter(responses.values()))[:50] if responses else ""
        self._log_decision(
            DecisionType.PROCESSING,
            category,
            confidence,
            reasoning,
            input_hash,
            preview
        )
        return self._format_response(question, category, confidence, responses)


if __name__ == "__main__":
    agente = LegalAgent()
    print("\n" + "="*50)
    print("AGENTE LEGAL INTELIGENTE INICIADO")
    print("==========================================")
    print("Categorías disponibles: POLÍTICAS, CONTRATOS, NORMATIVAS")
    print("Escribe tu consulta. Para salir, escribe 'salir'.")
    print("="*50 + "\n")

    while True:
        try:
            pregunta = input("👉 Haz tu pregunta según la categoría: ").strip()
            if pregunta.lower() in ["salir", "exit", "quit"]:
                print("👋 Gracias por usar el Agente Legal. ¡Hasta luego!")
                break
            if not pregunta:
                print("🤔 Por favor, ingresa una pregunta.")
                continue
            respuesta = agente.ask(pregunta)
            print(respuesta)
        except KeyboardInterrupt:
            print("\n👋 Operación cancelada. Hasta luego.")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
