import re,sys
def bank_html(s):
    m=re.search(r'<div class="sort-bank"[^>]*>',s)
    if not m: return None
    i=m.end(); depth=1
    for t in re.finditer(r'<div\b|</div>',s[i:]):
        depth += 1 if t.group(0).startswith('<div') else -1
        if depth==0: return s[i:i+t.start()]
    return s[i:]
if __name__=='__main__':
    for p in sys.argv[1:]:
        s=open(p,encoding='utf-8',errors='replace').read()
        b=bank_html(s)
        n=len(re.findall(r'class="sort-chip"',b)) if b else 0
        d=re.search(r'\bvar\s+sortTotal\s*=\s*(\d+)',s)
        print('%-38s chips=%-3s sortTotal=%s'%(p,n,d.group(1) if d else '-'))
