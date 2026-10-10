import { AuthUser } from '../api';
type AccountActionsProps = { onOpen: () => void; user?: AuthUser | null; onLogout?: () => void };

export default function AccountActions({ onOpen, user, onLogout }: AccountActionsProps) {
  if (user) return <div className="account-actions"><span className="login-note">{user.email}</span><button className="login-button" type="button" onClick={onLogout}>Se déconnecter</button></div>;
  return (
    <div className="account-actions">
      <button className="login-button" type="button" onClick={onOpen}>Se connecter</button>
      <button className="signup-button" type="button" onClick={onOpen}>Créer un compte</button>
    </div>
  );
}
