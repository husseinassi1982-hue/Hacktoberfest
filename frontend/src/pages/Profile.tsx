import { Dispatch, FormEvent, SetStateAction, useState } from 'react';

type ProfileProps = { onNotice: (message: string) => void };
type TagEditorProps = {
  label: string;
  values: string[];
  suggestions: string[];
  placeholder: string;
  onChange: Dispatch<SetStateAction<string[]>>;
};

const assetSuggestions = ['Actions', 'ETF', 'Obligations', 'Fonds', 'Immobilier', 'Liquidités', 'Cryptoactifs'];
const sectorSuggestions = ['Technologie', 'Santé', 'Finance', 'Énergie', 'Industrie', 'Consommation', 'Autre'];

function TagEditor({ label, values, suggestions, placeholder, onChange }: TagEditorProps) {
  const [draft, setDraft] = useState('');
  const addTag = (value: string) => {
    const cleanValue = value.trim();
    if (!cleanValue || values.includes(cleanValue)) return;
    onChange((current) => [...current, cleanValue]);
    setDraft('');
  };
  const removeTag = (value: string) => onChange((current) => current.filter((item) => item !== value));

  return (
    <div className="tag-editor">
      <span className="field-label">{label}</span>
      <div className="tag-list" aria-live="polite">
        {values.map((value) => (
          <span className="profile-tag" key={value}>
            {value}
            <button type="button" aria-label={`Retirer ${value}`} onClick={() => removeTag(value)}>×</button>
          </span>
        ))}
        {values.length === 0 && <span className="tag-empty">Aucune préférence ajoutée</span>}
      </div>
      <div className="tag-input-row">
        <input value={draft} onChange={(event) => setDraft(event.target.value)} onKeyDown={(event) => { if (event.key === 'Enter') { event.preventDefault(); addTag(draft); } }} placeholder={placeholder} />
        <button type="button" className="small-action" onClick={() => addTag(draft)} disabled={!draft.trim()}>Ajouter</button>
      </div>
      <div className="suggestion-list">
        <span>Suggestions</span>
        {suggestions.map((suggestion) => (
          <button type="button" className={values.includes(suggestion) ? 'suggestion selected' : 'suggestion'} aria-pressed={values.includes(suggestion)} key={suggestion} onClick={() => values.includes(suggestion) ? removeTag(suggestion) : addTag(suggestion)}>{suggestion}</button>
        ))}
      </div>
    </div>
  );
}

