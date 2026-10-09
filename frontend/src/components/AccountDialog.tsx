type AccountDialogProps = { onClose: () => void; onNotice: (message: string) => void };

export default function AccountDialog({ onClose, onNotice }: AccountDialogProps) {
  return (
    <div className="login-overlay" role="presentation" onMouseDown={(event) => { if (event.currentTarget === event.target) onClose(); }}>
      <section className="login-dialog" role="dialog" aria-modal="true" aria-labelledby="login-heading">
        <button className="dialog-close" type="button" aria-label="Fermer" onClick={onClose}>×</button>
        <div className="eyebrow">Espace client</div>
        <h2 id="login-heading">Retrouvez votre espace Northstar.</h2>
        <p>Connectez-vous pour permettre à Gemma d’utiliser votre profil et vos données de portefeuille.</p>
        <label>Adresse e-mail<input type="email" placeholder="vous@exemple.com" /></label>
        <label>Mot de passe<input type="password" placeholder="••••••••" /></label>
        <button className="primary-action login-submit" type="button" onClick={() => { onClose(); onNotice('La connexion sera disponible lorsque le service d’authentification sera branché.'); }}>Continuer</button>
        <span className="login-note">Aucune donnée réelle n’est encore transmise.</span>
      </section>
    </div>
  );
}
