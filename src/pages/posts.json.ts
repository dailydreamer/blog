import { getPosts, markdownToPlainText } from "@/lib/content";
import { site } from "@/lib/site";

export async function GET() {
  const posts = await getPosts();

  return Response.json(
    posts.map((post) => ({
      title: post.title,
      date: post.date.toISOString(),
      tags: post.tags,
      keywords: post.keywords,
      url: `${site.url}/posts/${post.slug}/`,
      excerpt: post.excerpt,
      content: markdownToPlainText(post.markdown),
    })),
  );
}
