import React, { useState } from 'react';
import { askGemini } from '../services/geminiService'; // Certifique-se de importar!
import '../styles/ChatAssistant.css';
import imagen from '../assets/imagen.png';

const apiUrl = import.meta.env.VITE_API_URL;

function formatBotText(text: string) {
    // ... (seu código formatador permanece igual)
    let html = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
    html = html.replace(/^([A-Za-zÀ-ÿ\s]+:)/gm, '<strong>$1</strong><br>');
    if (/\*\s/.test(text)) {
        html = html.replace(/(\*\s.*?)(?=\*\s|$)/gs, (item) => `<li>${item.replace(/^\*\s/, '')}</li>`);
        html = html.replace(/(<br>\s*){2,}/g, '<br>');
        html = html.replace(/(<li>.*?<\/li>)+/gs, (list) => `<ul>${list}</ul>`);
    }
    if (/^\d+\./m.test(text)) {
        html = html.replace(/(\d+\.\s.*?)(?=\d+\.|$)/gs, (item) => `<li>${item.replace(/^\d+\.\s/, '')}</li>`);
        html = `<ol>${html}</ol>`;
    }
    html = html.replace(/\n{2,}/g, '<br><br>');
    html = html.replace(/\n/g, '<br>');
    html = html.replace(/<\/strong><br>/g, '</strong><br><br>');
    return html;
}

async function enviarImagemParaBackend(file: File) {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(`${apiUrl}/analisar-imagem/`, {
        method: "POST",
        body: formData,
    });
    const data = await response.json();
    return data.resposta;
}

const ChatAssistant: React.FC = () => {
    const [userInput, setUserInput] = useState('');
    const [messages, setMessages] = useState<{ from: 'user' | 'bot', text: string }[]>([]);
    const [loading, setLoading] = useState(false);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setUserInput(event.target.value);
    };

    const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) setSelectedFile(file);
    };

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!userInput.trim() && !selectedFile) return;
        setLoading(true);

        // Se houver arquivo selecionado, envie para o backend Python
        if (selectedFile) {
            setMessages(prev => [...prev, { from: 'user', text: `Arquivo enviado: ${selectedFile.name}` }]);
            try {
                const respostaImagem = await enviarImagemParaBackend(selectedFile);
                setMessages(prev => [...prev, { from: 'bot', text: respostaImagem }]);
            } catch (e) {
                setMessages(prev => [...prev, { from: 'bot', text: 'Erro ao analisar a imagem.' }]);
            }
            setSelectedFile(null);
            setLoading(false);
            return;
        }

        // Envia o histórico junto com a pergunta
        const question = userInput;
        setMessages(prev => [...prev, { from: 'user', text: question }]);
        setUserInput('');
        try {
            const history = messages.map(msg => ({
                from: msg.from,
                text: msg.text
            }));
            // Chama a função do serviço, enviando histórico
            const answer = await askGemini(question, history);
            setMessages(prev => [...prev, { from: 'bot', text: answer }]);
        } catch (e) {
            setMessages(prev => [...prev, { from: 'bot', text: 'Erro ao buscar resposta da IA.' }]);
        }
        setLoading(false);
    };

    return (
        <div className="chat-assistant">
            {/* Imagem acima do chat */}
            <img
                src={imagen}
                alt="Imagem do Chatbot"
                style={{ display: 'block', margin: '0 auto 16px auto', maxWidth: 120 }}
            />

            <div className="chat-messages">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={msg.from === 'user' ? 'chat-question' : 'chat-answer-area'}
                    >
                        {msg.from === 'user' ? (
                            <div>{msg.text}</div>
                        ) : (
                            <div style={{ display: 'flex', alignItems: 'center' }}>
                                <div
                                    className="chat-answer"
                                    dangerouslySetInnerHTML={{ __html: formatBotText(msg.text) }}
                                />
                                <button
                                    className="chat-copy-btn"
                                    onClick={() => navigator.clipboard.writeText(msg.text)}
                                    style={{ marginLeft: 8 }}
                                    title="Copiar resposta"
                                >
                                    Copiar
                                </button>
                            </div>
                        )}
                    </div>
                ))}
                {loading && (
                    <div className="chat-answer-area">
                        <div className="chat-answer">Pensando...</div>
                    </div>
                )}
            </div>

            {/* Preview do arquivo selecionado */}
            {selectedFile && (
                <div className="chat-file-preview" style={{ margin: '12px 0' }}>
                    <b>Arquivo selecionado:</b> {selectedFile.name}
                    {selectedFile.type.startsWith('image/') && (
                        <div>
                            <img
                                src={URL.createObjectURL(selectedFile)}
                                alt="Preview"
                                style={{ maxWidth: 120, marginTop: 8, borderRadius: 8 }}
                            />
                        </div>
                    )}
                    {selectedFile.type === 'application/pdf' && (
                        <div style={{ marginTop: 8 }}>
                            <span role="img" aria-label="PDF">📄</span> PDF selecionado
                        </div>
                    )}
                </div>
            )}

            <form className="chat-input-area" onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={userInput}
                    onChange={handleInputChange}
                    placeholder="Digite sua pergunta..."
                    className="chat-input"
                    disabled={loading}
                />
                <label className="chat-upload-label">
                    📎
                    <input
                        type="file"
                        accept="image/*,application/pdf"
                        capture="environment"
                        onChange={handleFileUpload}
                        className="chat-upload"
                        disabled={loading}
                    />
                </label>
                <button type="submit" className="chat-send-btn" disabled={loading}>
                    Enviar
                </button>
            </form>
        </div>
    );
};

export default ChatAssistant;