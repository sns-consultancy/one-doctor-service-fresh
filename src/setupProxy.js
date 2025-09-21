const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function(app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://127.0.0.1:8000",
      changeOrigin: true,
      logLevel: "silent",
      onError: (err, req, res) => {
        // Swallow noisy dev errors (e.g., metrics during reload)
        if (!res.headersSent) {
          res.writeHead(204);
          res.end();
        }
      },
    })
  );
};
