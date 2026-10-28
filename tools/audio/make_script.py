#!/usr/bin/env python3
"""Turn tabs of a study-kit HTML page into spoken-word scripts (.txt), ready for TTS.

Usage:
  python3 make_script.py KIT.html OUTDIR SECTION_ID[:Label] [SECTION_ID[:Label] ...]
Example:
  python3 make_script.py ../../MATHS350/topology-exam-kit.html out bookwork:Bookwork defs:Definitions

Each section (the element with that id) is read in document order: headings, <summary>,
<dt>/<dd> pairs, <p> and <li>. Tables, <pre>/.calc blocks, SVGs, scripts and interactive
widgets (.flash, .dq, inputs, buttons) are skipped. Maths symbols become words (see speak()).
"""
import re, sys, os
from bs4 import BeautifulSoup, NavigableString
GREEK={'α':'alpha','β':'beta','σ':'sigma','τ':'tau','ρ':'rho','φ':'phi','θ':'theta','λ':'lambda','ε':'epsilon','γ':'gamma','π':'pi','Δ':'delta','Σ':'sum','ψ':'psi','μ':'mu','κ':'kappa'}
def inner(el):
    out=[]
    for c in el.children:
        if isinstance(c,NavigableString): out.append(str(c))
        elif c.name=='sub':
            t=c.get_text()
            out.append(' star' if t=='*' else ' '+t+' ')
        elif c.name=='sup':
            t=c.get_text()
            if t in('2','²'): out.append(' squared ' if False else ' '+t+' ')
            elif t=='A': out.append(' to the A ')
            else: out.append(' to the '+t+' ')
        elif c.name in('span',) and 'tag' in (c.get('class') or []): continue
        elif c.name in('span',) and 'qed' in (c.get('class') or []): continue
        else: out.append(inner(c))
    return ''.join(out)
SUBS=str.maketrans({'₀':' 0','₁':' 1','₂':' 2','₃':' 3','ₙ':' n','ᵢ':' i','ⱼ':' j','ₘ':' m','₊':' plus','₋':' minus'})
SUPS={'¹':' 1','²':' 2','³':' 3','ⁿ':' n','⁺':' plus'}
def speak(t):
    t=t.replace('(⇒)','Forward direction. ').replace('(⇐)','Reverse direction. ').replace('⇒:',', forward direction:').replace('⇐:',', reverse direction:').replace('⇐',' Reverse direction. ')
    t=t.replace('′',' prime').replace('°',' interior').replace('⊔',' disjoint union ').replace('≡',' is identically ').replace('𝒫',' the power set of').replace('⟨','').replace('⟩','').replace('§','section ').replace('é','e').replace('ń','n')
    t=t.replace('IVT','I.V.T.').replace('dim 1','dimension 1').replace('dim 2','dimension 2').replace('Heine–Borel','Heine Borel').replace('+',' plus ')
    t=re.sub(r'\b(id)\b','the identity',t)
    t=re.sub(r'\[(v[^\]]*)\]',r' the simplex \1 ',t)
    t=re.sub(r'\[([^\[\],]{1,8}),\s*([^\[\],]{1,8})\]',r' the closed interval \1 to \2 ',t)
    t=re.sub(r'\{([^{}]{1,40})\}',r' the set \1 ',t)
    t=re.sub(r'(?<![A-Za-z])([A-Za-zα-ωΔ][̂̄]?\*?)\s?\((?=[^()]{1,25}\))',r'\1 of (',t)
    def pair(m):
        a,b=m.group(1).strip(),m.group(2).strip()
        if m.string[:m.start()].endswith('of '): return ' '+a+', '+b+' '
        if re.search(r'[xyzpst]|^0$',a+' '+b) and not re.fullmatch(r'[-−]?\d+',a): return ' the point '+a+', '+b+' '
        if a=='0' and b in('0',): return ' the origin '
        return ' the open interval '+a+' to '+b+' '
    t=re.sub(r'\(([^(),]{1,8}),\s*([^(),]{1,8})\)',pair,t)
    t=re.sub(r'\binf\b','the infimum of',t)
    t=re.sub(r'\((\d|i{1,3}|iv|v|vi|[a-e])\)',r' part \1, ',t)
    t=t.replace('∎','').replace('T3½','T three and a half').replace('½',' a half ')
    t=re.sub(r'\[0,\s*1\]',' the unit interval ',t)
    t=re.sub(r'([A-Za-zσ])⁻¹',r'\1 inverse',t); t=t.replace('⁻¹',' inverse')
    combos={'σ̂':' sigma hat ','τ̂':' tau hat ','f̂':' f hat ','F̂':' F hat ','Ĥ':' H hat ','v̂':' v hat ','σ̄':' sigma bar ','ρ̄':' rho bar ','τ̄':' tau bar ','ä':' the constant loop at a ','Ã':' A tilde ','Ā':' A bar ','b̈':' the constant loop at b '}
    for k,v in combos.items(): t=t.replace(k,v)
    for k,v in SUPS.items(): t=t.replace(k,v)
    t=t.translate(SUBS)
    rep=[('⇔',' if and only if '),('⇒',', which implies '),('↦',' maps to '),('→',' to '),('∉',' is not in '),('∈',' in '),('∋',' containing '),
      ('⊆',' is a subset of '),('⊂',' is a subset of '),('⊇',' contains '),('⋃',' the union of '),('⋂',' the intersection of '),('∪',' union '),('∩',' intersect '),
      ('∖',' minus '),('×',' cross '),('∅',' the empty set '),('≠',' is not equal to '),('≤',' at most '),('≥',' at least '),('≅',' is isomorphic to '),('≃',' is homotopy equivalent to '),
      ('∼',' tilde '),('∘',' composed with '),('∂',' boundary '),('∏',' the product of '),('ℝ',' R '),('ℚ',' Q '),('ℤ',' Z '),('ℕ',' N '),('ℙ',' P '),('𝔠',' the continuum '),
      ('∞',' infinity '),('∗',' star '),('↾',' restricted to '),('±',' plus or minus '),('√',' root '),('−',' minus '),('…',' dot dot dot '),('⋯',' dot dot dot '),('▢',''),('·',' times '),('—',', '),('–',' to '),('=',' equals '),('<',' less than '),('>',' greater than '),('|',' ')]
    for a,b in rep: t=t.replace(a,b)
    for k,v in GREEK.items(): t=t.replace(k,' '+v+' ')
    words=[(r'\bnbhds\b','neighbourhoods'),(r'\bnbhd\b','neighbourhood'),(r'\biff\b','if and only if'),(r'\bcl\b','the closure of'),(r'\bint\b','the interior of'),(r'\bfr\b','the frontier of'),
      (r'\bker\b','the kernel of'),(r'\bIm\b','the image of'),(r'\bT0\b','T zero'),(r'\bT1\b','T one'),(r'\bT2\b','T two'),(r'\bT3\b','T three'),(r'\bT4\b','T four'),
      (r'\bProp\b\.?','Proposition'),(r'\bThm\b\.?','Theorem'),(r'\bCor\b\.?','Corollary'),(r'\bDef\b\.?','Definition'),(r'\bEx\b\.?','Example'),(r'\be\.g\.','for example'),(r'\bi\.e\.','that is'),
      (r'\bA(\d)\.(\d+)',r'algebraic \1 point \2'),(r'\bcts\b','continuous'),(r'\bvs\b','versus'),(r'\b(\d+)\.(\d+)\b',r'\1 point \2')]
    for a,b in words: t=re.sub(a,b,t)
    t=re.sub(r'\(([^()]{1,3})\)',r' \1 ',t)  # (i) (1) etc
    t=re.sub(r'[\[\]{}()]',' , ',t)
    t=re.sub(r'(the set\s+)+','the set ',t)
    t=re.sub(r'\s*,\s*(,\s*)+',', ',t); t=re.sub(r'\s+',' ',t).strip()
    t=re.sub(r'\s+([,.;:])',r'\1',t); t=re.sub(r'^,\s*','',t)
    return t

