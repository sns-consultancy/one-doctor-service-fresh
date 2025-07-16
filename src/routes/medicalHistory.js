const express = require("express");
const router = express.Router();

// Example: in-memory store (replace with MongoDB later)
let db = {};

// POST /api/medical-history
router.post("/", (req, res) => {
  const { user_id } = req.body;

  if (!user_id) {
    return res.status(400).json({ message: "Missing user_id" });
  }

  // Save/update in-memory
  db[user_id] = req.body;

  console.log("✅ Medical history submitted:", req.body);

  res.json({ success: true, message: "Medical history saved." });
});

// GET all medical histories
router.get("/", (req, res) => {
  const allData = Object.values(db);
  res.json({ success: true, data: allData });
});

// GET medical history by userId
router.get("/:userId", (req, res) => {
  const { userId } = req.params;
  const data = db[userId];

  if (!data) {
    return res.status(404).json({ message: "Not found" });
  }

  res.json({ success: true, data });
});

module.exports = router;
