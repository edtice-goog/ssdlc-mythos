# -*- coding: utf-8 -*-
"""Build the merged SSDLC deck.

Re-runnable: cut a line out of PLAN, re-run, and page numbers follow automatically.
"""
import zipfile, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Data\ssdlc-mythos')

OUT  = 'ssdlc-mythos-full.pptx'
THES = 'ssdlc-thesis.pptx'
DIAG = 'two-loop-calibration.pptx'
FOOT = 'SSDLC in the Mythos Era  \u00b7  '
DIAG_SCALE = 0.75          # 13.333in canvas -> 10in canvas

# (source deck, slide part, section label; label None = title/divider slide, no footer)
PLAN = [
    (THES, 'slide1',  None),
    (THES, 'slide2',  'Thesis'),
    (THES, 'slide3',  'Thesis'),
    (THES, 'slide4',  'Thesis'),
    (THES, 'slide11', 'Thesis'),      # THE TREND: finding -> exploiting -> chaining
    (THES, 'slide5',  'Thesis'),      # collapsed reference frame, carries the cost point
    (THES, 'slide8',  'Thesis'),
    (THES, 'slide9',  'Thesis'),
    (THES, 'slide10', 'Thesis'),

    ('01-classification.pptx', 'slide1', None),
    ('01-classification.pptx', 'slide2', 'Classification'),
    ('01-classification.pptx', 'slide3', 'Classification'),
    ('01-classification.pptx', 'slide4', 'Classification'),
    ('01-classification.pptx', 'slide5', 'Classification'),
    ('01-classification.pptx', 'slide6', 'Classification'),
    ('01-classification.pptx', 'slide7', 'Classification'),

    ('02-placement.pptx', 'slide1', None),
    ('02-placement.pptx', 'slide2', 'Placement'),
    ('02-placement.pptx', 'slide3', 'Placement'),
    ('02-placement.pptx', 'slide4', 'Placement'),
    ('02-placement.pptx', 'slide5', 'Placement'),
    ('02-placement.pptx', 'slide6', 'Placement'),
    ('02-placement.pptx', 'slide7', 'Placement'),

    ('03-tool-properties.pptx', 'slide1', None),
    ('03-tool-properties.pptx', 'slide2', 'Tool Properties'),
    ('03-tool-properties.pptx', 'slide3', 'Tool Properties'),
    ('03-tool-properties.pptx', 'slide4', 'Tool Properties'),
    ('03-tool-properties.pptx', 'slide5', 'Tool Properties'),
    ('03-tool-properties.pptx', 'slide6', 'Tool Properties'),
    ('03-tool-properties.pptx', 'slide7', 'Tool Properties'),

    ('05-ai-roles.pptx', 'slide1', None),
    ('05-ai-roles.pptx', 'slide2', 'AI Roles'),
    ('05-ai-roles.pptx', 'slide3', 'AI Roles'),
    ('05-ai-roles.pptx', 'slide4', 'AI Roles'),
    ('05-ai-roles.pptx', 'slide5', 'AI Roles'),
    ('05-ai-roles.pptx', 'slide6', 'AI Roles'),
    ('05-ai-roles.pptx', 'slide7', 'AI Roles'),

    ('06-economics.pptx', 'slide1', None),
    ('06-economics.pptx', 'slide6', 'Economics'),
    ('06-economics.pptx', 'slide2', 'Economics'),
    ('06-economics.pptx', 'slide5', 'Economics'),

    ('07-agentic-oversight.pptx', 'slide1', None),
    ('07-agentic-oversight.pptx', 'slide3', 'Agentic Oversight'),
    ('07-agentic-oversight.pptx', 'slide5', 'Agentic Oversight'),
    ('07-agentic-oversight.pptx', 'slide4', 'Agentic Oversight'),
    ('07-agentic-oversight.pptx', 'slide6', 'Agentic Oversight'),

    (DIAG, 'slide1', 'Agentic Oversight'),   # two-loop diagram, rescaled; closes the deck
]

