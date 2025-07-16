// Load environment variables from .env file
require("dotenv").config();

// Load dependencies
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const bodyParser = require("body-parser");

// Create Express app
const app = express();

// 1️⃣ Connect to MongoDB
mongoose
  .connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("✅ MongoDB Connected"))
  .catch((err) => console.error("❌ MongoDB Connection Error:", err));

// 2️⃣ Enable CORS for all routes
app.use(cors());

// 3️⃣ Stripe webhook route (MUST come before bodyParser.json)
app.post(
  "/api/stripe/webhook",
  express.raw({ type: "application/json" }),
  require("./routes/stripeWebhook")
);

// 4️⃣ Parse JSON after Stripe webhook
app.use(bodyParser.json());

// 5️⃣ API routes
app.use("/api/stripe", require("./routes/stripeRoutes"));
app.use("/api/medical-history", require("./routes/medicalHistory"));
app.use("/api", require("./routes/openaiRoutes"));

// 6️⃣ Default root route (optional)
app.get("/", (req, res) => {
  res.send("✅ API Server is running");
});

// 7️⃣ Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
