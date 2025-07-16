// /middleware/auth.js
const jwt = require("jsonwebtoken");

// Example: attaches req.user with id & plan
exports.protect = (req, res, next) => {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) {
    return res.status(401).json({ error: "No token" });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = {
      id: decoded.id,
      plan: decoded.plan || "free" // assume 'free' if none
    };
    next();
  } catch (err) {
    res.status(401).json({ error: "Invalid token" });
  }
};
