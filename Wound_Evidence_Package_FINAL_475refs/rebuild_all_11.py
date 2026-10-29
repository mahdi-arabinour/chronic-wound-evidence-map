#!/usr/bin/env python3
"""Portable rebuild of 11 retained descriptive supplementary figures from filtered article-level CSVs.
Run: python rebuild_all_11.py
Requires matplotlib, numpy. Does not access the internet.
This demonstrates numerical consistency of selected-source descriptive coding, NOT independent scientific validation.
"""
from pathlib import Path
from collections import Counter,defaultdict
import csv,re,json,math,textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
ROOT=Path(__file__).resolve().parent
CODE=ROOT/'coding';MAT=ROOT/'matrices';F=ROOT/'figures';F.mkdir(exist_ok=True)
source={1:1,2:1,3:1,4:2,5:2,6:2,7:3,8:3,9:4,10:4,11:5,12:5,13:5,14:5}
expected_n={1:28,2:28,3:28,4:20,5:20,6:20,7:37,8:41,9:45,10:45,11:34,12:34,13:34,14:34}
si={}
with (ROOT/'Current_SI_Table_References.csv').open(encoding='utf-8-sig',newline='') as h:
 for r in csv.DictReader(h):si.setdefault(r['SI_Table'],set()).add(int(r['Reference_number']))
with (ROOT/'Current_Main_475_References.csv').open(encoding='utf-8-sig',newline='') as h:registered={int(r['Reference_number']) for r in csv.DictReader(h)}
assert len(registered)==475

def norm(x):return ' '.join(str(x or '').casefold().split())
def openrows(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def matrix(p):
 with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.reader(h))
def short(x,width=23):
 x=' '.join(str(x).split())
 return '\n'.join(textwrap.wrap(x,width,break_long_words=False,break_on_hyphens=False))

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.right':False,'axes.spines.top':False,'savefig.facecolor':'white','figure.facecolor':'white'})
COL=LinearSegmentedColormap.from_list('sourcecounts',['#f2f7f8','#aecbd5','#528dab','#205176'])
aspects={1:2452/1300,2:2452/1584,3:1196/849,4:7612/3761,5:7867/3760,6:7972/4953,7:1365/760,8:1365/658,9:1365/827,10:1365/703,11:1365/781,12:1365/870,13:1365/781,14:1365/863}
style={1:'readout',2:'time',3:'bubble',4:'modules',5:'outputs',6:'hbar',7:'outputheat',8:'descriptorheat',9:'hbar',10:'dataheat',11:'maturityheat',12:'hbar',13:'stack',14:'hbar'}
titles={1:'AI-ready readout domains across wound-model classes',2:'Temporal depth of reported wound-model measurements',3:'Exploratory model complexity and disease-context scores',4:'Programmed wound-state modules',5:'Quantitative readout coverage by platform class',6:'Unaddressed translational limitations',7:'Trigger / staged-release material outputs',8:'Smart biomaterial descriptor domains',9:'AI tasks represented among Table S4 sources',10:'Data modalities in the mapped AI studies',11:'Exploratory evidence-maturity categories',12:'Translational bottlenecks in mapped studies',13:'Hypothetical early-stage animal-use reduction potential',14:'Risks of overinterpretation in the evidence map'}

def common(fig,no):
 fig.patch.set_facecolor('white')
 fig.suptitle(f'Figure S{no}  |  {titles[no]}',fontsize=12,weight='bold',y=.985,color='#23384a')

XSHORT={
 1:['Time','Imaging','Barrier','Molecular','Histology','Material','Vascular'],
 4:['Flow','O2 / vessels','Barrier','Inflammation','Infection','Bio sensing','Actuation'],
 5:['Imaging','Barrier','Molecular','Bio sensing','Microbial','Vascular','Drug response'],
 7:['Release','Biofilm','Immune','Vascular','Matrix','Epithelial','Closure','Safety'],
 8:['Material','Release','Biofilm','Redox','Immune','Vascular','Histology','Area / time','Safety'],
 10:['Images','Multi-image','Clinical','Time series','Omics','Material','Sensors','Actuation'],
 11:['Low','Moderate','Mod-high','High']
}
def heat(m,no):
 r=m[1:];xs=m[0][1:-1];ys=[x[0] for x in r]
 a=np.asarray([[float(v or 0) for v in x[1:-1]] for x in r])
 width=10.6;fig,ax=plt.subplots(figsize=(width,width/aspects[no]),dpi=180)
 im=ax.imshow(a,cmap=COL,vmin=0,vmax=max(1,a.max()),aspect='auto')
 ax.set_yticks(range(len(ys)),labels=[short(x,29 if no in (8,11) else 27) for x in ys],fontsize=8.1)
 ax.set_xticks(range(len(xs)),labels=XSHORT[no],fontsize=8.4)
 ax.tick_params(length=0)
 for i in range(len(ys)):
  for j in range(len(xs)):
   v=int(a[i,j]);ax.text(j,i,str(v),fontsize=9,ha='center',va='center',weight='semibold',color='white' if v>max(1,a.max())*.58 else '#183549')
 ax.set_xticks(np.arange(-.5,len(xs),1),minor=True);ax.set_yticks(np.arange(-.5,len(ys),1),minor=True)
 ax.grid(which='minor',color='white',linewidth=.8)
 ax.tick_params(which='minor',bottom=False,left=False)
 common(fig,no)
 fig.colorbar(im,ax=ax,fraction=.020,pad=.012).set_label('Coded studies',fontsize=8)
 left=.24 if no in (1,4,5,7,8,10) else .31
 bottom=.16 if len(xs)>=7 else .17
 fig.subplots_adjust(left=left,right=.96,bottom=bottom,top=.85)
 return fig

