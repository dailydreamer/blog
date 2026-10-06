#!/usr/bin/env python3
"""Real Chromium QA. Set BROWSER_CLI to an isolated agent-browser wrapper."""
import json,os,subprocess,sys,time
from pathlib import Path
cli=os.environ.get('BROWSER_CLI','agent-browser');base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4180';out=Path(sys.argv[2] if len(sys.argv)>2 else '/tmp/mobile-menu-qa');out.mkdir(parents=True,exist_ok=True)
results=[]
def run(*args):
 p=subprocess.run([cli,*args],capture_output=True,text=True,timeout=35)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return p.stdout.strip()
def js(code):return run('eval',code)
def check(label,expression):
 js('if(!('+expression+')) throw new Error('+json.dumps(label)+'); true')
 results.append(label)
def settle():
 # Back/close is asynchronous; assert the observable state instead of assuming timing.
 for _ in range(30):
  if js('Boolean(!document.querySelector("dialog").open && !history.state?.mobileDirectory)')=='true':return
  time.sleep(.05)
 raise AssertionError('menu history did not settle')
def open_menu():run('click','#sidebar-toggle');check('open and locked','document.querySelector("dialog").open && document.body.style.position==="fixed"')
run('set','viewport','390','844');run('open',base+'/?qa='+str(time.time_ns()));run('open',base+'/posts/2021-10-24-the-minds-i/');run('set','media','light','reduced-motion')
check('no second disclosure','!document.querySelector("details")')
js('scrollTo({top:600,behavior:"instant"})');start=js('scrollY')
for i in range(3):
 open_menu();run('click','#mobile-directory-close');settle();check('scroll and focus restored '+str(i),'scrollY==='+start+' && document.body.style.position!=="fixed" && document.activeElement.id==="sidebar-toggle"')
open_menu();run('press','Escape');settle();check('Escape closes','!document.querySelector("dialog").open')
open_menu();run('back');settle();check('Back closes without navigating','location.pathname.includes("2021-10-24-the-minds-i")')
run('forward');check('Forward restores dismissible modal','document.querySelector("dialog").open');run('press','Escape');settle()
open_menu();run('mouse','move','1','1');run('mouse','down');run('mouse','up');settle();check('backdrop closes','!document.querySelector("dialog").open')
open_menu();check('open focuses close button','document.activeElement.id==="mobile-directory-close"');run('focus','.sidebar-profile-link');run('press','Shift+Tab');check('focus stays inside modal','document.querySelector("dialog").contains(document.activeElement)');run('press','Tab');check('focus wraps to profile link','document.activeElement.classList.contains("sidebar-profile-link")')
for w,h in [(320,568),(568,320),(844,390),(390,844)]:
 run('set','viewport',str(w),str(h));check('fits viewport '+str((w,h)),'(()=>{let r=document.querySelector("dialog").getBoundingClientRect();return r.left>=0&&r.top>=0&&r.right<=innerWidth&&r.bottom<=innerHeight&&document.documentElement.scrollWidth<=innerWidth})()')
 run('scrollintoview','nav[aria-label="文章目录"] a:last-child');check('last article reachable '+str((w,h)),'(()=>{let r=document.querySelector("nav[aria-label=文章目录] a:last-child").getBoundingClientRect(),c=document.querySelector(".mobile-directory-content").getBoundingClientRect();return r.top>=c.top&&r.bottom<=c.bottom})()')
 check('close remains visible','document.querySelector("#mobile-directory-close").getBoundingClientRect().top>=0')
 run('screenshot',str(out/f'menu-{w}x{h}.png'))
run('click','nav[aria-label="文章目录"] a:last-child');check('article click closes and navigates','location.pathname.includes("2015-06-04-a-pragmatic-programmer")&&!document.querySelector("dialog").open&&document.body.style.position!=="fixed"')
open_menu();run('click','nav[aria-label="Tags"] a[href="/posts/"]');check('archive click closes and navigates','location.pathname==="/posts/"&&!document.querySelector("dialog").open')
open_menu();run('set','viewport','1440','1000');settle();check('desktop restores sidebar and unlocks','document.querySelector("#site-sidebar").parentElement===document.body&&document.body.style.position!=="fixed"')
run('click','#sidebar-toggle');check('desktop collapse works','document.body.classList.contains("sidebar-collapsed")');run('click','#sidebar-toggle')
run('set','viewport','390','844');open_menu();run('click','#mobile-directory-close');settle();check('mobile works after desktop switch','!document.querySelector("dialog").open')
(out/'mobile-menu-qa.json').write_text(json.dumps({'checks':results,'passed':len(results)},ensure_ascii=False,indent=2));print('PASS',len(results),'browser checks')
