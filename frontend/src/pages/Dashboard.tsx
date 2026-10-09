import { useState } from 'react';
import AllocationChart from '../components/AllocationChart';
import MonteCarloChart from '../components/MonteCarloChart';
import PortfolioValue from '../components/PortfolioValue';
import RiskCard from '../components/RiskCard';
import Portfolio from './Portfolio';
import Advisor from './Advisor';
import Profile from './Profile';
import AccountActions from '../components/AccountActions';
import AccountDialog from '../components/AccountDialog';

const navigation = [['⌂', 'Vue d’ensemble'], ['◒', 'Portefeuille'], ['✦', 'Conseiller IA'], ['◎', 'Profil investisseur']];

export default function Dashboard() {
  const [active, setActive] = useState('Vue d’ensemble');
  const [notice, setNotice] = useState('Données de démonstration actives. Les calculs réels seront fournis par FastAPI.');
  const [accountDialogOpen, setAccountDialogOpen] = useState(false);
  const selectNavigation = (label: string) => {
    setActive(label);
    setNotice(label === 'Vue d’ensemble' ? 'Vue d’ensemble sélectionnée.' : `${label} ouvert. Les données affichées sont simulées jusqu’au branchement de FastAPI.`);
  };
  const renderPage = () => {
    if (active === 'Portefeuille') return <Portfolio onNotice={setNotice} />;
    if (active === 'Conseiller IA') return <Advisor onNotice={setNotice} onOpenAccount={() => setAccountDialogOpen(true)} />;
    if (active === 'Profil investisseur') return <Profile onNotice={setNotice} />;
    return <div id="main-content" className="dashboard-flow">
      <section className="portfolio-summary" aria-labelledby="portfolio-heading"><div><div className="label">Valeur totale investie</div><h2 id="portfolio-heading" className="value">124 860,40 €</h2><div className="delta">+18 420,40 € <span>+17,3 % depuis l’origine</span></div></div><PortfolioValue /><div className="summary-metrics"><div><span>Performance annuelle</span><strong>+11,8 %</strong></div><div><span>Liquidités</span><strong>7 492 €</strong></div><div><span>Prochaine revue</span><strong>Dans 14 jours</strong></div></div></section>
      <section className="analysis-section" aria-labelledby="analysis-heading"><div className="section-heading"><div><div className="eyebrow">Projection &amp; scénarios</div><h2 id="analysis-heading">Votre trajectoire dans le temps</h2></div><span className="section-meta">10 000 scénarios · horizon 12 ans</span></div><div className="analysis-layout"><MonteCarloChart /><aside className="decision-rail" aria-label="Repères de décision"><RiskCard /><section className="profile-summary"><div className="profile-summary-heading"><h3>Profil investisseur</h3><span className="mono">CM-2048</span></div><strong>Camille Martin</strong><dl><div><dt>Objectif</dt><dd>Croissance équilibrée</dd></div><div><dt>Horizon</dt><dd>8 à 12 ans</dd></div></dl><button className="profile-link" type="button" onClick={() => selectNavigation('Profil investisseur')}>Modifier le profil <span aria-hidden="true">↗</span></button></section></aside></div></section>
      <section className="allocation-section" aria-labelledby="allocation-heading"><div className="section-heading"><div><div className="eyebrow">Répartition actuelle</div><h2 id="allocation-heading">Où travaille votre capital ?</h2></div><button className="text-action" type="button" onClick={() => setNotice('Le rééquilibrage sera disponible lorsque le moteur quantitatif sera connecté.')}>Simuler un rééquilibrage <span aria-hidden="true">→</span></button></div><AllocationChart /></section>
    </div>;
  };
  return <div className="app-shell">
    <aside className="sidebar"><div className="brand"><span className="brand-mark" /><span className="brand-name">NORTHSTAR</span></div><nav className="nav" aria-label="Navigation principale">{navigation.map(([icon, label]) => <button className={`nav-button ${active === label ? 'active' : ''}`} key={label} aria-current={active === label ? 'page' : undefined} onClick={() => selectNavigation(label)}><span className="nav-icon" aria-hidden="true">{icon}</span><span>{label}</span></button>)}</nav><div className="sidebar-footer"><span className="status-dot" />Données simulées<br />Dernière synchro : aujourd’hui, 09:42</div></aside>
    <main className={`content ${active === 'Conseiller IA' ? 'content-advisor' : ''}`}><a className="skip-link" href="#main-content">Aller au contenu principal</a>{active !== 'Conseiller IA' && <><header className="topbar"><div><div className="eyebrow">Espace patrimonial / {active}</div><h1>{active === 'Vue d’ensemble' ? 'Bonjour Camille.' : active}</h1><p className="subtitle">{active === 'Vue d’ensemble' ? 'Une lecture claire de votre trajectoire, avant votre prochaine décision.' : 'Retrouvez ici les informations et actions liées à cet espace.'}</p></div><div className="topbar-actions"><div className="date-pill">09 OCT. 2026 · MARCHÉS OUVERTS</div><AccountActions onOpen={() => setAccountDialogOpen(true)} /></div></header><p className="system-notice" role="status" aria-live="polite"><span className="status-dot" />{notice}</p></>}{renderPage()}</main>
    {accountDialogOpen && <AccountDialog onClose={() => setAccountDialogOpen(false)} onNotice={setNotice} />}
  </div>;
}
