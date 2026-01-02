import os
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()  # Carrega as variáveis do .env
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

app = FastAPI()

# Model names podem ser sobrescritos via variáveis de ambiente
DEFAULT_TEXT_MODEL = os.getenv("GEMINI_TEXT_MODEL", "gemini-2.5-flash")
DEFAULT_VISION_MODEL = os.getenv("GEMINI_VISION_MODEL", "gemini-2.5-pro")

def _list_models_safe():
    """Tenta listar modelos disponíveis da API (útil para depuração).
    Retorna uma lista simples de dicionários com nome e capacidades quando possível.
    """
    try:
        models = genai.list_models()
        out = []
        # models pode ser um iterável de dicts/objetos — normalize de forma defensiva
        for m in models:
            try:
                name = getattr(m, 'name', None) or (m.get('name') if isinstance(m, dict) else None) or str(m)
            except Exception:
                name = str(m)
            try:
                caps = getattr(m, 'supported_methods', None) or getattr(m, 'capabilities', None) or (m.get('capabilities') if isinstance(m, dict) else [])
            except Exception:
                caps = []
            out.append({"name": name, "capabilities": caps})
        return out
    except Exception as e:
        return {"error": str(e)}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://enfermagem-ia-opus.vercel.app/",
        "https://enfermagem-ia.onrender.com",
        "https://enfermagem-ia.vercel.app" 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = (
    "Você é um(a) enfermeiro(a) experiente, educado(a), cordial e objetivo(a), que responde dúvidas clínicas de forma clara, curta e prática. "
    "Responda sempre de forma respeitosa, gentil e direta, focando na dúvida apresentada, e só inclua detalhes essenciais para a prática clínica. "
    "Evite respostas longas, listas extensas ou explicações teóricas. Seja empático(a), técnico(a) e sempre oriente a seguir protocolos locais (COREN, ANVISA). "
    "Se não souber ou se a dúvida for muito ampla, peça para o usuário ser mais específico. Limite sua resposta a no máximo 5 linhas."
)

@app.post("/perguntar")
async def perguntar(request: Request):
    try:
        data = await request.json()
        pergunta = data.get("pergunta")
        historico = data.get("historico", [])
        if not pergunta:
            return {"resposta": "Pergunta não enviada."}
        # Usa o modelo configurado por variável de ambiente, com fallback ao padrão
        text_model = os.getenv("GEMINI_TEXT_MODEL", DEFAULT_TEXT_MODEL)
        model = genai.GenerativeModel(text_model)
        # Monta o contexto com o histórico
        context = [SYSTEM_PROMPT]
        for msg in historico:
            prefix = "Usuário:" if msg["from"] == "user" else "Assistente:"
            context.append(f"{prefix} {msg['text']}")
        context.append(pergunta)
        response = model.generate_content(context)
        return {"resposta": response.text}
    except Exception as e:
        # Se o erro for de modelo não encontrado, tente listar modelos disponíveis
        err_text = str(e)
        if "not found" in err_text or "not supported" in err_text or "404" in err_text:
            models = _list_models_safe()
            return {"resposta": "Modelo não encontrado ou não suportado. Verifique /models para ver modelos disponíveis.", "erro": err_text, "model_list": models}
        return {"resposta": f"Erro interno: {err_text}"}

@app.post("/analisar-imagem/")
async def analisar_imagem(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            return {"resposta": "Apenas imagens (JPG, PNG) são suportadas."}
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        vision_model = os.getenv("GEMINI_VISION_MODEL", DEFAULT_VISION_MODEL)
        model = genai.GenerativeModel(vision_model)
        response = model.generate_content([
            SYSTEM_PROMPT,
            "Descreva o que vê nesta imagem de forma clínica.",
            image
        ])
        return {"resposta": response.text}
    except Exception as e:
        err_text = str(e)
        if "not found" in err_text or "not supported" in err_text or "404" in err_text:
            models = _list_models_safe()
            return {"resposta": "Modelo de visão não encontrado ou não suportado. Verifique /models para ver modelos disponíveis.", "erro": err_text, "model_list": models}
        return {"resposta": f"Erro interno: {err_text}"}


@app.get("/models")
async def list_models():
    """Retorna a lista de modelos disponíveis (útil para depuração local)."""
    return _list_models_safe()