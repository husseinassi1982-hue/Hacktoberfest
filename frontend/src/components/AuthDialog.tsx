import { FormEvent, useState } from 'react';
import { authenticate, AuthUser } from '../api';

type Props = { onClose: () => void; onNotice: (message: string) => void; onAuthenticated: (user: AuthUser) => void };

export default function AuthDialog({ onClose, onNotice, onAuthenticated }: Props) {
  const [registering, setRegistering] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const submit = (event: FormEvent) => {
    event.preventDefault(); setBusy(true); setError('');
    void authenticate(registering ? '/auth/register' : '/auth/login', email, password)
      .then((user) => { onAuthenticated(user); onClose(); onNotice(`Connecté : ${user.email}`); })
      .catch((reason: Error) => setError(reason.message))
      .finally(() => setBusy(false));
  };
  return <div className="login-overlay" role="presentation" onMouseDown={(event) => { if (event.currentTarget === event.target) onClose(); }}>
    <section className="login-dialog" role="dialog" aria-modal="true" aria-labelledby="auth-heading">
      <button className="dialog-close" type="button" aria-label="Fermer" onClick={onClose}>×</button>
      <div className="eyebrow">Espace client</div>
      <h2 id="auth-heading">{registering ? 'Créer un compte' : 'Se connecter'}</h2>
      <form onSubmit={submit}>
        <label>Adresse e-mail<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required /></label>
        <label>Mot de passe<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} minLength={8} required /></label>
        {error && <p role="alert">{error}</p>}
        <button className="primary-action login-submit" type="submit" disabled={busy}>{busy ? 'En cours…' : 'Continuer'}</button>
      </form>
      <button type="button" className="text-action" onClick={() => setRegistering((value) => !value)}>{registering ? 'Se connecter' : 'Créer un compte'}</button>
    </section>
  </div>;
}
