#!/usr/bin/env python3
"""Package the actual build, offline copy, uncommitted source patch and evidence."""
import hashlib,html,json,os,re,shutil,subprocess,sys,urllib.request,zipfile
from pathlib import Path
from urllib.parse import urlsplit,unquote,quote
repo=Path(__file__).resolve().parents[1]
out=Path(sys.argv[1] if len(sys.argv)>1 else '../blog-review').resolve();out.mkdir(exist_ok=True)
for name in ['dist','offline']:
 target=out/name
 if target.exists():shutil.rmtree(target)
 shutil.copytree(repo/'dist',target)
root=out/'offline'
vendor=root/'vendor';vendor.mkdir(exist_ok=True)
cache=out/'mathjax-tex-svg-3.2.2.js'
if not cache.exists():
 urllib.request.urlretrieve('https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js',cache)
shutil.copy2(cache,vendor/'mathjax.js')
def local_url(value,source):
 u=urlsplit(html.unescape(value))
 if u.netloc and u.netloc!='dailydreamer.me':return value
 if u.scheme and u.scheme not in ['http','https']:return value
 if not u.path:return value
 target=(root/unquote(u.path).lstrip('/')) if u.path.startswith('/') else source.parent/unquote(u.path)
 if target.is_dir():target=target/'index.html'
 if not target.exists():raise ValueError(f'Missing offline target: {value}')
 return quote(os.path.relpath(target,source.parent),safe='/')+('?' + u.query if u.query else '')+('#'+u.fragment if u.fragment else '')
for p in root.rglob('*.html'):
 s=p.read_text()
 # Offline review cannot load network comments. Formula rendering is bundled locally.
 s=re.sub(r'<script\b[^>]*src="https://utteranc\.es/[^"<>]*"[^>]*>.*?</script>','',s,flags=re.S)
 s=s.replace('https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js','/vendor/mathjax.js')
 # Build modules contain only self-contained navigation handlers. Inline as classic
 # scripts for file:// browsers, which otherwise reject module loads across files.
 def script(m):
  tag=m.group(0);src=re.search(r'src="([^"]+)"',tag)
  if 'type="module"' not in tag:return tag
  if src:
   body=(root/unquote(src[1]).lstrip('/')).read_text()
   if re.search(r'\b(?:import|export)\s',body):raise ValueError('Module bundling required')
  else:body=tag[tag.index('>')+1:tag.rindex('</script>')]
  return '<script>(()=>{'+body+'})();</script>'
 s=re.sub(r'<script\b[^>]*>.*?</script>',script,s,flags=re.S)
 # Keep SEO metadata canonical; rewrite navigation and assets only.
 def tag(m):
  t=m.group(0)
  if re.search(r'rel="(?:canonical|alternate)"',t):return t
  t=re.sub(r'(href|src|poster)="([^"]+)"',lambda a:f'{a[1]}="{local_url(a[2],p)}"',t)
  if 'http-equiv="refresh"' in t:t=re.sub(r'(url=)([^"<>]+)',lambda a:a[1]+local_url(a[2],p),t)
  return t
 s=re.sub(r'<[^>]+>',tag,s)
 p.write_text(s)
for p in root.rglob('*.css'):
 s=p.read_text();s=re.sub(r'url\((["\']?)(/[^)"\']+)\1\)',lambda m:'url("'+local_url(m[2],p)+'")',s);p.write_text(s)
patch=subprocess.check_output(['git','diff','--binary','HEAD'],cwd=repo)
files=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=repo).decode().strip('\0').split('\0')
for f in filter(None,files):
 result=subprocess.run(['git','diff','--no-index','--binary','--','/dev/null',f],cwd=repo,capture_output=True)
 if result.returncode not in [0,1]:raise RuntimeError(result.stderr.decode())
 patch+=result.stdout
(out/'source-changes.patch').write_bytes(patch)
with zipfile.ZipFile(out/'source-changes.zip','w',zipfile.ZIP_DEFLATED) as z:
 changed=subprocess.check_output(['git','diff','--name-only','HEAD','-z'],cwd=repo).decode().strip('\0').split('\0')
 for f in sorted(set(filter(None,changed+files))):
  if (repo/f).is_file():z.write(repo/f,f)
(out/'README.txt').write_text('Open offline/index.html directly in your browser. This is the complete built site with 24 articles and assets.\nThe dist/ directory is the unchanged production build. Serve with python3 -m http.server --directory dist.\nOffline copy bundles MathJax and omits online comments. External article links still require internet.\nApply source-changes.patch to fc27104ff450a7dadc045270fc5866084c30c4f3 using git apply. No commit, push or deployment performed.\n')
for name,folder in [('static-audit.json','dist'),('offline-audit.json','offline')]:
 result=subprocess.run([sys.executable,str(repo/'scripts/audit-static.py'),str(out/folder)],capture_output=True,text=True)
 (out/name).write_text(result.stdout)
 if result.returncode:raise RuntimeError(result.stdout+result.stderr)
zip_path=out.with_suffix('.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(out.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(out.parent))
print(json.dumps({'zip':str(zip_path),'bytes':zip_path.stat().st_size,'sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest()},indent=2))
