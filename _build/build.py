import json, re, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import C, INTROS, LINKS
SRC="/mnt/user-data/uploads/오늘의교실_백업/"
OUT="/mnt/project-files/edu-archive/"
os.makedirs(OUT+"apps",exist_ok=True)
HOME_BTN = '''
<!-- 오늘의 교실: 홈 버튼 -->
<a href="../index.html" id="oc-home" title="오늘의 교실 홈으로" style="position:fixed;left:12px;bottom:12px;z-index:2147483647;background:#fff;color:#3b2f2a;border:1px solid #e6dccf;border-radius:999px;padding:8px 14px;font:600 13px/1 system-ui,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;text-decoration:none;box-shadow:0 2px 8px rgba(0,0,0,.12)">🏠 오늘의 교실</a>
<style>@media print{#oc-home{display:none!important}}</style>
'''
def fix(html, slug):
    html = html.replace("unpkg.com/lucide@latest","unpkg.com/lucide@0.460.0")
    if slug=="o2-logo-songs":
        names=[]
        for n in re.findall(r'data-original-artist="([^"]+)"',html):
            if n not in names: names.append(n)
        for i,n in enumerate(names,1):
            html=html.replace(n,f"작곡가{i}")
    if "</body>" in html:
        i=html.rfind("</body>"); html=html[:i]+HOME_BTN+html[i:]
    else: html+=HOME_BTN
    return html
items=[]
for src,slug,subj,sub,title,desc,note in C:
    h=open(SRC+src,encoding="utf-8").read()
    open(OUT+f"apps/{slug}.html","w",encoding="utf-8").write(fix(h,slug))
    items.append(dict(slug=slug,subject=subj,sub=sub,title=title,desc=desc,note=note,url=f"apps/{slug}.html"))
intros={}
for src,slug,subj in INTROS:
    h=open(SRC+src,encoding="utf-8").read()
    open(OUT+f"apps/{slug}.html","w",encoding="utf-8").write(fix(h,slug))
    intros[subj]=f"apps/{slug}.html"
links=[dict(title=t,url=u,subject=s,desc=d,external=True) for t,u,s,d in LINKS]
tpl=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"index.tpl.html"),encoding="utf-8").read()
data=json.dumps(dict(items=items,intros=intros,links=links),ensure_ascii=False)
open(OUT+"index.html","w",encoding="utf-8").write(tpl.replace("/*DATA*/null",data))
print(len(items),len(intros),len(links))
