type AccountActionsProps = { onOpen: () => void };

export default function AccountActions({ onOpen }: AccountActionsProps) {
  return (
    <div className="account-actions">
      <button className="login-button" type="button" onClick={onOpen}>Se connecter</button>
      <button className="signup-button" type="button" onClick={onOpen}>Créer un compte</button>
    </div>
  );
}
