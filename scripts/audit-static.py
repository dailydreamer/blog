#!/usr/bin/env python3
"""Audit all local HTML/CSS references, fragments, XML feeds and JSON post URLs."""
import json,re,sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from xml.etree import ElementTree as ET
root=Path(sys.argv[1] if len(sys.argv)>1 else 'dist').resolve()
errors=[]; checked=0
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.refs=[];self.ids=set();self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for k in ['src','href','poster']:
   if a.get(k): self.refs.append(a[k])
  if a.get('srcset'): self.refs += [v.strip().split()[0] for v in a['srcset'].split(',')]
  if a.get('http-equiv','').lower()=='refresh': self.refs += re.findall(r'url=(.*)',a.get('content',''),re.I)
pages={p:Page(p.read_text()) for p in root.rglob('*.html')}
def check(source,ref):
 global checked
 u=urlsplit(ref)
 if u.scheme and u.scheme not in ['http','https']:return
 if u.netloc and u.netloc!='dailydreamer.me':return
 # Metadata remains canonical in offline copy, but validate against local equivalent.
 p=unquote(u.path); target=(root/p.lstrip('/') if p.startswith('/') else source.parent/p) if p else source
 if target.is_dir():target=target/'index.html'
 target=target.resolve();checked+=1
 if not target.is_file():errors.append(f'{source.relative_to(root)}: missing {ref}');return
 if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{source.relative_to(root)}: missing fragment {ref}')
for p,page in pages.items():
 for ref in page.refs:check(p,ref)
for p in root.rglob('*.css'):
 for ref in re.findall(r'url\([\"\']?([^\)\"\']+)',p.read_text()):check(p,ref)
for name in ['rss.xml','index.xml','sitemap.xml']:
 p=root/name
 try:
  tree=ET.parse(p)
  for el in tree.iter():
   if el.tag.split('}')[-1] in ['loc','link','guid'] and el.text:check(p,el.text)
 except Exception as e:errors.append(str(e))
for name in ['posts.json','index.json']:
 for post in json.loads((root/name).read_text()):check(root/name,post['url'])
print(json.dumps({'root':str(root),'html_pages':len(pages),'references_checked':checked,'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
