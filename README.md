# dailydreamer blog

Personal site prototype migrated from Hugo to Astro + Tailwind.

## Astro prototype

Install dependencies.

```sh
npm install
```

Preview locally.

```sh
npm run dev
```

Build static output into `dist/`.

```sh
npm run build
```

The Astro prototype keeps Hugo content in `content/posts`, reads TOML frontmatter, and emits:

- `/` homepage
- `/posts/[slug]/` post pages
- `/tags/[tag]/` tag archives
- `/rss.xml` and legacy `/index.xml`
- `/posts.json` and legacy `/index.json`
- `/sitemap.xml`

## Legacy Hugo commands

Create a new post.

```sh
hugo new posts/date-post_name.md
```

Preview content at localhost.

```sh
hugo server
```

Generate content to public folder.

```sh
hugo
```
