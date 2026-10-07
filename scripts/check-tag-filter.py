#!/usr/bin/env python3
"""Check in-place tag filtering and its interaction with modal history in Chromium."""
import json,os,subprocess,sys,time
from pathlib import Path
cli=os.environ.get('BROWSER_CLI','agent-browser');base=sys.argv[1];out=Path(sys.argv[2]);out.mkdir(exist_ok=True);checks=[]
def run(*args):
 p=subprocess.run([cli,*args],capture_output=True,text=True,timeout=35)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return p.stdout.strip()
def check(label,expr):
 for _ in range(25):
  if run('eval','Boolean('+expr+')')=='true':checks.append(label);return
  time.sleep(.05)
 raise AssertionError(label)
def tag(name):run('click','nav[aria-label="Tags"] [data-filter-tag='+json.dumps(name,ensure_ascii=False)+']')
def counts(n,label):
 check(label,f'document.querySelectorAll("main [data-post-tags]:not([hidden])").length==={n}&&document.querySelectorAll("#site-sidebar [data-post-tags]:not([hidden])").length==={n}&&[...document.querySelectorAll("[data-filter-count]")].every(e=>e.textContent==="{n} 篇文章")')
 check(label+' same document','window.filterSentinel===42&&location.pathname==="/posts/"')
 check(label+' selected','document.querySelectorAll("nav[aria-label=Tags] [aria-current=true]").length===1')
for width,label in [(1440,'desktop'),(390,'mobile')]:
 run('set','viewport',str(width),'844');run('open',base+'/posts/');run('eval','window.filterSentinel=42');counts(24,label+' initial')
 if width<1024:run('click','#sidebar-toggle')
 for name,n in [('一苇书舟',16),('格物见微',3),('问津行录',5),('',24)]:tag(name);counts(n,label+' '+(name or 'all'))
 run('back');counts(5,label+' Back');run('forward');counts(24,label+' Forward')
 tag('格物见微');counts(3,label+' select before article')
 if width<1024:
  check('filter keeps modal open','document.querySelector("dialog").open')
  run('focus','.sidebar-profile-link');run('press','Shift+Tab')
  check('Tab wraps to visible item','document.activeElement.matches("[data-post-tags]:not([hidden])")')
  run('click','#mobile-directory-close');check('close commits filter','!document.querySelector("dialog").open&&!history.state?.mobileDirectory');counts(3,'closed filter')
 run('click','main [data-post-tags]:not([hidden]) a')
 check(label+' article opens','Boolean(document.querySelector(".content"))')
 run('back');counts(3,label+' return from article')
 run('screenshot',str(out/(label+'-filtered.png')))
 if width<1024:
  run('click','#sidebar-toggle');tag('一苇书舟');run('press','Escape');check('Escape closes filtered menu','!document.querySelector("dialog").open&&!history.state?.mobileDirectory');counts(16,'Escape preserves selection')
  run('back');counts(3,'Back after close restores prior selection')
  run('forward');counts(16,'Forward after close restores selection')
  run('click','#sidebar-toggle');tag('问津行录');run('back');counts(16,'Back within modal restores selection')
  run('back');check('Back exits modal','!document.querySelector("dialog").open');counts(16,'Back exits modal with base filter')
# Direct and legacy links remain usable; all reset overrides deep-link default.
run('set','viewport','1440','900');run('open',base+'/tags/技术/');check('legacy redirect','decodeURIComponent(location.pathname)==="/tags/格物见微/"');check('deep link initial','document.querySelectorAll("main [data-post-tags]:not([hidden])").length===3');tag('');check('deep link reset','document.querySelectorAll("main [data-post-tags]:not([hidden])").length===24');run('reload');check('deep link reset survives reload','document.querySelectorAll("main [data-post-tags]:not([hidden])").length===24');run('back');check('deep link Back','document.querySelectorAll("main [data-post-tags]:not([hidden])").length===3')
run('open',base+'/');run('eval','window.filterSentinel=42');tag('一苇书舟');check('cover unchanged','location.pathname==="/"&&window.filterSentinel===42&&Boolean(document.querySelector(".home-cover"))&&document.querySelectorAll("#site-sidebar [data-post-tags]:not([hidden])").length===16')
for w,h in [(320,568),(568,320),(844,390)]:
 run('set','viewport',str(w),str(h));run('click','#sidebar-toggle');tag('问津行录');check('no overflow '+str(w),'document.documentElement.scrollWidth<=innerWidth');check('visible focus '+str(w),'!document.activeElement.closest("[hidden]")');run('screenshot',str(out/f'filtered-menu-{w}.png'));run('click','#mobile-directory-close');check('close '+str(w),'!document.querySelector("dialog").open&&!history.state?.mobileDirectory')
(out/'tag-filter-qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},ensure_ascii=False,indent=2));print('PASS',len(checks),'tag filter checks')
