const express = require("express");
const router = express.Router();
const Stripe = require("stripe");
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

// Create Checkout Session
router.post("/create-checkout-session", async (req, res) => {
  const { priceId, userId } = req.body;

  try {
    const session = await stripe.checkout.sessions.create({
      mode: "subscription",
      payment_method_types: ["card"],
      line_items: [
        {
          price: priceId,
          quantity: 1
        }
      ],
      metadata: { userId },
      success_url: `${process.env.CLIENT_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.CLIENT_URL}/pricing`
    });

    res.json({ url: session.url });
  } catch (error) {
    console.error("Stripe error", error);
    res.status(500).json({ error: error.message });
  }
});

// Webhook for subscription events
router.post(
  "/webhook",
  express.raw({ type: "application/json" }),
  (request, response) => {
    const sig = request.headers["stripe-signature"];
    let event;

    try {
      event = stripe.webhooks.constructEvent(
        request.body,
        sig,
        process.env.STRIPE_WEBHOOK_SECRET
      );
    } catch (err) {
      console.error(`Webhook error: ${err.message}`);
      return response.status(400).send(`Webhook Error: ${err.message}`);
    }

    // Handle subscription events
    if (event.type === "checkout.session.completed") {
      const session = event.data.object;
      const userId = session.metadata.userId;

      console.log(`✅ User ${userId} subscribed successfully.`);
      console.log(`Session: ${session.id}`);
      console.log(`Customer: ${session.customer}`);
      console.log(`Subscription: ${session.subscription}`);

      // TODO: Save to your DB:
      // - Mark subscription active
      // - Save customer + subscription IDs
    }

    // Always return 200 so Stripe knows you received it
    response.send();
  }
);

// List recent invoices for a customer
router.get("/invoices/:customerId", async (req, res) => {
  const { customerId } = req.params;
  try {
    const invoices = await stripe.invoices.list({
      customer: customerId,
      limit: 10
    });
    res.json(invoices);
  } catch (error) {
    console.error("Error fetching invoices", error);
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;



