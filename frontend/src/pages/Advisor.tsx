import { FormEvent, useState } from 'react';
import AccountActions from '../components/AccountActions';
import { askAdvisor } from '../api';

type AdvisorProps = { onNotice: (message: string) => void; onOpenAccount: () => void };

type Message = {
  role: 'assistant' | 'user';
  content: string;
};

const starterPrompts = ['Quel est le risque principal de mon portefeuille ?', 'Que puis-je améliorer ce mois-ci ?', 'Simuler un rééquilibrage'];

export default function Advisor({ onNotice, onOpenAccount }: AdvisorProps) {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Bonjour Camille. Je peux vous aider à comprendre votre portefeuille, vos risques et les prochaines décisions à envisager.',
    },
  ]);
  const [isSending, setIsSending] = useState(false);

  const send = (event: FormEvent) => {
    event.preventDefault();
    const cleanQuestion = question.trim();
    if (!cleanQuestion || isSending) return;

    setMessages((current) => [...current, { role: 'user', content: cleanQuestion }]);
    setQuestion('');
    setIsSending(true);
    void askAdvisor(cleanQuestion)
      .then((response) => {
        setMessages((current) => [
          ...current,
          { role: 'assistant', content: `${response.message}\n\n${response.disclaimer}` },
        ]);
      })
      .catch((error: Error) => {
        setMessages((current) => [
          ...current,
          {
            role: 'assistant',
            content: `Je ne peux pas joindre le service de conseil pour le moment : ${error.message}`,
          },
        ]);
      })
      .finally(() => {
      setIsSending(false);
      });
  };

  const startConversation = () => {
    setMessages([]);
    setQuestion('');
    onNotice('Nouvelle conversation créée en mode simulation.');
  };

  return (
    <div id="main-content" className="advisor-chat-page">
      <header className="advisor-chat-topbar">
        <button className="advisor-model" type="button" onClick={startConversation} aria-label="Nouvelle conversation avec Gemma">
          <span className="brand-mark advisor-brand-mark" aria-hidden="true" />
          <span>Gemma</span>
          <span className="model-caret" aria-hidden="true">⌄</span>
        </button>
        <div className="advisor-account-actions">
          <span className="advisor-demo-label"><span className="status-dot" />Mode simulation</span>
          <AccountActions onOpen={onOpenAccount} />
        </div>
      </header>

      <div className="advisor-chat-layout">
        <section className="conversation-main" aria-label="Conversation avec Gemma">
          <div className="conversation-scroll">
            {messages.length === 0 ? (
              <div className="chat-welcome">
                <div className="welcome-icon" aria-hidden="true">✦</div>
                <h2>Que voulez-vous éclairer ?</h2>
                <p>Posez une question sur votre patrimoine ou choisissez un point de départ.</p>
              </div>
            ) : (
              <div className="message-list">
                {messages.map((message, index) => (
                  <article className={`full-chat-message ${message.role}`} key={`${message.role}-${index}`}>
                    <div className="message-avatar" aria-hidden="true">{message.role === 'assistant' ? 'N' : 'CM'}</div>
                    <div className="message-copy">
                      <strong>{message.role === 'assistant' ? 'Gemma' : 'Vous'}</strong>
                      <p>{message.content}</p>
                    </div>
                  </article>
                ))}
                {isSending && <div className="full-chat-message assistant"><div className="message-avatar" aria-hidden="true">N</div><div className="message-copy"><strong>Gemma</strong><p className="typing-state"><span />Analyse en cours<span className="typing-dots">...</span></p></div></div>}
              </div>
            )}
          </div>

          <div className="composer-area">
            {messages.length === 1 && <div className="starter-prompts">{starterPrompts.map((prompt) => <button type="button" key={prompt} onClick={() => setQuestion(prompt)}>{prompt}<span aria-hidden="true">↗</span></button>)}</div>}
            <form className="full-chat-form" onSubmit={send}>
              <button className="composer-add" type="button" aria-label="Ajouter une pièce jointe" onClick={() => onNotice('Les pièces jointes seront disponibles avec votre compte.')}>＋</button>
              <label className="sr-only" htmlFor="full-advisor-question">Message à Gemma</label>
              <input id="full-advisor-question" value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Écrivez votre message à Gemma..." />
              <button className="composer-send" type="submit" aria-label="Envoyer le message" disabled={!question.trim() || isSending}>↑</button>
            </form>
            <p className="chat-disclaimer">Gemma peut se tromper. Vérifiez les informations importantes avant de prendre une décision.</p>
          </div>
        </section>
      </div>

    </div>
  );
}