def bars(m,no):
 r=[(short(x[0],49),int(x[1])) for x in m[1:]]
 r=sorted(r,key=lambda x:(-x[1],x[0]))
 fig,ax=plt.subplots(figsize=(10.6,10.6/aspects[no]),dpi=180)
 yy=np.arange(len(r));vals=[x[1] for x in r]
 ax.barh(yy,vals,height=.64,color='#235c7b')
 ax.set_yticks(yy,labels=[x[0] for x in r],fontsize=8.4)
 ax.invert_yaxis();ax.set_xlim(0,max(vals)*1.17)
 for i,v in enumerate(vals):ax.text(v+.25,i,str(v),va='center',fontsize=8.6,weight='bold',color='#213744')
 ax.set_xlabel('Coded references (overlapping categories possible)',fontsize=9)
 ax.grid(axis='x',color='#d7e4ea',alpha=.7,linestyle=':');ax.set_axisbelow(True)
 common(fig,no);fig.subplots_adjust(left=.45,right=.95,bottom=.12,top=.86)
 return fig

def timeplot(m,no):
 r=m[1:];g=[x[0] for x in r]; cats=m[0][1:-1]
 a=np.asarray([[int(x) for x in row[1:-1]] for row in r]);cum=np.zeros(len(g));colors=['#dfebef','#8fb4c7','#3e819e','#1c4f76']
 fig,ax=plt.subplots(figsize=(10.6,10.6/aspects[no]),dpi=180)
 for j,label in enumerate(cats):
  vals=a[:,j]; ax.barh(np.arange(len(g)),vals,left=cum,color=colors[j],height=.56,label=short(label,28))
  for i,v in enumerate(vals):
   if v:ax.text(cum[i]+v/2,i,str(v),ha='center',va='center',fontweight='bold',color='white' if j>=2 else '#1a3744',fontsize=9)
  cum+=vals
 ax.set_yticks(np.arange(len(g)),labels=[short(x,32) for x in g],fontsize=9);ax.invert_yaxis();ax.set_xlim(0,max(cum)*1.10)
 ax.set_xlabel('Studies per model class',fontsize=9)
 ax.legend(loc='upper center',bbox_to_anchor=(.5,-.21),ncol=2,frameon=False,fontsize=8.5)
 common(fig,no);fig.subplots_adjust(left=.34,right=.96,bottom=.29,top=.85)
 return fig

def bubbleplot(m,no):
 fig,ax=plt.subplots(figsize=(10.6,10.6/aspects[no]),dpi=180)
 colors=['#286280','#6b9f9f','#a06970','#bc925f']
 for k,r in enumerate(m[1:]):
  g,n,x,y=r; x=float(x);y=float(y); n=int(n)
  ax.scatter(x,y,s=n*145,c=[colors[k]],edgecolors='#1f3342',linewidths=.9,alpha=.87)
  dx={0:.12,1:.09,2:-.17,3:-.16}[k];dy={0:.16,1:-.22,2:.17,3:-.25}[k]
  ax.annotate(short(g,27)+f'\n(n={n})',(x,y),xytext=(x+dx,y+dy),fontsize=9,weight='medium',color='#183445',ha='left' if dx>0 else 'right')
 ax.set_xlim(.65,4.3);ax.set_ylim(.6,4.35)
 ax.set_xticks([1,2,3,4]);ax.set_yticks([1,2,3,4]);ax.grid(color='#dbe7ea',linestyle=':',zorder=0)
 ax.set_xlabel('Proposed structural complexity score (1-4)',fontsize=9)
 ax.set_ylabel('Proposed chronic disease relevance (1-4)',fontsize=9)
 common(fig,no);fig.subplots_adjust(left=.16,right=.95,bottom=.15,top=.86)
 return fig

