import fs from "node:fs/promises";
import path from "node:path";
import { Renderer, marked, type Token, type Tokens } from "marked";
import { parse as parseToml } from "@iarna/toml";

const root = process.cwd();
const postsDir = path.join(root, "content/posts");
const homeFile = path.join(root, "content/_index.md");

export type Post = {
  slug: string;
  title: string;
  date: Date;
  tags: string[];
  keywords: string[];
  markdown: string;
  html: string;
  headings: Heading[];
  wordCount: number;
  readingMinutes: number;
  excerpt: string;
  hasMath: boolean;
};

export type Heading = {
  depth: number;
  text: string;
  slug: string;
};

type Frontmatter = {
  title?: string;
  date?: string | Date;
  tags?: string[];
  keywords?: string[];
};

function parseHugoMarkdown(source: string): { data: Frontmatter; markdown: string } {
  const match = source.match(/^\+\+\+\s*\n([\s\S]*?)\n\+\+\+\s*\n?/);
  if (!match) {
    return { data: {}, markdown: source };
  }

  return {
    data: parseToml(match[1]) as Frontmatter,
    markdown: source.slice(match[0].length),
  };
}

function resolveHugoRef(ref: string): string {
  const [target, anchor] = ref.split("#");
  const slug = path.basename(target, ".md");
  const hash = anchor ? `#${slugify(anchor)}` : "";

  if (target.startsWith("posts/")) {
    return `/posts/${slug}/${hash}`;
  }

  return `/${target.replace(/\.md$/, "")}/${hash}`;
}

function normalizeHugoShortcodes(markdown: string): string {
  return markdown.replace(/\{\{<\s*ref\s+"([^"]+)"\s*>\}\}/g, (_, ref: string) => resolveHugoRef(ref));
}

function normalizeDate(value: string | Date | undefined): Date {
  if (value instanceof Date) return value;
  if (value) return new Date(value);
  return new Date(0);
}

function buildExcerpt(markdown: string): string {
  const paragraph = markdown
    .split(/\n{2,}/)
    .map((part) => part.trim())
    .find((part) => part && !part.startsWith("#") && !part.startsWith("![")) ?? "";

  return paragraph
    .replace(/!\[[^\]]*\]\([^)]+\)/g, "")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/[`*_>#-]/g, "")
    .replace(/\s+/g, " ")
    .slice(0, 150);
}

function slugify(text: string): string {
  return text
    .trim()
    .toLowerCase()
    .replace(/<[^>]*>/g, "")
    .replace(/[^\p{Letter}\p{Number}\s_-]/gu, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

function createSlugger() {
  const counts = new Map<string, number>();

  return (text: string) => {
    const base = slugify(text) || "section";
    const count = counts.get(base) ?? 0;
    counts.set(base, count + 1);
    return count === 0 ? base : `${base}-${count}`;
  };
}

function collectHeadings(tokens: Token[]): Heading[] {
  const slug = createSlugger();

  return tokens
    .filter((token): token is Tokens.Heading => token.type === "heading" && token.depth >= 2 && token.depth <= 3)
    .map((token) => ({
      depth: token.depth,
      text: token.text,
      slug: slug(token.text),
    }));
}

function renderMarkdown(markdown: string): { html: string; headings: Heading[] } {
  const tokens = marked.lexer(markdown);
  const headings = collectHeadings(tokens);
  const slug = createSlugger();
  const renderer = new Renderer();

  renderer.heading = function ({ tokens, depth, text }: Tokens.Heading) {
    const id = slug(text);
    return `<h${depth} id="${id}">${this.parser.parseInline(tokens)}</h${depth}>\n`;
  };

  return {
    html: marked.parser(tokens, { renderer }),
    headings,
  };
}

function countReadableWords(markdown: string): number {
  const text = markdown
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/`[^`]*`/g, " ")
    .replace(/!\[[^\]]*\]\([^)]+\)/g, " ")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/<[^>]+>/g, " ")
    .replace(/[>#*_~\-+=[\]()`]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  const cjkCount = text.match(/[\u3400-\u9fff]/g)?.length ?? 0;
  const latinWordCount = text.replace(/[\u3400-\u9fff]/g, " ").match(/[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*/g)?.length ?? 0;

  return cjkCount + latinWordCount;
}

export function markdownToPlainText(markdown: string): string {
  return markdown
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/`([^`]*)`/g, "$1")
    .replace(/!\[[^\]]*\]\([^)]+\)/g, " ")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/<[^>]+>/g, " ")
    .replace(/[#>*_~\-+=[\]()`]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function hasMath(markdown: string): boolean {
  return /(^|\s)\$\$[\s\S]*?\$\$/.test(markdown) || /\\\\[([]/.test(markdown);
}

async function readPost(file: string): Promise<Post> {
  const source = await fs.readFile(path.join(postsDir, file), "utf8");
  const parsed = parseHugoMarkdown(source);
  const markdown = normalizeHugoShortcodes(parsed.markdown);
  const slug = file.replace(/\.md$/, "");
  const { html, headings } = renderMarkdown(markdown);
  const wordCount = countReadableWords(markdown);

  return {
    slug,
    title: parsed.data.title ?? slug,
    date: normalizeDate(parsed.data.date),
    tags: parsed.data.tags ?? [],
    keywords: parsed.data.keywords ?? [],
    markdown,
    html,
    headings,
    wordCount,
    readingMinutes: Math.max(1, Math.ceil(wordCount / 400)),
    excerpt: buildExcerpt(markdown),
    hasMath: hasMath(markdown),
  };
}

export async function getPosts(): Promise<Post[]> {
  const files = (await fs.readdir(postsDir)).filter((file) => file.endsWith(".md"));
  const posts = await Promise.all(files.map(readPost));

  return posts.sort((a, b) => b.date.getTime() - a.date.getTime());
}

export async function getPost(slug: string): Promise<Post | undefined> {
  const posts = await getPosts();
  return posts.find((post) => post.slug === slug);
}

export async function getTags(): Promise<Array<{ name: string; count: number }>> {
  const counts = new Map<string, number>();
  for (const post of await getPosts()) {
    for (const tag of post.tags) {
      counts.set(tag, (counts.get(tag) ?? 0) + 1);
    }
  }

  return Array.from(counts, ([name, count]) => ({ name, count })).sort(
    (a, b) => b.count - a.count || a.name.localeCompare(b.name, "zh-CN"),
  );
}

export async function getHomeContent(): Promise<{ title: string; html: string }> {
  const source = await fs.readFile(homeFile, "utf8");
  const { data, markdown } = parseHugoMarkdown(source);

  return {
    title: data.title ?? "Welcome to Dailydreamer's Space",
    html: await marked.parse(markdown),
  };
}

export function formatPostDate(date: Date, style: "short" | "long" = "short"): string {
  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: style === "long" ? "long" : "short",
    day: style === "long" ? "numeric" : undefined,
  }).format(date);
}

export function getTagLabel(tag: string): string {
  return tag;
}
