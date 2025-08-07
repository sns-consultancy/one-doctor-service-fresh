import React from 'react';
import MedicationHistory from './pages/MedicationHistory';

export default function App() {
  return (
    <div className="App">
      <nav className="p-4 bg-gray-100">
        <a href="/medication-history" className="text-blue-500">
          Medication History
        </a>
      </nav>
      <MedicationHistory />
    </div>
  );
}