EMU = 914400
RT  = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
TOTAL = len(PLAN)
# section-divider slides = slide1 of every sub-deck except the thesis title slide
DIVIDERS = {(d, s) for d, s, lab in PLAN if lab is None and d != THES}

_zips = {}
def Z(d):
    if d not in _zips:
        _zips[d] = zipfile.ZipFile(d)
    return _zips[d]

def rels_path(part):
    head, tail = part.rsplit('/', 1)
    return head + '/_rels/' + tail + '.rels'

def rels_for(d, part):
    try:
        return Z(d).read(rels_path(part)).decode('utf-8')
    except KeyError:
        return None

def resolve(base, target):
    segs = base.rsplit('/', 1)[0].split('/')
    for s in target.split('/'):
        if s == '..':
            segs.pop()
        elif s and s != '.':
            segs.append(s)
    return '/'.join(segs)

# ---------------------------------------------------------------- 1. gather parts
need = {}
for d, s, _ in PLAN:
    need.setdefault(d, set()).add('ppt/slides/%s.xml' % s)

for d in list(need):
    frontier = list(need[d])
    while frontier:
        part = frontier.pop()
        rx = rels_for(d, part)
        if not rx:
            continue
        for m in re.finditer(r'Type="([^"]+)" Target="([^"]+)"', rx):
            typ, tgt = m.group(1), m.group(2)
            if tgt.startswith('http') or typ.endswith('notesMaster'):
                continue
            tp = resolve(part, tgt)
            if tp not in need[d]:
                need[d].add(tp)
                frontier.append(tp)

# the thesis supplies the one shared notesMaster (plus the theme it points at)
need[THES].add('ppt/notesMasters/notesMaster1.xml')
for m in re.finditer(r'Target="([^"]+)"',
                     Z(THES).read('ppt/notesMasters/_rels/notesMaster1.xml.rels').decode('utf-8')):
    need[THES].add(resolve('ppt/notesMasters/notesMaster1.xml', m.group(1)))

# ---------------------------------------------------------------- 2. rename parts
KINDS = [('ppt/slides/', 'slide'), ('ppt/slideLayouts/', 'slideLayout'),
         ('ppt/slideMasters/', 'slideMaster'), ('ppt/notesSlides/', 'notesSlide'),
         ('ppt/notesMasters/', 'notesMaster'), ('ppt/theme/', 'theme'), ('ppt/media/', 'media')]
counter = {k: 0 for _, k in KINDS}
newname = {}

def assign(d, part):
    if (d, part) in newname:
        return newname[(d, part)]
    for prefix, kind in KINDS:
        if part.startswith(prefix):
            counter[kind] += 1
            nn = '%s%s%d.%s' % (prefix, kind, counter[kind], part.rsplit('.', 1)[1])
            newname[(d, part)] = nn
            return nn
    raise SystemExit('unclassified part: ' + part)

for d, s, _ in PLAN:                       # slides first, so slideN == presentation order
    assign(d, 'ppt/slides/%s.xml' % s)
for d in sorted(need):
    for part in sorted(need[d]):
        assign(d, part)

# ---------------------------------------------------------------- 3. transforms
def scale(x, f=DIAG_SCALE):
    x = re.sub(r'(<a:(?:off|chOff) x=")(-?\d+)(" y=")(-?\d+)(")',
               lambda m: m.group(1) + str(int(int(m.group(2)) * f)) + m.group(3)
                         + str(int(int(m.group(4)) * f)) + m.group(5), x)
    x = re.sub(r'(<a:(?:ext|chExt) cx=")(\d+)(" cy=")(\d+)(")',
               lambda m: m.group(1) + str(int(int(m.group(2)) * f)) + m.group(3)
                         + str(int(int(m.group(4)) * f)) + m.group(5), x)
    x = re.sub(r'\bsz="(\d+)"', lambda m: 'sz="%d"' % max(100, int(int(m.group(1)) * f)), x)
    x = re.sub(r'<a:ln w="(\d+)"', lambda m: '<a:ln w="%d"' % max(1, int(int(m.group(1)) * f)), x)
    return x

