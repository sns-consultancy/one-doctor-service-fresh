const mongoose = require("mongoose");

const UserSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  stripeCustomerId: { type: String },
  subscriptionStatus: { type: String },
  // Add fields as needed
});

module.exports = mongoose.model("User", UserSchema);
