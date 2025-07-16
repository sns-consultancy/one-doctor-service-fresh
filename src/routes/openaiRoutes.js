const express = require("express");
const router = express.Router();
const { rateLimiter, generateResponse } = require("../controllers/openai");

router.post("/generate", rateLimiter, generateResponse);

module.exports = router;

