import React from 'react';
import ChatAssistant from './components/ChatAssistant';
import './styles/App.css';
import logo from './assets/logo.png'; // Use seu ícone de estetoscópio

const App: React.FC = () => {
  return (
    <div className="App">
      <header className="app-header">
        <img src={logo} alt="Logo Enfermagem IA" className="logo-header" />
      </header>
      <main>
        <ChatAssistant />
        <section className="about">
          <h2>Sobre o Projeto</h2>
          <div className="about-card">
            <b>O que é?</b>
            <p>
              Assistente inteligente para profissionais da saúde responderem dúvidas clínicas, evoluções e prescrições.
            </p>
            <b>Inspiração</b>
            <p>
              Criado para ajudar profissionais, inspirado na experiência da minha esposa enfermeira.
            </p>
            <b>Como usar</b>
            <p>
              Faça perguntas baseadas em boas práticas nacionais (COREN, ANVISA) e receba respostas rápidas.
            </p>
            <div className="about-alert">
              O assistente gera respostas baseadas em boas práticas nacionais. Protocolos podem variar por cidade ou instituição.
            </div>
          </div>
        </section>
      </main>
      <footer>
         © {new Date().getFullYear()} Enfermagem IA. Todos os direitos reservados.
      </footer>
    </div>
  );
};

export default App;