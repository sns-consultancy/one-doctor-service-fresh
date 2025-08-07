// /models/usage.js
const mongoose = require("mongoose");

const usageSchema = new mongoose.Schema({
  userId: String,
  date: String, // 'YYYY-MM-DD'
  count: { type: Number, default: 0 }
});

module.exports = mongoose.model("Usage", usageSchema);