def stackplot(m,no):
 r=m[1:];groups=[short(x[0],38) for x in r];a=np.array([[int(v) for v in x[1:-1]] for x in r]);cats=m[0][1:-1]
 fig,ax=plt.subplots(figsize=(10.6,10.6/aspects[no]),dpi=180)
 cum=np.zeros(len(r));cols=['#205577','#8aaebf','#dee6e8']
 for j,c in enumerate(cats):
  vals=a[:,j];ax.barh(np.arange(len(r)),vals,left=cum,color=cols[j],height=.61,label=short(c,26))
  for i,v in enumerate(vals):
   if v:ax.text(cum[i]+v/2,i,str(v),ha='center',va='center',fontsize=9,color='white' if j==0 else '#1f3642',weight='bold')
  cum+=vals
 ax.set_yticks(np.arange(len(r)),labels=groups,fontsize=8.8);ax.invert_yaxis();ax.set_xlim(0,max(cum)*1.12)
 ax.set_xlabel('Source study count',fontsize=9)
 ax.legend(frameon=False,fontsize=8,ncol=3,loc='lower center',bbox_to_anchor=(.5,-.32))
 common(fig,no);fig.subplots_adjust(left=.40,right=.97,bottom=.23,top=.83)
 return fig


# Stage4 removed ordinal S3, S11, S13; all public labels renumbered sequentially.
new_to_old={1:1,2:2,3:4,4:5,5:6,6:7,7:8,8:9,9:10,10:12,11:14}
source={new:source[old] for new,old in new_to_old.items()}
expected_n={new:expected_n[old] for new,old in new_to_old.items()}
aspects={new:aspects[old] for new,old in new_to_old.items()}
style={new:style[old] for new,old in new_to_old.items()}
titles={new:titles[old] for new,old in new_to_old.items()}
XSHORT={new:XSHORT[old] for new,old in new_to_old.items() if old in XSHORT}

stats=[];checked_cells=0
for n in range(1,12):
 old=new_to_old[n]
 code=openrows(CODE/f'S{n:02d}_study_coding.csv')
 sources={int(r['Main_ref']) for r in code}
 assert len(sources)==expected_n[n],(n,len(sources))
 assert sources.issubset(registered)
 assert sources.issubset(si[f'S{source[n]}'])
 m=matrix(MAT/f'S{n:02d}_matrix.csv');counts=Counter()
 for r in code:
  v=r['Code_0_1']
  if v and v.strip() not in ('0','0.0'):counts[norm(r['Group']),norm(r['Domain'])]+=int(v)
 if old==2:
  for row in m[1:]:
   for j,d in enumerate(m[0][1:-1]):
    assert counts[norm(row[0]),norm(d)]==int(row[j+1]);checked_cells+=1
  fig=timeplot(m,n)
 elif old in (6,9,12,14):
  for row in m[1:]:
   val=sum(int(r['Code_0_1'] or 0) for r in code if norm(r['Group' if old==9 else 'Domain'])==norm(row[0]))
   assert val==int(row[1]),(n,old,row[0],val,row[1]);checked_cells+=1
  fig=bars(m,n)
 else:
  for row in m[1:]:
   for j,d in enumerate(m[0][1:-1]):
    assert counts[norm(row[0]),norm(d)]==int(row[j+1]),(n,old,row[0],d,counts[norm(row[0]),norm(d)],row[j+1]);checked_cells+=1
  fig=heat(m,n)
 out=F/f'Figure_S{n:02d}_REBUILT.png'
 fig.savefig(out,dpi=190,facecolor='white')
 fig.savefig(out.with_suffix('.svg'),format='svg',facecolor='white');plt.close(fig)
 stats.append({'figure':f'S{n}','source_table':f'Table S{source[n]}','unique_studies':len(sources),'coding_records':len(code),'image':out.name})
 print('Rebuilt S'+str(n),'n',len(sources),'records',len(code),'image bytes',out.stat().st_size)
assert checked_cells==339,(checked_cells,'expected 339 numerical cells')
(ROOT/'REBUILD_VALIDATION.json').write_text(json.dumps({'count_cells_verified':checked_cells,'comparison_pass':True,'figures':stats,'limitation':'Numerical reproduction of 11 descriptive figures. No independent full-text validation of all source classifications.'},indent=2),encoding='utf-8')
print('PASS:',checked_cells,'of',checked_cells,'matrix numeric cells; 11 descriptive figures generated.')
