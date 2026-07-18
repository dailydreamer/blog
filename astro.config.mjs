import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  site: "https://dailydreamer.me",
  publicDir: "./static",
  vite: {
    plugins: [tailwindcss()],
  },
});
