import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import {parse} from '@iarna/toml';
import {getPosts, getTags, formatPostDate} from '../src/lib/content.ts';
const baseline='0261cbc94eba661a0374b4eff120ade88456f811';
const read=p=>fs.readFileSync(`dist/${p}`,'utf8');
const git=p=>execFileSync('git',['show',`${baseline}:${p}`],{encoding:'utf8'});
const split=s=>{const m=s.match(/^\+\+\+\s*\n([\s\S]*?)\n\+\+\+\s*\n?/);return {data:parse(m[1]),body:s.slice(m[0].length)};};
const norm=s=>s.replace(/\s+/g,' ').trim();
const posts=await getPosts(), tags=await getTags();
const mapping={'读书':'一苇书舟','技术':'格物见微','项目':'问津行录'};
test('all 24 original posts retain complete body, title, date, keywords and approved taxonomy',()=>{
 const old=execFileSync('git',['ls-tree','--name-only',`${baseline}:content/posts`],{encoding:'utf8'}).trim().split('\n').sort();
 assert.equal(posts.length,24); assert.deepEqual(fs.readdirSync('content/posts').sort(),old);
 for(const f of old){const before=split(git(`content/posts/${f}`)),after=split(fs.readFileSync(`content/posts/${f}`,'utf8'));
 assert.equal(after.body,before.body,f); for(const key of ['title','date','keywords'])assert.deepEqual(after.data[key],before.data[key],`${f}:${key}`);
 assert.deepEqual(after.data.tags,before.data.tags.map(t=>mapping[t]??t),f);
 }
});
test('each complete rendered article and every tag membership is reachable from archive',()=>{
 const archive=read('posts/index.html');
 for(const p of posts){assert.ok(archive.includes(`/posts/${p.slug}/`));const html=read(`posts/${p.slug}/index.html`);assert.ok(norm(html).includes(norm(p.html)),p.slug);assert.ok(html.includes(`https://dailydreamer.me/posts/${p.slug}/`));}
 for(const t of tags){const html=read(`tags/${t.name}/index.html`);const main=html.slice(html.indexOf('<main'));for(const p of posts)assert.equal(main.includes(`/posts/${p.slug}/`),p.tags.includes(t.name),p.slug);}
});
test('home uses Hugo title and full level-three introduction; navigation includes archive',()=>{
 assert.equal(fs.readFileSync('content/_index.md','utf8'),git('content/_index.md'));
 const home=read('index.html'); assert.match(home,/<h1>Welcome to Dailydreamer(?:'|&#39;)s Space<\/h1>/);assert.match(home,/<h3>We walk until the path is done, in wind and sand and setting sun\.<\/h3>/);assert.ok(home.includes('href="/posts/"'));assert.ok(home.includes('mobile-directory'));assert.ok(!home.includes('<details'));assert.ok(home.includes('收起文章目录'));
});
test('RSS and JSON feeds contain exactly the same 24 original articles',()=>{
 assert.equal(read('index.xml'),read('rss.xml'));assert.equal(read('index.json'),read('posts.json'));
 const feed=JSON.parse(read('posts.json'));assert.equal(feed.length,24);assert.equal((read('rss.xml').match(/<item>/g)||[]).length,24);
 for(const p of posts){const item=feed.find(i=>i.url.endsWith(`/posts/${p.slug}/`));assert.equal(item.title,p.title);assert.deepEqual(item.tags,p.tags);assert.ok(read('rss.xml').includes(item.url));}
});
test('legacy article, lowercase Hugo slug and original tag paths redirect to existing routes',()=>{
 const routes={'post/2016-03-20-a-new-kind-of-science':'posts/2016-03-20-a-new-kind-of-science',...Object.fromEntries(Object.entries(mapping).map(([a,b])=>[`tags/${a}`,`tags/${b}`]))};
 for(const p of posts)if(p.slug!==p.slug.toLowerCase())routes[`posts/${p.slug.toLowerCase()}`]=`posts/${p.slug}`;
 for(const [old,current] of Object.entries(routes)){const html=decodeURIComponent(read(`${old}/index.html`));assert.ok(html.includes(`/${current}/`));assert.ok(fs.existsSync(`dist/${current}/index.html`));}
});
test('sitemap, CNAME and 404 canonical are valid',()=>{
 const sitemap=read('sitemap.xml');assert.ok(sitemap.includes('https://dailydreamer.me/posts/'));for(const p of posts)assert.ok(sitemap.includes(`/posts/${p.slug}/`));for(const t of tags)assert.ok(sitemap.includes(`/tags/${encodeURIComponent(t.name)}/`));assert.equal(read('CNAME'),fs.readFileSync('static/CNAME','utf8'));assert.match(read('404.html'),/rel="canonical" href="https:\/\/dailydreamer.me\/404.html"/);
});

test('display dates preserve each source calendar day regardless of build timezone',()=>{
 for(const p of posts){const raw=split(fs.readFileSync(`content/posts/${p.slug}.md`,'utf8')).data.date;const day=String(raw).slice(0,10);assert.equal(p.calendarDate,day);const [y,m,d]=day.split('-').map(Number);assert.equal(formatPostDate(p.calendarDate,'long'),`${y}年${m}月${d}日`);assert.ok(read(`posts/${p.slug}/index.html`).includes(`${y}年${m}月${d}日`));}
});

test('article directory sits after metadata and before complete body, with no empty directory',()=>{
 for(const p of posts){const html=read(`posts/${p.slug}/index.html`);const start=html.indexOf('id="article-toc"');const body=html.indexOf('class="content mt-9"');assert.equal(start>=0,p.headings.length>0,p.slug);assert.ok(!html.includes('文章结构'));assert.ok(!html.includes('article-toc-toggle'));if(start>=0){assert.ok(start>html.indexOf('</header>')&&start<body,p.slug);assert.match(html,/<h2[^>]*id="article-toc-title"[^>]*>目录<\/h2>/);}}
});
