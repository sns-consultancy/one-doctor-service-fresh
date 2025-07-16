// /controllers/stripe.js
const Stripe = require("stripe");
const stripe = Stripe(process.env.STRIPE_SECRET_KEY);

exports.createCheckoutSession = async (req, res) => {
  const { priceId } = req.body;

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
      customer_email: req.user.email, // Ensure this exists
      subscription_data: {
        trial_period_days: 30
      },
      success_url: `${process.env.DOMAIN}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.DOMAIN}/cancel`
    });

    res.json({ url: session.url });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Stripe session creation failed" });
  }
};

exports.handleWebhook = async (req, res) => {
  const sig = req.headers["stripe-signature"];
  let event;

  try {
    event = stripe.webhooks.constructEvent(
      req.rawBody,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    console.error(err);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  if (event.type === "checkout.session.completed") {
    const session = event.data.object;
    console.log("Subscription completed!", session);

    // Example: Save subscription data to your DB
    // await User.updateOne(
    //   { email: session.customer_email },
    //   {
    //     stripeCustomerId: session.customer,
    //     subscriptionId: session.subscription,
    //     planStatus: "active"
    //   }
    // );
  }

  res.json({ received: true });
};

exports.createCustomerPortalSession = async (req, res) => {
  const { stripeCustomerId } = req.user; // Ensure this is stored and retrieved properly

  const session = await stripe.billingPortal.sessions.create({
    customer: stripeCustomerId,
    return_url: `${process.env.DOMAIN}/account`
  });

  res.json({ url: session.url });
};
