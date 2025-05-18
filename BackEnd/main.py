import os
from fastapi import FastAPI, File, UploadFile
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
        "https://enfermagem-ia-opus.vercel.app/"  # troque pelo seu domínio real
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = (
    "Você é um(a) enfermeiro(a) experiente e objetivo(a), que responde dúvidas clínicas de forma clara, curta e prática, "
    "sem rodeios e sem explicações genéricas. Responda sempre de forma direta, focando na dúvida apresentada, e só inclua "
    "detalhes essenciais para a prática clínica. Evite respostas longas, listas extensas ou explicações teóricas. "
    "Seja empático(a), técnico(a) e sempre oriente a seguir protocolos locais (COREN, ANVISA). "
    "Se não souber ou se a dúvida for muito ampla, peça para o usuário ser mais específico. "
    "Limite sua resposta a no máximo 5 linhas."
)

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