SP_RE = re.compile(r'<p:sp>(?:(?!</p:sp>).)*</p:sp>', re.S)

def drop_spine(x):
    """Remove the four-box series spine + caption (everything below y = 4.95in)."""
    out, last, removed = [], 0, 0
    for m in SP_RE.finditer(x):
        off = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>', m.group(0))
        if off and int(off.group(2)) / EMU >= 4.95:
            out.append(x[last:m.start()])
            last = m.end()
            removed += 1
    out.append(x[last:])
    if removed == 0:
        raise SystemExit('drop_spine removed nothing')
    return ''.join(out)

PHASE2_X, PHASE8_X = 1481328, 7562088

def collapse_reference(x):
    """One reference-frame slide: highlight phases 2 and 8 to match phase 1's
    existing highlight, and swap the headline for the cost-collapse point."""
    for xoff in (PHASE2_X, PHASE8_X):
        i = x.find('<a:off x="%d"' % xoff)
        if i < 0:
            raise SystemExit('phase box at x=%d not found' % xoff)
        j = x.rfind('<p:sp>', 0, i)
        k = x.index('</p:sp>', i) + len('</p:sp>')
        blk = x[j:k]
        new = (blk.replace('srgbClr val="FFFFFF"', 'srgbClr val="F4F0E8"')
                  .replace('srgbClr val="D6D6D6"', 'srgbClr val="B8860B"'))
        if new == blk:
            raise SystemExit('fill swap failed at x=%d' % xoff)
        x = x[:j] + new + x[k:]

    old_title = '<a:t>Start with prescient information</a:t>'
    if old_title not in x:
        raise SystemExit('reference headline not found')
    x = x.replace(old_title, '<a:t>Three of these were too expensive to do.</a:t>')

    old_sub = ('Traditional controls remain the deterministic backbone. AI augments triage, '
               'reach analysis, and fix synthesis. Learn/Calibrate feeds back into every earlier phase.')
    new_sub = ('Requirements &amp; Threat Model, Design, and Learn &amp; Calibrate were heavyweight '
               'human work, skipped on cost. LLM assistance collapses that cost.')
    if old_sub not in x:
        raise SystemExit('reference subtitle not found')
    return x.replace(old_sub, new_sub)

NEXT_SLIDES = {('01-classification.pptx', 'ppt/slides/slide7.xml'),
               ('02-placement.pptx', 'ppt/slides/slide7.xml'),
               ('03-tool-properties.pptx', 'ppt/slides/slide7.xml')}

