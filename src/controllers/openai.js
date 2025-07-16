const { Configuration, OpenAIApi } = require("openai");
const Usage = require("../models/Usage");

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY
});

const openai = new OpenAIApi(configuration);

const plans = {
  free: { queriesPerDay: 5 },
  premium: { queriesPerDay: 50 },
  pro: { queriesPerDay: 200 }
};

async function rateLimiter(req, res, next) {
  const userId = req.user.id;
  const today = new Date().toISOString().slice(0,10);

  let usage = await Usage.findOne({ userId, date: today });
  if (!usage) {
    usage = await Usage.create({ userId, date: today, count: 0 });
  }

  const plan = plans[req.user.plan] || plans.free;

  if (usage.count >= plan.queriesPerDay) {
    return res.status(403).json({ error: "Daily limit exceeded. Upgrade your plan." });
  }

  usage.count++;
  await usage.save();

  next();
}

async function generateResponse(req, res) {
  const { prompt } = req.body;

  try {
    const completion = await openai.createChatCompletion({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: prompt }
      ]
    });

    res.json({ text: completion.data.choices[0].message.content });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "OpenAI request failed" });
  }
}

module.exports = {
  rateLimiter,
  generateResponse
};
