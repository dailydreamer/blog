# dailydreamer blog

Personal site prototype migrated from Hugo to Astro + Tailwind.

## Astro prototype

Install dependencies.

```sh
npm ci
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
- `/posts/` complete archive and `/posts/[slug]/` post pages
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

## Reproducible migration verification

Use Node 24 (verified with 24.19.0) and the committed lockfile. In restricted
workspaces, use a writable npm cache and disable optional Astro telemetry:

```sh
npm ci --cache /workspace/.npm-cache
ASTRO_TELEMETRY_DISABLED=1 npm test
ASTRO_TELEMETRY_DISABLED=1 npm run build
npm run review
```

`npm test` builds the actual site, compares all 24 articles with Hugo commit
`0261cbc94eba661a0374b4eff120ade88456f811`, verifies titles, full Markdown,
dates, keywords and approved tag mapping, checks rendered bodies, archive,
feeds, redirects, CNAME and canonical URLs, then audits every local HTML/CSS
reference and fragment. It requires the repository's Git history.

`npm run review` creates `../blog-review.zip` with the untouched `dist/`, a
complete `offline/` copy, uncommitted source patch and changed-source ZIP.
Open `offline/index.html` directly. The first packaging run downloads pinned
MathJax 3.2.2 for offline formula rendering; later runs reuse its local copy.
Online comments are omitted only in the offline copy. External article links
still require internet. This command never publishes the site.

Historical `/post/2016-03-20-a-new-kind-of-science`, lowercase Hugo article
slug and `/tags/读书/`, `/tags/技术/`, `/tags/项目/` redirect to current pages.
The approved labels remain 一苇书舟 / 格物见微 / 问津行录.