def drop_tool_selection_row(x):
    """The section roadmap slides list all four decks. Tool Selection is cut, so
    remove its row: the Now/Next marker, the label, and the description under it."""
    y0 = None
    for m in SP_RE.finditer(x):
        if '<a:t>Tool Selection</a:t>' in m.group(0):
            y0 = int(re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>', m.group(0)).group(2)) / EMU
            break
    if y0 is None:
        raise SystemExit('Tool Selection row not found')
    out, last, removed = [], 0, 0
    for m in SP_RE.finditer(x):
        off = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>', m.group(0))
        if not off:
            continue
        y = int(off.group(2)) / EMU
        if y0 - 0.06 <= y <= y0 + 0.55 and y < 4.95:      # keep the footer band
            out.append(x[last:m.start()])
            last = m.end()
            removed += 1
    out.append(x[last:])
    # marker chip background, marker label, row label, row description
    if removed != 4:
        raise SystemExit('expected to remove 4 shapes, removed %d' % removed)
    x = ''.join(out)
    # this one's headline was purely a handoff to the cut section
    return x.replace('<a:t>Properties name the interface. Selection picks the implementations.</a:t>',
                     '<a:t>Properties name the interface. The marketplace picks the implementations.</a:t>')

def apply_footer(x, label, page):
    if not label:
        return x
    x = re.sub(r'<a:t>SSDLC in the Mythos Era[^<]*</a:t>',
               '<a:t>%s%s</a:t>' % (FOOT, label), x)
    x = re.sub(r'<a:t>\s*\d+\s*/\s*\d+\s*</a:t>', '<a:t>%d / %d</a:t>' % (page, TOTAL), x)
    return x

GEOM_PARTS = ('ppt/slides/', 'ppt/slideLayouts/', 'ppt/slideMasters/')

# sldMasterId and sldLayoutId share one global id space across the whole package.
# Every source deck numbered its first layout 2147483649, so they must be reassigned.
MASTER_ID_BASE = 2147483648
_layout_gid = [MASTER_ID_BASE + 128]

def renumber_layout_ids(x):
    def bump(_m):
        _layout_gid[0] += 1
        return '<p:sldLayoutId id="%d"' % _layout_gid[0]
    return re.sub(r'<p:sldLayoutId id="\d+"', bump, x)

def transform(d, part, x, page, label):
    is_slide = part.startswith('ppt/slides/')
    if d == DIAG and part.startswith(GEOM_PARTS):
        x = scale(x)
    if part.startswith('ppt/slideMasters/'):
        x = renumber_layout_ids(x)
    if is_slide:
        key = (d, part.split('/')[-1][:-4])
        if (d, part) == (THES, 'ppt/slides/slide5.xml'):
            x = collapse_reference(x)
        if key in DIVIDERS:
            x = drop_spine(x)
        if (d, part) in NEXT_SLIDES:
            x = drop_tool_selection_row(x)
        x = apply_footer(x, label, page)
    return x

# ---------------------------------------------------------------- 4. write package
slide_at = {}
for i, (d, s, label) in enumerate(PLAN, 1):
    slide_at[(d, 'ppt/slides/%s.xml' % s)] = (i, label)

out = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED)
written = []
def put(name, data):
    out.writestr(name, data if isinstance(data, bytes) else data.encode('utf-8'))
    written.append(name)

NOTES_MASTER = newname[(THES, 'ppt/notesMasters/notesMaster1.xml')]

for d in sorted(need):
    for part in sorted(need[d]):
        nn = newname[(d, part)]
        raw = Z(d).read(part)
        if part.startswith('ppt/media/'):
            put(nn, raw)
        else:
            page, label = slide_at.get((d, part), (0, None))
            put(nn, transform(d, part, raw.decode('utf-8'), page, label))

        rx = rels_for(d, part)
        if rx:
            def fix(m, _part=part, _nn=nn, _d=d):
                typ, tgt = m.group(1), m.group(2)
                if tgt.startswith('http'):
                    return m.group(0)
                if typ.endswith('notesMaster'):
                    nt = NOTES_MASTER
                else:
                    nt = newname[(_d, resolve(_part, tgt))]
                a = _nn.rsplit('/', 1)[0].split('/')
                b = nt.split('/')
                while a and b[:1] == a[:1]:
                    a.pop(0); b.pop(0)
                return 'Type="%s" Target="%s"' % (typ, '../' * len(a) + '/'.join(b))
            put(rels_path(nn), re.sub(r'Type="([^"]+)" Target="([^"]+)"', fix, rx))

# ---- presentation.xml + its rels
masters = sorted({newname[k] for k in newname if '/slideMasters/' in k[1]},
                 key=lambda s: int(re.search(r'(\d+)', s.split('/')[-1]).group(1)))
prels, sldids = [], []
for i, m in enumerate(masters):
    prels.append('<Relationship Id="rId%d" Type="%sslideMaster" Target="%s"/>'
                 % (i + 1, RT, m[len('ppt/'):]))
base = len(masters)
prels.append('<Relationship Id="rId%d" Type="%snotesMaster" Target="%s"/>'
             % (base + 1, RT, NOTES_MASTER[len('ppt/'):]))
for i, (d, s, _) in enumerate(PLAN, 1):
    rid = base + 1 + i
    prels.append('<Relationship Id="rId%d" Type="%sslide" Target="%s"/>'
                 % (rid, RT, newname[(d, 'ppt/slides/%s.xml' % s)][len('ppt/'):]))
    sldids.append('<p:sldId id="%d" r:id="rId%d"/>' % (255 + i, rid))
