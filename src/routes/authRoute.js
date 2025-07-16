// routes/authRoutes.js
const express = require("express");
const router = express.Router();
const bcrypt = require("bcrypt");
const User = require("../models/User");

// Generates a random referral code
function generateReferralCode() {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  let code = "";
  for (let i = 0; i < 6; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return code;
}

router.post("/signup", async (req, res) => {
  try {
    const { email, password, referralCode: signupReferralCode } = req.body;

    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ error: "Email already registered." });
    }

    let referrer = null;
    if (signupReferralCode) {
      referrer = await User.findOne({ referralCode: signupReferralCode });
      if (!referrer) {
        return res.status(400).json({ error: "Invalid referral code." });
      }
    }

    const passwordHash = await bcrypt.hash(password, 10);

    const newUser = new User({
      email,
      passwordHash,
      referralCode: generateReferralCode(),
      referredBy: signupReferralCode || null,
      trialEndsAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
    });
    await newUser.save();

    if (referrer) {
      referrer.trialEndsAt = new Date(
        (referrer.trialEndsAt || new Date()).getTime() + 30 * 24 * 60 * 60 * 1000
      );
      await referrer.save();
    }

    res.json({ message: "Signup successful!" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Server error." });
  }
});

module.exports = router;
