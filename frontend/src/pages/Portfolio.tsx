import { useEffect, useMemo, useState } from 'react';
import { getSavedPortfolios, SavedPortfolio } from '../api';

type PortfolioProps = { onNotice: (message: string) => void };
const currency = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' });
const number = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 2 });

function valueOf(item: SavedPortfolio) {
  return item.portfolio.cash + item.portfolio.positions.reduce((total, position) => total + position.quantity * position.price, 0);
}

export default function Portfolio({ onNotice }: PortfolioProps) {
  const [portfolios, setPortfolios] = useState<SavedPortfolio[]>([]);
  const [selectedId, setSelectedId] = useState<number>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const load = () => {
    setLoading(true);
    setError('');
    void getSavedPortfolios().then((response) => {
      setPortfolios(response.portfolios);
      setSelectedId((current) => current && response.portfolios.some((item) => item.id === current) ? current : response.portfolios[0]?.id);
    }).catch((reason: Error) => setError(reason.message.includes('401') ? 'Connectez-vous pour consulter vos portefeuilles.' : `Impossible de charger les portefeuilles : ${reason.message}`)).finally(() => setLoading(false));
  };
  useEffect(load, []);
  const selected = portfolios.find((item) => item.id === selectedId);
  const total = selected ? valueOf(selected) : 0;
  const allocation = useMemo(() => {
    if (!selected || total <= 0) return [];
    const groups = new Map<string, number>();
    selected.portfolio.positions.forEach((position) => groups.set(position.sector, (groups.get(position.sector) ?? 0) + position.quantity * position.price));
    return [...groups.entries()].map(([name, amount]) => ({ name, amount, weight: amount / total * 100 }));
  }, [selected, total]);

  if (loading) return <div id="main-content" className="page-flow"><p className="system-notice">Chargement de vos portefeuilles…</p></div>;
  if (error) return <div id="main-content" className="page-flow"><section className="empty-state"><h2>Portefeuille indisponible</h2><p>{error}</p><button className="primary-action" type="button" onClick={load}>Réessayer</button></section></div>;
  if (!selected) return <div id="main-content" className="page-flow"><section className="empty-state"><h2>Aucun portefeuille enregistré</h2><p>Créez un portefeuille depuis l’espace de gestion pour l’analyser avec l’assistant IA.</p><button className="text-action" type="button" onClick={() => onNotice('Ajoutez d’abord un portefeuille via l’API /portfolio/saved.')}>Comment ajouter un portefeuille ?</button></section></div>;

  return <div id="main-content" className="page-flow">
    <section className="portfolio-page-summary"><div><div className="label">Portefeuille sélectionné</div><div className="value">{selected.name}</div><div className="delta">{currency.format(total)} <span>mis à jour le {new Date(selected.updated_at).toLocaleDateString('fr-FR')}</span></div></div><div className="portfolio-periods" aria-label="Portefeuille"><select value={selected.id} onChange={(event) => setSelectedId(Number(event.target.value))}>{portfolios.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}</select><button type="button" onClick={load}>Actualiser</button></div></section>
    <section className="portfolio-chart-strip"><div className="value-trend"><p>Valeur actuelle</p><strong>{currency.format(total)}</strong><small>{selected.portfolio.positions.length} position(s) · liquidités {currency.format(selected.portfolio.cash)}</small></div><div className="portfolio-health"><span>Source des données</span><strong>Portefeuille persistant</strong><p>Ces valeurs proviennent de votre compte utilisateur.</p></div></section>
    <section className="holdings-section"><div className="section-heading"><div><div className="eyebrow">Positions</div><h2>Composition détaillée</h2></div><button className="text-action" type="button" onClick={() => onNotice('La simulation de rééquilibrage utilise ce portefeuille persistant.')}>Simuler un rééquilibrage →</button></div><div className="holdings-table-wrap"><table className="holdings-table"><thead><tr><th>Position</th><th>Type</th><th>Valeur</th><th>Prix</th><th>Poids</th></tr></thead><tbody>{selected.portfolio.positions.map((position) => { const amount = position.quantity * position.price; return <tr key={`${selected.id}-${position.symbol}`}><th scope="row">{position.symbol}</th><td>{position.asset_type}</td><td>{currency.format(amount)}</td><td>{currency.format(position.price)}</td><td>{number.format(amount / total * 100)} %</td></tr>; })}</tbody></table></div></section>
    <section className="allocation-section portfolio-allocation"><div className="section-heading"><div><div className="eyebrow">Lecture rapide</div><h2>Répartition par secteur</h2></div><span className="section-meta">{allocation.length} catégories</span></div><div className="allocation-list">{allocation.map((item) => <div className="allocation-row" key={item.name}><span>{item.name}</span><span>{number.format(item.weight)} % · {currency.format(item.amount)}</span></div>)}</div></section>
  </div>;
}