export default function Profile({ onNotice }: ProfileProps) {
  const [name, setName] = useState('Camille Martin');
  const [residence, setResidence] = useState('');
  const [currency, setCurrency] = useState('CAD');
  const [customCurrency, setCustomCurrency] = useState('');
  const [objective, setObjective] = useState('Faire croître mon capital pour garder davantage de liberté dans 10 ans');
  const [horizonYears, setHorizonYears] = useState('10');
  const [initialCapital, setInitialCapital] = useState('100000');
  const [monthlyContribution, setMonthlyContribution] = useState('600');
  const [risk, setRisk] = useState(62);
  const [maxLoss, setMaxLoss] = useState('20');
  const [assets, setAssets] = useState(['ETF', 'Actions', 'Obligations']);
  const [sectors, setSectors] = useState(['Technologie', 'Santé']);
  const [excludedSectors, setExcludedSectors] = useState<string[]>([]);
  const [bankInstitution, setBankInstitution] = useState('');
  const [bankAccountName, setBankAccountName] = useState('');
  const [bankAccountType, setBankAccountType] = useState('');
  const [bankLastFour, setBankLastFour] = useState('');
  const [bankTransfer, setBankTransfer] = useState('');
  const [advancedOpen, setAdvancedOpen] = useState(false);
  const [experience, setExperience] = useState('');
  const [liquidityNeed, setLiquidityNeed] = useState('');
  const [notes, setNotes] = useState('');

  const save = (event: FormEvent) => {
    event.preventDefault();
    onNotice('Profil sauvegardé localement. Aucune donnée bancaire n’est envoyée ni chiffrée pour le moment.');
  };
  const riskLabel = risk < 35 ? 'Prudent' : risk < 70 ? 'Équilibré' : 'Dynamique';
  const displayCurrency = currency === 'OTHER' ? customCurrency || 'devise choisie' : currency;

  return (
    <div id="main-content" className="page-flow profile-page">
      <section className="profile-intro">
        <div>
          <div className="eyebrow">Profil investisseur · CM-2048</div>
          <h2>Parlez-nous de votre situation, à votre manière.</h2>
          <p>Les suggestions sont des points de départ, pas des limites. Vous pouvez écrire vos propres objectifs, ajouter autant de produits ou de secteurs que nécessaire, et compléter les détails qui comptent pour vous.</p>
        </div>
        <span className="profile-avatar" aria-hidden="true">CM</span>
      </section>

      <form className="profile-form modular-profile-form" onSubmit={save}>
        <div className="form-progress"><div><strong>Profil personnalisé</strong><span>Les champs marqués facultatifs peuvent être complétés plus tard.</span></div><span>Étape 1 sur 1</span></div>

        <section className="form-section">
          <div className="form-section-heading"><div><div className="eyebrow">01 · Situation</div><h3>Qui investit et dans quel contexte ?</h3><p>La devise choisie sera utilisée pour afficher les montants du portefeuille.</p></div><span className="section-meta">Essentiel</span></div>
          <div className="field-grid equal-fields">
            <label><span className="field-label">Nom ou identifiant</span><input value={name} onChange={(event) => setName(event.target.value)} placeholder="Votre nom" required /></label>
            <label><span className="field-label">Résidence fiscale <span className="optional">facultatif</span></span><input value={residence} onChange={(event) => setResidence(event.target.value)} placeholder="Pays ou région" /></label>
            <label><span className="field-label">Devise principale</span><select value={currency} onChange={(event) => setCurrency(event.target.value)}><option value="CAD">Dollar canadien (CAD)</option><option value="USD">Dollar américain (USD)</option><option value="EUR">Euro (EUR)</option><option value="GBP">Livre sterling (GBP)</option><option value="CHF">Franc suisse (CHF)</option><option value="OTHER">Autre devise</option></select></label>
            <label><span className="field-label">Préciser la devise <span className="optional">si nécessaire</span></span><input value={customCurrency} onChange={(event) => setCustomCurrency(event.target.value)} placeholder="Ex. JPY ou franc CFA" disabled={currency !== 'OTHER'} /></label>
          </div>
        </section>

        <section className="form-section">
          <div className="form-section-heading"><div><div className="eyebrow">02 · Projet</div><h3>Qu’aimeriez-vous accomplir ?</h3><p>Un objectif libre est plus utile qu’une catégorie imposée.</p></div><span className="section-meta">Essentiel</span></div>
          <div className="field-stack">
            <label>Votre objectif principal<textarea value={objective} onChange={(event) => setObjective(event.target.value)} rows={2} placeholder="Ex. financer une maison, préparer ma retraite..." required /></label>
            <div className="field-grid three-columns">
              <label>Horizon souhaité <span className="optional">années</span><input type="number" min="0" max="100" value={horizonYears} onChange={(event) => setHorizonYears(event.target.value)} placeholder="10" /></label>
              <label>Capital initial <span className="optional">{displayCurrency}</span><input type="number" min="0" value={initialCapital} onChange={(event) => setInitialCapital(event.target.value)} placeholder="100000" /></label>
              <label>Versement régulier <span className="optional">par mois</span><input type="number" min="0" value={monthlyContribution} onChange={(event) => setMonthlyContribution(event.target.value)} placeholder="600" /></label>
            </div>
          </div>
        </section>

        <section className="form-section">
          <div className="form-section-heading"><div><div className="eyebrow">03 · Risque</div><h3>Quelle baisse pourriez-vous supporter ?</h3><p>Le score est un repère continu, pas un profil prédéfini.</p></div><strong className="risk-value">{risk} · {riskLabel}</strong></div>
          <div className="field-stack"><label htmlFor="risk-range">Tolérance estimée<input id="risk-range" type="range" min="0" max="100" value={risk} onChange={(event) => setRisk(Number(event.target.value))} /></label><div className="range-labels"><span>Préserver</span><span>Équilibrer</span><span>Croître</span></div><label>Perte temporaire maximale acceptable <span className="optional">en pourcentage</span><input type="number" min="0" max="100" value={maxLoss} onChange={(event) => setMaxLoss(event.target.value)} placeholder="20" /></label></div>
        </section>

        <section className="form-section">
          <div className="form-section-heading"><div><div className="eyebrow">04 · Préférences</div><h3>Dans quoi souhaitez-vous investir ?</h3><p>Ajoutez, retirez ou écrivez vos propres catégories.</p></div><span className="section-meta">Modulable</span></div>
          <div className="field-stack"><TagEditor label="Produits autorisés" values={assets} onChange={setAssets} suggestions={assetSuggestions} placeholder="Ajouter un produit ou une classe d’actifs" /><TagEditor label="Secteurs qui vous intéressent" values={sectors} onChange={setSectors} suggestions={sectorSuggestions} placeholder="Ajouter un secteur" /><TagEditor label="Secteurs ou activités à éviter" values={excludedSectors} onChange={setExcludedSectors} suggestions={sectorSuggestions} placeholder="Ajouter une exclusion" /></div>
        </section>

        <section className="form-section sensitive-section">
          <div className="form-section-heading"><div><div className="eyebrow">05 · Informations bancaires</div><h3>Quel compte souhaitez-vous associer ?</h3><p>Ces informations servent uniquement à contextualiser les versements et la liquidité. Ne saisissez pas de mot de passe, code secret ou numéro complet.</p></div><span className="sensitive-label">Sensible · facultatif</span></div>
          <div className="banking-content"><div className="security-note"><span aria-hidden="true">!</span><p>La collecte et le chiffrement sécurisés seront définis avec le backend après validation. Pour l’instant, ces champs restent dans l’état frontend mocké et ne sont pas envoyés.</p></div><div className="field-grid equal-fields">
            <label><span className="field-label">Institution financière</span><input value={bankInstitution} onChange={(event) => setBankInstitution(event.target.value)} placeholder="Ex. Banque ou courtier" /></label>
            <label><span className="field-label">Nom du compte <span className="optional">facultatif</span></span><input value={bankAccountName} onChange={(event) => setBankAccountName(event.target.value)} placeholder="Ex. Compte investissement" /></label>
            <label><span className="field-label">Type de compte</span><select value={bankAccountType} onChange={(event) => setBankAccountType(event.target.value)}><option value="">Sélectionner</option><option>Compte courant</option><option>Compte épargne</option><option>Compte-titres</option><option>CELI / TFSA</option><option>REER / RRSP</option><option>Autre</option></select></label>
            <label><span className="field-label">Quatre derniers chiffres <span className="optional">jamais le numéro complet</span></span><input inputMode="numeric" maxLength={4} value={bankLastFour} onChange={(event) => setBankLastFour(event.target.value.replace(/\D/g, '').slice(0, 4))} placeholder="0000" /></label>
            <label><span className="field-label">Versement automatique mensuel <span className="optional">{displayCurrency}</span></span><input type="number" min="0" value={bankTransfer} onChange={(event) => setBankTransfer(event.target.value)} placeholder="0" /></label>
          </div></div>
        </section>

        <details className="advanced-details" open={advancedOpen} onToggle={(event) => setAdvancedOpen(event.currentTarget.open)}><summary><span><span className="eyebrow">06 · Détails avancés</span><strong>Ce que vous voulez encore nous préciser</strong></span><span aria-hidden="true">{advancedOpen ? '−' : '+'}</span></summary><div className="advanced-content"><div className="field-grid"><label>Votre expérience d’investissement <span className="optional">libre</span><input value={experience} onChange={(event) => setExperience(event.target.value)} placeholder="Ex. Je connais les ETF mais pas les obligations" /></label><label>Besoin de liquidité <span className="optional">libre</span><input value={liquidityNeed} onChange={(event) => setLiquidityNeed(event.target.value)} placeholder="Ex. 10 000 € disponibles sous 12 mois" /></label></div><label>Autres contraintes ou informations utiles <span className="optional">libre</span><textarea value={notes} onChange={(event) => setNotes(event.target.value)} rows={3} placeholder="Fiscalité, convictions, devise, contraintes personnelles..." /></label></div></details>
        <div className="form-actions"><span className="form-save-note">Les préférences restent modifiables à tout moment.</span><button className="primary-action" type="submit">Enregistrer le profil</button></div>
      </form>
    </div>
  );
}
