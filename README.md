# 🩺 Enfermagem IA – Assistente Inteligente para Profissionais da Saúde

<img src="./src/assets/imagen.png" alt="Logo Enfermagem IA" width="120" style="display:block;margin:24px auto;" />

## 🟢 Projeto Online

Acesse a versão online do Enfermagem IA:  
👉 [https://enfermagem-ia.vercel.app/](https://enfermagem-ia.vercel.app/)

## 📌 Sobre o Projeto

O **Enfermagem IA** é um assistente virtual criado para apoiar profissionais e estudantes de enfermagem, fornecendo respostas rápidas, objetivas e técnicas para dúvidas clínicas, interpretação de prescrições, evolução de prontuário, cuidados, diluições e muito mais.  
O projeto nasceu da vivência prática de uma enfermeira, com o objetivo de facilitar o cotidiano na área da saúde, promovendo agilidade, segurança e atualização constante.

---

## ⚙️ Tecnologias Utilizadas

- **Frontend:**  
  - [React](https://react.dev/) + [Vite](https://vitejs.dev/)
  - CSS customizado (Mobile First, Dark Mode)
- **Backend:**  
  - [FastAPI](https://fastapi.tiangolo.com/) (Python)
  - [Google Generative AI SDK (Gemini)](https://ai.google.dev/)
- **Deploy:**  
  - [Vercel](https://vercel.com/) (Frontend)
  - [Render](https://render.com/) ou similar (Backend)
- **Outros:**  
  - [Pillow](https://python-pillow.org/) para manipulação de imagens
  - [dotenv](https://pypi.org/project/python-dotenv/) para variáveis de ambiente

---

## 🎨 Paleta de Cores

As cores principais do projeto estão definidas no CSS:

```css
:root {
    --green-dark: #161F1F;
    --green-light: #0A2D25;
    --gray-dark: #1A1E21;
    --gray-medium: #22262B;
    --gray-light: #2A2F35;
    --white: #ffffff;
}
```

---

## 🗂️ Estrutura de Pastas

```
Enfermagem-IA
├── BackEnd
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── src
│   ├── assets
│   │   ├── imagen.png
│   │   └── (outros arquivos)
│   ├── components
│   │   └── ChatAssistant.tsx
│   ├── styles
│   │   ├── App.css
│   │   └── ChatAssistant.css
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
├── public
│   ├── favicon.png
│   └── index.html
├── .gitignore
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

---

## 💡 Funcionalidades

- **Chat inteligente:** Responde dúvidas clínicas de forma objetiva, curta e prática.
- **Análise de imagens:** Permite enviar fotos de prescrições ou documentos para análise automática.
- **Mobile First:** Interface adaptada para uso em celulares e tablets.
- **Dark Mode:** Visual confortável para ambientes hospitalares.
- **Cópia rápida:** Botão para copiar respostas da IA.
- **Upload de imagens:** Suporte a fotos tiradas na hora ou da galeria.

---

## 🚀 Como Executar o Projeto

### 1. **Clone o repositório:**
```bash
git clone https://github.com/seu_usuario/enfermagem-ia.git
```

### 2. **Frontend (React + Vite)**

```bash
cd Enfermagem-IA
npm install
npm run dev
```
Acesse [http://localhost:3000](http://localhost:3000)

### 3. **Backend (FastAPI)**

```bash
cd BackEnd
pip install -r requirements.txt
# Crie um arquivo .env com sua chave GEMINI_API_KEY
uvicorn main:app --reload
```
A API estará em [http://localhost:8000](http://localhost:8000)

---

## 🌐 Deploy

- **Frontend:**  
  Deploy pelo [Vercel](https://vercel.com/) (conecte seu GitHub e selecione a pasta `src` como root).
- **Backend:**  
  Recomenda-se [Render](https://render.com/) para FastAPI.  
  Lembre-se de configurar as variáveis de ambiente no painel da plataforma.

---


## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📧 Contato

Dúvidas, sugestões ou parcerias?  
Entre em contato pelo e-mail: **seu_email@exemplo.com**

---

> Feito com 💚 por [Seu Nome](https://github.com/seu_usuario)