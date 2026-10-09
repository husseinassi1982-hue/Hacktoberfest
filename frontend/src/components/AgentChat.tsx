import { FormEvent, useState } from 'react';

type AgentChatProps = { onClose: () => void };

export default function AgentChat({ onClose }: AgentChatProps) {
	const [question, setQuestion] = useState('');
	const [reply, setReply] = useState('Votre exposition à la technologie est de 32 %. Elle soutient la croissance, mais dépasse légèrement votre cible de 28 %. Je peux simuler un rééquilibrage vers la santé ou les obligations.');
	const [isSending, setIsSending] = useState(false);
	const send = (event: FormEvent) => {
		event.preventDefault();
		const cleanQuestion = question.trim();
		if (!cleanQuestion || isSending) return;
		setIsSending(true);
		setQuestion('');
		window.setTimeout(() => {
			setReply(`Je prends en compte votre demande « ${cleanQuestion} ». Les données de marché et les simulations seront bientôt appelées via l’API FastAPI.`);
			setIsSending(false);
		}, 650);
	};
	return <aside className="advisor-sidebar" aria-label="Conseiller Gemma"><header className="advisor-header"><div><span className="eyebrow">Conseiller patrimonial</span><h2>Parlez à Gemma</h2></div><button className="dialog-close" type="button" aria-label="Fermer le conseiller" onClick={onClose}>×</button></header><div className="advisor-status"><span className="status-dot" />Disponible en mode simulation</div><div className="chat-message"><div className="avatar" aria-hidden="true">N</div><div className="chat-bubble" aria-live="polite">{isSending ? <span className="typing-state"><span />Analyse en cours<span className="typing-dots">...</span></span> : reply}</div></div><form className="chat-form" onSubmit={send}><label className="sr-only" htmlFor="advisor-question">Votre question</label><input id="advisor-question" value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ex. Dois-je rééquilibrer ?" /><button className="send-button" type="submit" aria-label="Envoyer" disabled={!question.trim() || isSending}>↗</button></form><div className="advisor-prompts"><span>Essayez une question</span><button type="button" onClick={() => setQuestion('Quel est le risque principal de mon portefeuille ?')}>Risque principal</button><button type="button" onClick={() => setQuestion('Que puis-je améliorer ce mois-ci ?')}>Prochaine action</button></div><p className="chat-footnote">Réponse simulée · aucune décision d’investissement n’est exécutée.</p></aside>;
}
