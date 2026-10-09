import { useState } from 'react';
import AllocationChart from '../components/AllocationChart';
import PortfolioValue from '../components/PortfolioValue';
import { allocations } from '../mockData';

type PortfolioProps = { onNotice: (message: string) => void };

const holdings = [
  ['MSCI World ETF', 'ETF · Monde', '38 420 €', '+14,2 %', '31 %'],
  ['Health Innovation', 'Actions · Santé', '26 214 €', '+9,2 %', '21 %'],
  ['Euro Aggregate Bond', 'Obligations', '13 731 €', '+3,8 %', '11 %'],
  ['Clean Energy Fund', 'Fonds · Énergie', '14 983 €', '-2,3 %', '12 %'],
  ['Cash reserve', 'Liquidités', '7 492 €', '0,0 %', '6 %'],
];

export default function Portfolio({ onNotice }: PortfolioProps) {
  const [period, setPeriod] = useState('1 an');
  return <div id="main-content" className="page-flow"><section className="portfolio-page-summary"><div><div className="label">Valeur du portefeuille</div><div className="value">124 860,40 €</div><div className="delta">+11,8 % <span>sur les 12 derniers mois</span></div></div><div className="portfolio-periods" aria-label="Période du graphique">{['1 mois', '1 an', 'Depuis le début'].map((item) => <button className={period === item ? 'selected' : ''} key={item} type="button" onClick={() => setPeriod(item)}>{item}</button>)}</div></section><section className="portfolio-chart-strip"><PortfolioValue /><div className="portfolio-health"><span>État du portefeuille</span><strong>Aligné avec votre profil</strong><p>La volatilité observée reste sous votre seuil de tolérance.</p></div></section><section className="holdings-section"><div className="section-heading"><div><div className="eyebrow">Positions</div><h2>Composition détaillée</h2></div><button className="text-action" type="button" onClick={() => onNotice('La simulation de rééquilibrage utilise actuellement des données mockées.')}>Simuler un rééquilibrage →</button></div><div className="holdings-table-wrap"><table className="holdings-table"><thead><tr><th>Position</th><th>Type</th><th>Valeur</th><th>Performance</th><th>Poids</th></tr></thead><tbody>{holdings.map(([name, type, value, performance, weight]) => <tr key={name}><th scope="row">{name}</th><td>{type}</td><td>{value}</td><td className={performance.startsWith('-') ? 'negative' : 'positive'}>{performance}</td><td>{weight}</td></tr>)}</tbody></table></div></section><section className="allocation-section portfolio-allocation"><div className="section-heading"><div><div className="eyebrow">Lecture rapide</div><h2>Répartition par secteur</h2></div><span className="section-meta">{allocations.length} catégories</span></div><AllocationChart /></section></div>;
}
