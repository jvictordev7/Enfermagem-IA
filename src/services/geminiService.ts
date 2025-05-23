const apiUrl = import.meta.env.VITE_API_URL;

export async function askGemini(userPrompt: string, history: { from: 'user' | 'bot', text: string }[] = []) {
  try {
    const response = await fetch(`${apiUrl}/perguntar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pergunta: userPrompt, historico: history }),
    });
    const data = await response.json();
    return data.resposta;
  } catch (error) {
    console.error("Erro ao buscar resposta da IA:", error);
    throw error;
  }
}