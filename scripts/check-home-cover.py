#!/usr/bin/env python3
"""Verify the welcome cover fits without clipping text or disabling inner-page scrolling."""
import json,os,subprocess,sys,time
from pathlib import Path
cli=os.environ.get('BROWSER_CLI','agent-browser');base=sys.argv[1];out=Path(sys.argv[2]);out.mkdir(exist_ok=True);checks=[]
def run(*args):
 p=subprocess.run([cli,*args],capture_output=True,text=True,timeout=35)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return p.stdout.strip()
def check(label,expr):
 for _ in range(20):
  if run('eval','Boolean('+expr+')')=='true':checks.append(label);return
  time.sleep(.05)
 raise AssertionError(label)
for w,h in [(390,844),(393,659),(320,568),(375,667),(844,390),(568,320),(320,240),(1440,900)]:
 run('set','viewport',str(w),str(h));run('open',base+'/?cover-qa='+str(time.time_ns()));run('set','media','light','reduced-motion')
 check(f'{w}x{h} fits vertically','document.documentElement.scrollHeight<=innerHeight+1&&document.body.scrollHeight<=innerHeight+1')
 check(f'{w}x{h} fits horizontally','document.documentElement.scrollWidth<=innerWidth')
 check(f'{w}x{h} text fully visible','[...document.querySelectorAll(".home-cover-copy h1,.home-introduction")].every(e=>{let r=e.getBoundingClientRect();return r.top>=0&&r.top+Math.max(r.height,e.scrollHeight)<=innerHeight+1&&r.left>=0&&r.right<=innerWidth+1})')
 check(f'{w}x{h} arrow visible','(()=>{let r=document.querySelector("#sidebar-toggle").getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight&&r.left>=0&&r.right<=innerWidth})()')
 run('eval','scrollTo({top:1000,behavior:"instant"})');check(f'{w}x{h} no page scroll','scrollY<=1')
 run('screenshot',str(out/f'cover-{w}x{h}.png'))
 if w<1024:
  run('click','#sidebar-toggle');check('menu opens '+str((w,h)),'document.querySelector("dialog").open')
  run('scrollintoview','nav[aria-label="文章目录"] a:last-child');check('menu remains scrollable '+str((w,h)),'document.querySelector(".mobile-directory-content").scrollTop>0')
  run('press','Escape');check('menu closes '+str((w,h)),'!document.querySelector("dialog").open&&document.body.style.position!=="fixed"&&scrollY<=1')
# Resize the same loaded document to model changes in available viewport height.
run('set','viewport','390','844');run('open',base+'/?cover-qa='+str(time.time_ns()))
for h in [640,740,844]:
 run('set','viewport','390',str(h));check('dynamic viewport '+str(h),'document.documentElement.scrollHeight<=innerHeight+1&&Math.abs(document.querySelector(".home-cover").getBoundingClientRect().height-innerHeight)<=1')
for path in ['/posts/','/posts/2021-10-24-the-minds-i/']:
 run('set','viewport','390','844');run('open',base+path);run('eval','scrollTo({top:600,behavior:"instant"})');check('inner page scroll '+path,'scrollY>100&&document.documentElement.scrollHeight>innerHeight')
(out/'cover-qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},ensure_ascii=False,indent=2));print('PASS',len(checks),'cover checks')
