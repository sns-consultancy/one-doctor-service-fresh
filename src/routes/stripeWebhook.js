const express = require("express");
const router = express.Router();
const Stripe = require("stripe");
const stripe = Stripe(process.env.STRIPE_SECRET_KEY);
const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

// Optional User import
let User;
try {
  User = require("../models/User");
} catch (err) {
  console.warn("⚠️ User model not found. Subscription updates will be skipped.");
}

router.post(
  "/webhook",
  express.raw({ type: "application/json" }),
  async (req, res) => {
    const sig = req.headers["stripe-signature"];
    let event;

    try {
      event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
    } catch (err) {
      console.error("❌ Webhook signature verification failed:", err.message);
      return res.status(400).send(`Webhook Error: ${err.message}`);
    }

    if (event.type === "checkout.session.completed") {
      const session = event.data.object;
      const customerEmail = session.customer_email;
      const subscriptionId = session.subscription;

      console.log(`✅ Checkout session completed for ${customerEmail}`);

      if (User) {
        try {
          const user = await User.findOne({ email: customerEmail });
          if (user) {
            user.stripeCustomerId = session.customer;
            user.subscriptionStatus = "active";
            user.subscriptionPlan = session.metadata?.planId || null;
            await user.save();
            console.log(`🔄 Updated subscription info for ${customerEmail}`);
          } else {
            console.warn(`⚠️ No user found for email ${customerEmail}`);
          }
        } catch (dbError) {
          console.error(`❌ Database error: ${dbError}`);
          return res.status(500).send(`Database error: ${dbError}`);
        }
      } else {
        console.log(`ℹ️ Skipping user update because User model is unavailable.`);
      }
    }

    res.json({ received: true });
  }
);

module.exports = router;