SKIP_TAGS={'table','pre','svg','script','style','button','input','select','nav'}
SKIP_CLASSES={'calc','flash','dq','chips','row','tag','qed','score','fig'}
BLOCKS=['h2','h3','h4','summary','dt','p','li']
def skipped(el,root):
    for a in [el,*el.parents]:
        if a is root: return False
        if a.name in SKIP_TAGS or SKIP_CLASSES & set(a.get('class') or []): return True
    return False
def read_section(soup,sid,label):
    root=soup.find(id=sid)
    if root is None: sys.exit(f"no element with id={sid}")
    L=[label+'.']
    for el in root.find_all(BLOCKS):
        if skipped(el,root): continue
        if el.find_parent(BLOCKS) and el.find_parent(BLOCKS) is not el and root in el.find_parent(BLOCKS).parents: continue
        if el.name=='dt':
            dd=el.find_next_sibling('dd'); n=el.find(class_='num')
            name=el.get_text().replace(n.get_text(),'') if n else el.get_text()
            head=speak(name)+(', '+speak(n.get_text()) if n else '')
            L.append(head+'. '+(speak(inner(dd)) if dd else '')); continue
        if el.name=='h2': continue  # section title is already the label
        if el.name in('h3','h4'): L.append(''); L.append(speak(el.get_text())+'.'); continue
        if el.name=='summary':
            parts=[speak(inner(c)) for c in el.find_all('span') if not (set(c.get('class') or [])&SKIP_CLASSES)]
            L.append('. '.join(p for p in parts if p)+'.'); continue
        txt=speak(inner(el))
        if txt: L.append(('Statement. ' if 'stmt' in (el.get('class') or []) else '')+txt)
    return L
if __name__=='__main__':
    if len(sys.argv)<4: sys.exit(__doc__)
    html,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
    soup=BeautifulSoup(open(html,encoding='utf-8').read(),'html.parser')
    for arg in sys.argv[3:]:
        sid,_,label=arg.partition(':'); label=label or sid.title()
        open(os.path.join(out,sid+'.txt'),'w').write('\n'.join(read_section(soup,sid,label)))
        print('wrote',os.path.join(out,sid+'.txt'))
