import { defineConfig } from "astro/config";
import { readdirSync } from "node:fs";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  site: "https://dailydreamer.me",
  publicDir: "./static",
  trailingSlash: "always",
  redirects: {
    "/post/2016-03-20-a-new-kind-of-science": "/posts/2016-03-20-a-new-kind-of-science/",
    ...Object.fromEntries(Object.entries({ "读书": "一苇书舟", "技术": "格物见微", "项目": "问津行录" }).map(([old, current]) => [`/tags/${old}/`, `/tags/${current}/`])),
    ...Object.fromEntries(readdirSync("content/posts").filter(file => file.endsWith(".md") && file !== file.toLowerCase()).map(file => [`/posts/${file.slice(0, -3).toLowerCase()}/`, `/posts/${file.slice(0, -3)}/`])),
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
