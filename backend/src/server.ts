import { createApp } from "./app.js";
import { config } from "./config.js";

createApp().listen(config.BACKEND_PORT, () => {
  console.log(`Backend em http://localhost:${config.BACKEND_PORT}`);
});
