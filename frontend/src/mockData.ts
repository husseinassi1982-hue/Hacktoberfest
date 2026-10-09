export type Allocation = {
  name: string;
  value: number;
  color: string;
  change: number;
};

export const allocations: Allocation[] = [
  { name: 'Technologie', value: 32, color: '#c85b3f', change: 18.4 },
  { name: 'Santé', value: 21, color: '#587b70', change: 9.2 },
  { name: 'Finance', value: 18, color: '#c59b4a', change: 12.6 },
  { name: 'Énergie', value: 12, color: '#7b6a90', change: -2.3 },
  { name: 'Obligations', value: 11, color: '#55708e', change: 3.8 },
  { name: 'Liquidités', value: 6, color: '#b7afa1', change: 0 },
];

export const portfolioHistory = [
  100, 101, 100.5, 103, 102, 106, 108, 107, 110, 109, 113, 115, 114,
  117, 119, 118, 121, 124, 123, 126, 129, 128, 132, 134, 138, 141,
];

export const monteCarlo = {
  percentile10: [100, 99, 98, 96, 94, 93, 91, 90, 88, 87, 86, 85],
  median: [100, 101, 103, 106, 109, 112, 116, 120, 124, 128, 132, 137],
  percentile90: [100, 104, 108, 114, 120, 127, 134, 141, 149, 157, 166, 174],
};

export const profile = {
  name: 'Camille Martin',
  objective: 'Croissance équilibrée',
  horizon: '8 à 12 ans',
  riskScore: 62,
  riskLabel: 'Modéré dynamique',
};
