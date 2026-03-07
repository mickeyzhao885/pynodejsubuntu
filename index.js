const express = require("express");
const path = require("path");

const app = express();

const PORT = process.env.SERVER_PORT || process.env.PORT || 8000;

// 如果在 Cloudflare / Nginx 后
app.set("trust proxy", true);


// 当前目录
const PUBLIC_DIR = __dirname;


// 静态资源
app.use(express.static(PUBLIC_DIR));


// 根路由
app.get("/", (req, res) => {
  res.sendFile(path.join(PUBLIC_DIR, "index.html"));
});


// 健康检查
app.route("/health")
  .get((req, res) => {
    res.json({
      status: "ok",
      time: new Date().toISOString(),
      ip: req.ip
    });
  })
  .head((req, res) => {
    res.status(204).end();
  });


// 启动服务器
const server = app.listen(PORT, () => {
  console.log(`HTTP server running on port: ${PORT}`);
});


// 启动错误
server.on("error", (err) => {
  console.error("Server start error:", err);
  process.exit(1);
});


// 优雅退出
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);

function shutdown() {
  console.log("Shutting down server...");
  server.close(() => {
    console.log("Server closed");
    process.exit(0);
  });
}
