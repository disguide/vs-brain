import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Static SPA build. `base: "./"` keeps asset paths relative so the built
// `dist/` can be served from any host/sub-path (handy for sharing one URL later).
export default defineConfig({
  plugins: [react()],
  base: "./",
});
