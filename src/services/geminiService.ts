import { GoogleGenerativeAI } from "@google/generative-ai";

const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
const genAI = new GoogleGenerativeAI(apiKey);

const SYSTEM_PROMPT = `
Você é um(a) enfermeiro(a) experiente e objetivo(a), que responde dúvidas clínicas de forma clara, curta e prática, sem rodeios e sem explicações genéricas. 
Responda sempre de forma direta, focando na dúvida apresentada, e só inclua detalhes essenciais para a prática clínica. 
Evite respostas longas, listas extensas ou explicações teóricas. 
Seja empático(a), técnico(a) e sempre oriente a seguir protocolos locais (COREN, ANVISA).
Se não souber ou se a dúvida for muito ampla, peça para o usuário ser mais específico.
Limite sua resposta a no máximo 5 linhas.
`;

export async function askGemini(userPrompt: string, history: {role: 'user' | 'model', text: string}[] = []) {
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

    // Construa o contexto do chat
    const contents = [
      { role: "user", parts: [{ text: SYSTEM_PROMPT }] },
      ...history.map(msg => ({
        role: msg.role,
        parts: [{ text: msg.text }]
      })),
      { role: "user", parts: [{ text: userPrompt }] }
    ];

    const result = await model.generateContent({ contents });
    return result.response.text();
  } catch (error) {
    console.error("Erro Gemini:", error);
    throw error;
  }
}