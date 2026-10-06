import { getPosts } from "@/lib/content";
import { site } from "@/lib/site";

function escapeXml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export async function GET() {
  const posts = await getPosts();
  const items = posts
    .map(
      (post) => `
        <item>
          <title>${escapeXml(post.title)}</title>
          <link>${site.url}/posts/${post.slug}/</link>
          <guid>${site.url}/posts/${post.slug}/</guid>
          <pubDate>${post.date.toUTCString()}</pubDate>
          <description>${escapeXml(post.excerpt)}</description>
        </item>`,
    )
    .join("");

  return new Response(
    `<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
      <channel>
        <title>dailydreamer</title>
        <link>${site.url}</link>
        <description>${escapeXml(site.description)}</description>
        ${items}
      </channel>
    </rss>`,
    {
      headers: {
        "Content-Type": "application/rss+xml; charset=utf-8",
      },
    },
  );
}