n = base + 1 + TOTAL
for kind, tgt in [('presProps', 'presProps.xml'), ('viewProps', 'viewProps.xml'),
                  ('theme', newname[(THES, 'ppt/theme/theme1.xml')][len('ppt/'):]),
                  ('tableStyles', 'tableStyles.xml')]:
    n += 1
    prels.append('<Relationship Id="rId%d" Type="%s%s" Target="%s"/>' % (n, RT, kind, tgt))

put('ppt/_rels/presentation.xml.rels',
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    + ''.join(prels) + '</Relationships>')

put('ppt/presentation.xml',
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" saveSubsetFonts="1">'
    '<p:sldMasterIdLst>'
    + ''.join('<p:sldMasterId id="%d" r:id="rId%d"/>' % (MASTER_ID_BASE + i, i + 1)
              for i in range(len(masters)))
    + '</p:sldMasterIdLst>'
    + '<p:sldIdLst>' + ''.join(sldids) + '</p:sldIdLst>'
    + '<p:notesMasterIdLst><p:notesMasterId r:id="rId%d"/></p:notesMasterIdLst>' % (base + 1)
    + '<p:sldSz cx="9144000" cy="5143500"/><p:notesSz cx="6858000" cy="9144000"/>'
      '</p:presentation>')

for part in ['ppt/presProps.xml', 'ppt/viewProps.xml', 'ppt/tableStyles.xml', 'docProps/core.xml']:
    put(part, Z(THES).read(part))

put('docProps/app.xml',
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
    'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
    '<Application>Microsoft Office PowerPoint</Application><Slides>%d</Slides></Properties>' % TOTAL)

put('_rels/.rels',
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="%sofficeDocument" Target="ppt/presentation.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/'
    'metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="%sextendedProperties" Target="docProps/app.xml"/>'
    '</Relationships>' % (RT, RT))

# ---- [Content_Types].xml
CT = {'slides': 'slide', 'slideLayouts': 'slideLayout', 'slideMasters': 'slideMaster',
      'notesSlides': 'notesSlide', 'notesMasters': 'notesMaster'}
MIME = {'rels': 'application/vnd.openxmlformats-package.relationships+xml',
        'xml': 'application/xml', 'png': 'image/png', 'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg', 'gif': 'image/gif', 'svg': 'image/svg+xml',
        'emf': 'image/x-emf', 'wmf': 'image/x-wmf', 'bmp': 'image/bmp'}
SINGLE = {'ppt/presentation.xml': 'presentationml.presentation.main',
          'ppt/presProps.xml': 'presentationml.presProps',
          'ppt/viewProps.xml': 'presentationml.viewProps',
          'ppt/tableStyles.xml': 'presentationml.tableStyles'}
ov, exts = [], {'xml', 'rels'}
for name, kind in SINGLE.items():
    ov.append('<Override PartName="/%s" ContentType="application/vnd.openxmlformats-officedocument.%s+xml"/>'
              % (name, kind))
ov.append('<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>')
ov.append('<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>')
for nn in written:
    if nn.endswith('.rels') or nn in SINGLE or nn.startswith('docProps/'):
        continue
    if nn.startswith('ppt/theme/'):
        ov.append('<Override PartName="/%s" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>' % nn)
    elif nn.startswith('ppt/media/'):
        exts.add(nn.rsplit('.', 1)[1].lower())
    else:
        folder = nn.split('/')[1]
        if folder in CT:
            ov.append('<Override PartName="/%s" ContentType="application/vnd.openxmlformats-officedocument.presentationml.%s+xml"/>'
                      % (nn, CT[folder]))

put('[Content_Types].xml',
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    + ''.join('<Default Extension="%s" ContentType="%s"/>' % (e, MIME.get(e, 'application/octet-stream'))
              for e in sorted(exts))
    + ''.join(ov) + '</Types>')

out.close()
print('wrote %s  ->  %d slides, %d masters, %d parts' % (OUT, TOTAL, len(masters), len(written)))
