import { getPosts, getTags } from "@/lib/content";
import { site } from "@/lib/site";

function escapeXml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export async function GET() {
  const [posts, tags] = await Promise.all([getPosts(), getTags()]);
  const urls = [
    { loc: `${site.url}/`, lastmod: posts[0]?.date.toISOString() },
    ...posts.map((post) => ({
      loc: `${site.url}/posts/${post.slug}/`,
      lastmod: post.date.toISOString(),
    })),
    ...tags.map((tag) => ({
      loc: `${site.url}/tags/${encodeURIComponent(tag.name)}/`,
      lastmod: posts[0]?.date.toISOString(),
    })),
  ];

  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls
  .map(
    (url) => `  <url>
    <loc>${escapeXml(url.loc)}</loc>
    ${url.lastmod ? `<lastmod>${url.lastmod}</lastmod>` : ""}
  </url>`,
  )
  .join("\n")}
</urlset>`,
    {
      headers: {
        "Content-Type": "application/xml; charset=utf-8",
      },
    },
  );
}
