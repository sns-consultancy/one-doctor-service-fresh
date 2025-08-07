import React, { useState } from 'react';
import QRPlaceholder from '../components/QRPlaceholder';

export default function MedicationHistory() {
  const [form, setForm] = useState({ user_id: '', age: '', medication: '' });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitting record', form);
  };

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Medication History</h1>
      <form onSubmit={handleSubmit} className="space-y-2">
        <input
          name="user_id"
          value={form.user_id}
          onChange={handleChange}
          placeholder="User ID"
          className="border p-2 w-full"
        />
        <input
          name="age"
          value={form.age}
          onChange={handleChange}
          placeholder="Age"
          className="border p-2 w-full"
        />
        <input
          name="medication"
          value={form.medication}
          onChange={handleChange}
          placeholder="Medication"
          className="border p-2 w-full"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2">
          Save
        </button>
      </form>
      <div className="mt-4">
        <QRPlaceholder />
      </div>
    </div>
  );
}
