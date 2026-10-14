#!/usr/bin/env python3
"""Add a video + full-length text overlay to an EMPTY CapCut project by editing its JSON.
Usage: capcut_add_overlay.py <project-name> <video.mp4> "LINE1\nLINE2" [highlight,words]
Needs CapCut closed. Backs up to *.pre-overlay. Set CAPCUT_TEMPLATE_PROJECT to any existing project with
a text segment whose material is in materials.texts (copied for schema fidelity)."""
import json,copy,uuid,shutil,os,sys,subprocess
R=os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft/")
name,vid,txt=sys.argv[1],sys.argv[2],sys.argv[3].replace("\\n","\n")
hl=[w for w in (sys.argv[4].split(",") if len(sys.argv)>4 else []) if w]
P=R+name+"/"; TLID=json.load(open(P+"Timelines/project.json"))["main_timeline_id"]
dur=int(float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",vid]))*1e6)
w,h=map(int,subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height","-of","csv=p=0:s=x",vid]).decode().strip().split("x"))
TPL=os.environ.get("CAPCUT_TEMPLATE_PROJECT") or sys.exit("set CAPCUT_TEMPLATE_PROJECT to a CapCut project name that contains a plain text segment")
T=json.load(open(R+TPL+"/draft_info.json")); out=json.load(open(P+"Timelines/%s/draft_info.json"%TLID))
nid=lambda:str(uuid.uuid4()).upper()
def find(i):
    for k,l in T["materials"].items():
        for m in l:
            if isinstance(m,dict) and m.get("id")==i: return k,m
vt=next(t for t in T["tracks"] if t["type"]=="video"); vs=copy.deepcopy(vt["segments"][0])
tids={m["id"] for m in T["materials"]["texts"]}
tt=next(t for t in T["tracks"] if t["type"]=="text" and any(g["material_id"] in tids for g in t["segments"]))
ts=copy.deepcopy(next(g for g in tt["segments"] if g["material_id"] in tids))
def bring(s):
    m2={}
    for i in [s["material_id"]]+s["extra_material_refs"]:
        k,m=find(i); m=copy.deepcopy(m); m["id"]=m2[i]=nid(); out["materials"][k].append(m)
    s["material_id"]=m2[s["material_id"]]; s["extra_material_refs"]=[m2[i] for i in s["extra_material_refs"]]; s["id"]=nid()
bring(vs); bring(ts)
out["canvas_config"]={"ratio":"original","width":w,"height":h,"background":None}
v=out["materials"]["videos"][-1]; v.update(path=vid,duration=dur,width=w,height=h,material_name=os.path.basename(vid),local_material_id=str(uuid.uuid4()))
vs["source_timerange"]=vs["target_timerange"]={"start":0,"duration":dur}; vs["source_timerange"]=dict(vs["target_timerange"])
ts["target_timerange"]={"start":0,"duration":dur}; ts["clip"]={**ts["clip"],"scale":{"x":1.0,"y":1.0},"transform":{"x":0.0,"y":0.0}}
font="/Applications/CapCut.app/Contents/Resources/Font/SystemFont/en.ttf"
def style(r,c): return {"fill":{"content":{"solid":{"color":c},"render_type":"solid"}},"range":r,"size":19,"bold":True,"useLetterColor":True,
  "strokes":[{"width":0.12,"mode":0,"content":{"solid":{"color":[0,0,0]},"render_type":"solid"}}],
  "shadows":[{"thickness_projection_distance":0,"thickness_projection_angle":-45,"feather":0.2,"distance":10,"content":{"solid":{"color":[0,0,0]},"render_type":"solid"},"thickness_projection_enable":False,"angle":-45}],
  "font":{"path":font,"id":""}}
cuts={0:[1,1,1]}
for x in hl:
    i=txt.index(x); cuts[i]=[1,.86,0]; cuts.setdefault(i+len(x),[1,1,1])
ks=sorted(cuts); styles=[style([s,(ks[j+1] if j+1<len(ks) else len(txt))],cuts[s]) for j,s in enumerate(ks)]
t=out["materials"]["texts"][-1]
t.update(content=json.dumps({"styles":styles,"text":txt}),recognize_text="",recognize_task_id="",font_size=19.0,words={"start_time":[],"end_time":[],"text":[]},
  background_alpha=0.0,background_color="",background_style=0,has_shadow=True,shadow_color="#000000ff",shadow_alpha=1.0,shadow_distance=10.0,shadow_smoothing=0.2,
  border_width=0.12,border_color="#000000ff",border_alpha=1.0,bold_width=0.012,line_spacing=0.1,line_max_width=0.95,is_rich_text=True,alignment=1,text_color="#ffffffff")
out["tracks"]=[{**{k:x for k,x in vt.items() if k!="segments"},"id":nid(),"segments":[vs]},{**{k:x for k,x in tt.items() if k!="segments"},"id":nid(),"segments":[ts]}]
out["duration"]=dur; s=json.dumps(out,separators=(",",":"),ensure_ascii=False)
for rel in ["draft_info.json","Timelines/%s/draft_info.json"%TLID]:
    shutil.copy2(P+rel,P+rel+".pre-overlay"); open(P+rel,"w").write(s)
m=json.load(open(P+"draft_meta_info.json")); shutil.copy2(P+"draft_meta_info.json",P+"draft_meta_info.json.pre-overlay")
m["tm_duration"]=dur
m["draft_materials"][0]["value"]=[{"ai_group_type":"","create_time":0,"duration":dur,"enter_from":0,"extra_info":os.path.basename(vid),"file_Path":vid,"height":h,"id":v["local_material_id"],"import_time":0,"import_time_ms":-1,"item_source":1,"md5":"","metetype":"video","roughcut_time_range":{"duration":dur,"start":0},"sub_time_range":{"duration":-1,"start":-1},"type":0,"width":w}]
json.dump(m,open(P+"draft_meta_info.json","w"),separators=(",",":")); print("ok",name,dur,w,h)
