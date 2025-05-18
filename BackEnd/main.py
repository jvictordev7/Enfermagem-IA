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
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Monta o contexto com o histórico
        context = [SYSTEM_PROMPT]
        for msg in historico:
            prefix = "Usuário:" if msg["from"] == "user" else "Assistente:"
            context.append(f"{prefix} {msg['text']}")
        context.append(pergunta)
        response = model.generate_content(context)
        return {"resposta": response.text}
    except Exception as e:
        return {"resposta": f"Erro interno: {str(e)}"}

@app.post("/analisar-imagem/")
async def analisar_imagem(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            return {"resposta": "Apenas imagens (JPG, PNG) são suportadas."}
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([
            SYSTEM_PROMPT,
            "Descreva o que vê nesta imagem de forma clínica.",
            image
        ])
        return {"resposta": response.text}
    except Exception as e:
        return {"resposta": f"Erro interno: {str(e)}"}