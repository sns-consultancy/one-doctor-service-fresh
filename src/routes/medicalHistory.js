const express = require("express");
const router = express.Router();
const medicalService = require("../Services/medicalRecordService");

// POST /api/medical-history
router.post("/", (req, res) => {
  const { user_id } = req.body;
  if (!user_id) {
    return res.status(400).json({ message: "Missing user_id" });
  }
  const record = medicalService.addRecord(req.body);
  res.json({ success: true, record });
});

// GET all medical histories
router.get("/", (req, res) => {
  const allData = medicalService.getAllRecords();
  res.json({ success: true, data: allData });
});

// GET medical history by userId
router.get("/:userId", (req, res) => {
  const { userId } = req.params;
  const data = medicalService.getRecordsByUser(userId);
  if (!data || data.length === 0) {
    return res.status(404).json({ message: "Not found" });
  }
  res.json({ success: true, data });
});

// Export medical history as PDF
router.get("/:userId/pdf", (req, res) => {
  try {
    const doc = medicalService.exportUserPDF(req.params.userId);
    res.setHeader("Content-Type", "application/pdf");
    doc.pipe(res);
  } catch (err) {
    res.status(500).json({ message: "PDF generation failed" });
  }
});

module.exports = router;
