// index.js (Node.js backend)

const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const admin = require("firebase-admin");

const admin = require("firebase-admin");
const path = require("path");

const serviceAccount = require(path.resolve(process.env.GOOGLE_APPLICATION_CREDENTIALS));

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://<YOUR_FIREBASE_PROJECT>.firebaseio.com"
});

// Create Express app
const app = express();
const PORT = process.env.PORT || 5000;

// Middlewares
app.use(cors());
app.use(bodyParser.json());

// Sample API Route (test)
app.get("/api/health", (req, res) => {
  res.json({ status: "Backend API is working ✅" });
});

// Example protected route to create Firestore data
app.post("/api/save-data", async (req, res) => {
  try {
    const { collection, docId, data } = req.body;
    await admin.firestore().collection(collection).doc(docId).set(data);
    res.json({ success: true });
  } catch (error) {
    console.error("Error saving data:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Server is running on port ${PORT}`);
});
