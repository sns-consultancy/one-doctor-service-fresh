const express = require("express");
const router = express.Router();
const Stripe = require("stripe");
const stripe = Stripe(process.env.STRIPE_SECRET_KEY);
const plans = require("../config/pricing"); // adjust path as needed

router.post("/create-checkout-session", async (req, res) => {
  const { planId, email } = req.body;

  // Find plan in config
  const plan = plans.find((p) => p.id === planId);
  if (!plan || !plan.stripePriceId) {
    return res.status(400).json({ error: "Invalid plan" });
  }

  const session = await stripe.checkout.sessions.create({
    payment_method_types: ["card"],
    mode: "subscription",
    customer_email: email,
    line_items: [
      {
        price: plan.stripePriceId,
        quantity: 1
      }
    ],
    success_url: `${process.env.CLIENT_URL}/pricing?success=true`,
    cancel_url: `${process.env.CLIENT_URL}/pricing?canceled=true`
  });

  res.json({ url: session.url });
});

module.exports = router;
