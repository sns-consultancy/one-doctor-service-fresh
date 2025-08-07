const PDFDocument = require('pdfkit');

class MedicalRecordService {
  constructor() {
    this.records = [];
  }

  categorizeAge(age) {
    if (age < 1) return 'infant';
    if (age < 3) return 'toddler';
    if (age < 18) return 'young';
    return 'adult';
  }

  addRecord(record) {
    const entry = {
      ...record,
      category: this.categorizeAge(record.age),
      date: new Date().toISOString(),
    };
    this.records.push(entry);
    return entry;
  }

  getAllRecords() {
    return this.records;
  }

  getRecordsByUser(userId) {
    return this.records.filter((r) => r.user_id === userId);
  }

  toJSON() {
    return JSON.stringify(this.records, null, 2);
  }

  exportUserPDF(userId) {
    const doc = new PDFDocument();
    const records = this.getRecordsByUser(userId);
    doc.text(`Medication History for ${userId}`);
    records.forEach((r) => {
      doc.moveDown().text(`${r.date}: ${r.medication || 'N/A'} (${r.category})`);
    });
    doc.end();
    return doc;
  }
}

module.exports = new MedicalRecordService();
