# -*- coding: utf-8 -*-
"""Generate a deck from its companion markdown.

A section becomes a slide only if it carries a `<!-- slide: ... -->` directive, so
doc-only sections (Why This Deck Exists) are skipped without special-casing.

    ## The Cost Components
    <!-- slide: eyebrow=THE COMPONENTS | headline=Two cost components. They move in
         opposite directions. | cols=2 -->

Within a slide section:
  * a leading plain paragraph      -> lead line under the headline
  * `**Term.** body` paragraphs    -> the labelled block grid
  * a trailing plain paragraph     -> closing line above the footer

Usage:  python build-decks.py 06-economics.md [-o out.pptx]
"""
import re, sys, os, math, zipfile, argparse, html

# ---------------------------------------------------------------- design tokens
INK, MUTED, ACCENT = '1A1A1A', '6B7280', 'B85042'
ACCENT_LT, SURFACE, WHITE = 'D89C92', 'F2F2F2', 'FFFFFF'
DISPLAY, BODY = 'Georgia', 'Calibri'

EMU        = 914400
SLIDE_W    = 10.0
SLIDE_H    = 5.625
MARGIN     = 0.50
CONTENT_W  = SLIDE_W - 2 * MARGIN          # 9.00

EYEBROW_Y, EYEBROW_H, EYEBROW_PT = 0.32, 0.22, 10
HEAD_Y,    HEAD_PT                = 0.58, 24
LEAD_PT,   LEAD_COLOR             = 13.5, MUTED
BLOCK_TITLE_PT, BLOCK_BODY_PT     = 11.5, 10.5
GUTTER     = 0.35
FOOTER_Y, FOOTER_PT = 5.32, 9
CLOSER_PT  = 10.5

# average glyph width in ems, per typeface — Georgia is materially wider than Calibri
EM = {'Calibri': 0.450, 'Georgia': 0.480}

def n_lines(text, width_in, pt, face=BODY):
    if not text:
        return 0
    per_line = max(1, int(width_in / (EM.get(face, 0.48) * pt / 72)))
    return max(1, math.ceil(len(text) / per_line))

def text_h(text, width_in, pt, face=BODY, leading=1.28):
    return n_lines(text, width_in, pt, face) * pt * leading / 72

def _norm(s):
    return set(re.sub(r'[^a-z0-9 ]', '', s.lower()).split())

def too_similar(a, b, thresh=0.50):
    """Suppress a lead line that merely restates the headline."""
    if not a or not b:
        return False
    x, y = _norm(a), _norm(b)
    if not x or not y:
        return False
    return len(x & y) / len(x | y) >= thresh

# ---------------------------------------------------------------- xml emitter
def esc(s):
    return html.escape(s, quote=False)

def run(text, pt, color, face, bold=False, italic=False, spc=None):
    a = 'sz="%d"' % int(pt * 100)
    if bold:   a += ' b="1"'
    if italic: a += ' i="1"'
    if spc:    a += ' spc="%d" kern="0"' % spc
    return ('<a:r><a:rPr lang="en-US" %s dirty="0"><a:solidFill><a:srgbClr val="%s"/></a:solidFill>'
            '<a:latin typeface="%s" pitchFamily="34" charset="0"/>'
            '<a:ea typeface="%s" pitchFamily="34" charset="-122"/>'
            '<a:cs typeface="%s" pitchFamily="34" charset="-120"/></a:rPr>'
            '<a:t>%s</a:t></a:r>' % (a, color, face, face, face, esc(text)))

_uid = [1]
def textbox(x, y, w, h, runs, anchor='t', align=None, space_after=0):
    _uid[0] += 1
    pPr = '<a:pPr indent="0" marL="0"%s%s><a:buNone/></a:pPr>' % (
        (' algn="%s"' % align) if align else '',
        (' spcAft="%d"' % space_after) if space_after else '')
    return ('<p:sp><p:nvSpPr><p:cNvPr id="%d" name="Text %d"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            '<p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln/></p:spPr>'
            '<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="%s"/>'
            '<a:lstStyle/><a:p>%s%s</a:p></p:txBody></p:sp>'
            % (_uid[0], _uid[0], int(x*EMU), int(y*EMU), int(w*EMU), int(h*EMU), anchor, pPr, ''.join(runs)))

def rect(x, y, w, h, fill=None, line=None, line_w=9525, radius=None):
    _uid[0] += 1
    geom = ('<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val %d"/></a:avLst></a:prstGeom>'
            % radius) if radius else '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
    f = '<a:solidFill><a:srgbClr val="%s"/></a:solidFill>' % fill if fill else '<a:noFill/>'
    l = ('<a:ln w="%d"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:ln>' % (line_w, line)) if line else '<a:ln><a:noFill/></a:ln>'
    return ('<p:sp><p:nvSpPr><p:cNvPr id="%d" name="Shape %d"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            '<p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>%s%s%s</p:spPr>'
            '<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>'
            % (_uid[0], _uid[0], int(x*EMU), int(y*EMU), int(w*EMU), int(h*EMU), geom, f, l))

ICON_DIR = 'deck-assets'
COL_HEAD_PT = 13
SUB_TITLE_PT, SUB_BODY_PT = 12, 10.5
ICON = 0.22

def pic(x, y, w, h, rid):
    _uid[0] += 1
    return ('<p:pic><p:nvPicPr><p:cNvPr id="%d" name="Picture %d"/>'
            '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            '<p:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            '<p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>'
            % (_uid[0], _uid[0], rid, int(x*EMU), int(y*EMU), int(w*EMU), int(h*EMU)))

ARROW = {'down': '↓', 'up': '↑', 'right': '→'}

SLIDE_TMPL = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
    '<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
    '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
    '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
    '%s</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')

# ---------------------------------------------------------------- layouts
def footer(shapes, label, page, total):
    if not label:
        return
    shapes.append(textbox(MARGIN, FOOTER_Y, 6.0, 0.25,
                          [run('SSDLC in the Mythos Era  ·  ' + label, FOOTER_PT, MUTED, BODY)],
                          anchor='ctr'))
    shapes.append(textbox(SLIDE_W - MARGIN - 0.80, FOOTER_Y, 0.80, 0.25,
                          [run('%d / %d' % (page, total), FOOTER_PT, MUTED, BODY)],
                          anchor='ctr', align='r'))

def title_slide(d):
    s = []
    if d.get('number'):
        s.append(textbox(MARGIN, 0.50, 2.00, 0.30,
                         [run(d['number'], 18, ACCENT, BODY, bold=True, spc=200)], anchor='ctr'))
    s.append(textbox(MARGIN, 1.55, 9.20, 1.15, [run(d['title'], 40, INK, DISPLAY)], anchor='t'))
    if d.get('subtitle'):
        s.append(textbox(MARGIN, 2.85, CONTENT_W, 0.50, [run(d['subtitle'], 17, INK, DISPLAY)]))
    if d.get('blurb'):
        s.append(textbox(MARGIN, 3.85, CONTENT_W, 0.40, [run(d['blurb'], 11, MUTED, BODY)]))
    s.append(rect(MARGIN, 5.05, 1.20, 0.035, fill=ACCENT))
    return s

def columns_slide(sl, label, page, total, icons):
    """Two or more columns, each a card with a header and a list of icon + title + body items."""
    s = []
    s.append(textbox(MARGIN, EYEBROW_Y, CONTENT_W, EYEBROW_H,
                     [run(sl['eyebrow'], EYEBROW_PT, ACCENT, BODY, bold=True, spc=200)], anchor='ctr'))
    hh = text_h(sl['headline'], CONTENT_W, HEAD_PT, DISPLAY)
    s.append(textbox(MARGIN, HEAD_Y, CONTENT_W, max(0.45, hh), [run(sl['headline'], HEAD_PT, INK, DISPLAY)]))
    y = HEAD_Y + max(0.45, hh) + 0.20

    cols = sl['columns']
    n = len(cols)
    cw = (CONTENT_W - GUTTER * (n - 1)) / n
    pad = 0.28
    inner = cw - 2 * pad - ICON - 0.14

    # one shared card height so the columns stay level
    def col_h(c):
        h = pad + COL_HEAD_PT * 1.3 / 72 + 0.30
        for _t, b in c['items']:
            h += max(ICON, text_h(_t, inner, SUB_TITLE_PT)) + 0.05 + text_h(b, inner, SUB_BODY_PT) + 0.26
        return h + pad - 0.26
    # never clamp: the items lay out at full height regardless, so a shorter card
    # would just let them spill past its edge
    ch = max(col_h(c) for c in cols)

    for i, c in enumerate(cols):
        cx = MARGIN + i * (cw + GUTTER)
        if c.get('style') == 'accent':
            s.append(rect(cx, y, cw, ch, fill=SURFACE))
            s.append(rect(cx, y, 0.055, ch, fill=ACCENT))
        else:
            s.append(rect(cx, y, cw, ch, fill=WHITE, line='D1D5DB'))
        head = c['title']
        arrow = ARROW.get(c.get('arrow', ''), '')
        runs = []
        if arrow:
            runs.append(run(arrow + '   ', COL_HEAD_PT, ACCENT, BODY, bold=True))
        runs.append(run(head, COL_HEAD_PT, ACCENT, BODY, bold=True, spc=120))
        s.append(textbox(cx + pad, y + pad, cw - 2 * pad, COL_HEAD_PT * 1.3 / 72, runs, anchor='ctr'))

        iy = y + pad + COL_HEAD_PT * 1.3 / 72 + 0.30
        rid = icons.get(c.get('icon'))
        for title, body in c['items']:
            th = max(ICON, text_h(title, inner, SUB_TITLE_PT))
            if rid:
                s.append(pic(cx + pad, iy + 0.02, ICON, ICON, rid))
            tx = cx + pad + (ICON + 0.14 if rid else 0)
            s.append(textbox(tx, iy, inner, th, [run(title, SUB_TITLE_PT, INK, BODY, bold=True)], anchor='ctr'))
            bh = text_h(body, inner, SUB_BODY_PT)
            s.append(textbox(tx, iy + th + 0.05, inner, bh, [run(body, SUB_BODY_PT, MUTED, BODY)]))
            iy += th + 0.05 + bh + 0.26
    bottom = y + ch          # real content bottom, excluding the gap below the cards
    y += ch + 0.20

    if sl.get('closer'):
        cht = text_h(sl['closer'], CONTENT_W, CLOSER_PT)
        if y + cht <= FOOTER_Y - 0.12:
            s.append(textbox(MARGIN, y, CONTENT_W, cht,
                             [run(sl['closer'], CLOSER_PT, INK, BODY, italic=True)]))
            bottom = y + cht
        else:
            sl['_dropped_closer'] = True      # never overlap the cards; report instead
    footer(s, label, page, total)
    return s, bottom

def grid_slide(sl, label, page, total):
    s = []
    s.append(textbox(MARGIN, EYEBROW_Y, CONTENT_W, EYEBROW_H,
                     [run(sl['eyebrow'], EYEBROW_PT, ACCENT, BODY, bold=True, spc=200)], anchor='ctr'))
    hh = text_h(sl['headline'], CONTENT_W, HEAD_PT, DISPLAY)
    s.append(textbox(MARGIN, HEAD_Y, CONTENT_W, max(0.45, hh), [run(sl['headline'], HEAD_PT, INK, DISPLAY)]))
    y = HEAD_Y + max(0.45, hh) + 0.14

    if sl.get('lead') and not too_similar(sl['lead'], sl['headline']):
        lh = text_h(sl['lead'], CONTENT_W, LEAD_PT)
        s.append(textbox(MARGIN, y, CONTENT_W, lh, [run(sl['lead'], LEAD_PT, LEAD_COLOR, BODY)]))
        y += lh + 0.26

    for para in sl.get('prose', []):
        ph = text_h(para, CONTENT_W, BLOCK_BODY_PT)
        if y + ph > FOOTER_Y - 0.20:
            break
        s.append(textbox(MARGIN, y, CONTENT_W, ph, [run(para, BLOCK_BODY_PT, MUTED, BODY)]))
        y += ph + 0.16

    blocks, cols = sl['blocks'], sl['cols']
    if blocks:
        cw = (CONTENT_W - GUTTER * (cols - 1)) / cols
        inner = cw - 0.44                                    # card padding l/r
        rows = [blocks[i:i + cols] for i in range(0, len(blocks), cols)]
        for row in rows:
            # one title band and one body band per row, so bodies line up across columns
            th = max(text_h(t, inner, BLOCK_TITLE_PT) for t, _ in row)
            bh = max(text_h(b, inner, BLOCK_BODY_PT) for _, b in row)
            rh = 0.22 + th + 0.08 + bh + 0.24
            for i, (title, body) in enumerate(row):
                bx = MARGIN + i * (cw + GUTTER)
                s.append(rect(bx, y, cw, rh, fill=SURFACE, radius=3000))
                s.append(textbox(bx + 0.22, y + 0.22, inner, th,
                                 [run(title, BLOCK_TITLE_PT, INK, BODY, bold=True)]))
                s.append(textbox(bx + 0.22, y + 0.22 + th + 0.08, inner, bh,
                                 [run(body, BLOCK_BODY_PT, MUTED, BODY)]))
            y += rh + 0.22

    if sl.get('closer'):
        ch = text_h(sl['closer'], CONTENT_W, CLOSER_PT)
        cy = min(y + 0.10, FOOTER_Y - 0.20 - ch)
        s.append(textbox(MARGIN, cy, CONTENT_W, ch, [run(sl['closer'], CLOSER_PT, INK, BODY, italic=True)]))
        y = cy + ch

    footer(s, label, page, total)
    return s, y

# ---------------------------------------------------------------- markdown parsing
DIRECTIVE = re.compile(r'<!--\s*(slide|deck)\s*:\s*(.*?)-->', re.S)

def parse_directive(body):
    out = {}
    for part in body.split('|'):
        if '=' in part:
            k, v = part.split('=', 1)
            out[k.strip()] = ' '.join(v.split())
    return out

def parse(md_path):
    raw = open(md_path, encoding='utf-8').read()
    deck = {}
    m = re.search(r'^#\s+(.+)$', raw, re.M)
    deck['title'] = m.group(1).strip() if m else os.path.basename(md_path)
    dm = re.search(r'<!--\s*deck\s*:\s*(.*?)-->', raw, re.S)
    if dm:
        deck.update(parse_directive(dm.group(1)))

    slides = []
    for sec in re.split(r'^##\s+', raw, flags=re.M)[1:]:
        head, rest = sec.split('\n', 1) if '\n' in sec else (sec, '')
        sm = re.search(r'<!--\s*slide\s*:\s*(.*?)-->', rest, re.S)
        if not sm:
            continue                                  # doc-only section
        d = parse_directive(sm.group(1))
        rest = rest[:sm.start()] + rest[sm.end():]

        # '### Column' blocks turn the slide into the columns layout
        columns, col_trailing = [], []
        if re.search(r'^###\s+', rest, re.M):
            head_part, *col_parts = re.split(r'^###\s+', rest, flags=re.M)
            for cp in col_parts:
                ctitle, crest = (cp.split('\n', 1) + [''])[:2]
                cm = re.search(r'<!--\s*col\s*:\s*(.*?)-->', crest, re.S)
                cd = parse_directive(cm.group(1)) if cm else {}
                if cm:
                    crest = crest[:cm.start()] + crest[cm.end():]
                # bullets may wrap: join continuation lines, but never across a blank line
                crest = re.sub(r'\n[ \t]+(?=\S)', ' ', crest)
                items = []
                for line in re.findall(r'^[ \t]*[-*][ \t]+(.*)$', crest, re.M):
                    im = re.match(r'\*\*(.+?)\*\*\s*(.*)$', line.strip())
                    if im:
                        items.append((im.group(1).rstrip('.').strip(), _clean(im.group(2))))
                    elif line.strip():
                        items.append((_clean(line), ''))
                # prose after the bullets belongs to the slide, not to the column
                for para in re.split(r'\n\s*\n', crest):
                    para = ' '.join(para.split())
                    if para and not re.match(r'[-*]\s', para) and not para.startswith('<!--'):
                        col_trailing.append(_clean(para))
                columns.append({'title': ctitle.strip(), 'items': items,
                                'icon': cd.get('icon'), 'style': cd.get('style', 'plain'),
                                'arrow': cd.get('arrow', '')})
            rest = head_part

        paras = [' '.join(p.split()) for p in re.split(r'\n\s*\n', rest) if p.strip()]

        blocks, pre, post = [], [], []
        for p in paras:
            bm = re.match(r'\*\*(.+?)\*\*\s*(.*)$', p)
            if bm:
                blocks.append((bm.group(1).rstrip('.').strip(), _clean(bm.group(2))))
            elif blocks:
                post.append(_clean(p))
            else:
                pre.append(_clean(p))
        lead   = pre[0] if pre else None
        closer = post[-1] if (blocks and post) else None
        if columns and col_trailing:
            closer = ' '.join(col_trailing)
        # no labelled blocks: the section is flowing prose, so render it as prose
        prose  = ([] if blocks else pre[1:])
        n = len(blocks)
        slides.append({
            'columns':  columns,
            'eyebrow':  d.get('eyebrow', head.strip().upper()),
            'headline': d.get('headline', head.strip()),
            'lead':     None if d.get('lead') == 'none' else lead,
            'blocks':   blocks,
            'prose':    prose,
            'closer':   None if d.get('closer') == 'none' else closer,
            'cols':     int(d['cols']) if 'cols' in d else (3 if n in (3, 6) else 2),
            'label':    d.get('label', deck.get('label', deck['title'])),
        })
    return deck, slides

def _clean(s):
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
    s = re.sub(r'\*(.+?)\*', r'\1', s)
    s = re.sub(r'`(.+?)`', r'\1', s)
    s = re.sub(r'\[(.+?)\]\([^)]*\)', r'\1', s)
    return s.strip()

# ---------------------------------------------------------------- package assembly
TEMPLATE = '06-economics.pptx'
KEEP = re.compile(r'^(ppt/(slideMasters|slideLayouts|theme|notesMasters|media)/|ppt/(presProps|viewProps|tableStyles)\.xml$|docProps/)')

def build(md_path, out_path):
    deck, slides = parse(md_path)
    total = len(slides) + 1
    parts = [SLIDE_TMPL % ''.join(title_slide(deck))]
    warn = []
    slide_icons = {}
    for i, sl in enumerate(slides, 2):
        if sl.get('columns'):
            need = sorted({c['icon'] for c in sl['columns'] if c.get('icon')})
            rids = {nm: 'rId%d' % (2 + k) for k, nm in enumerate(need)}
            slide_icons[i] = rids
            shapes, ybot = columns_slide(sl, sl['label'], i, total, rids)
        else:
            shapes, ybot = grid_slide(sl, sl['label'], i, total)
        if sl.get('_dropped_closer'):
            warn.append('slide %d ("%s"): closing line did not fit and was dropped '
                        '- shorten it, or set closer=none to make that explicit'
                        % (i, sl['eyebrow']))
        elif ybot > FOOTER_Y - 0.10:
            warn.append('slide %d ("%s") content reaches %.2f in, footer at %.2f'
                        % (i, sl['eyebrow'], ybot, FOOTER_Y))
        parts.append(SLIDE_TMPL % ''.join(shapes))

    src = zipfile.ZipFile(TEMPLATE)
    lay = 'ppt/slideLayouts/slideLayout1.xml'
    out = zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED)
    written = []
    def put(n, d):
        out.writestr(n, d if isinstance(d, bytes) else d.encode('utf-8')); written.append(n)

    # which media do the retained master/layout/notesMaster parts actually reference?
    used = set()
    for rp in [n for n in src.namelist() if n.endswith('.rels')
               and re.match(r'ppt/(slideMasters|slideLayouts|notesMasters)/_rels/', n)]:
        owner = rp.replace('/_rels/', '/')[:-5]
        for m in re.finditer(r'Target="([^"]+)"', src.read(rp).decode('utf-8')):
            t = m.group(1)
            if t.startswith('http'):
                continue
            seg = owner.rsplit('/', 1)[0].split('/')
            for q in t.split('/'):
                if q == '..': seg.pop()
                elif q and q != '.': seg.append(q)
            p = '/'.join(seg)
            if p.startswith('ppt/media/'):
                used.add(p)

    for info in src.infolist():
        n = info.filename
        if n.startswith('ppt/media/') and n not in used:
            continue                      # orphaned media makes PowerPoint report corruption
        if KEEP.match(n):
            put(n, src.read(n))

    RT = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
    emitted_media = set()
    for i, xml in enumerate(parts, 1):
        put('ppt/slides/slide%d.xml' % i, xml)
        rels_i = ['<Relationship Id="rId1" Type="%sslideLayout" '
                  'Target="../slideLayouts/slideLayout1.xml"/>' % RT]
        for name, rid in sorted(slide_icons.get(i, {}).items(), key=lambda kv: kv[1]):
            src_png = os.path.join(ICON_DIR, name + '.png')
            if not os.path.exists(src_png):
                raise SystemExit('missing icon: ' + src_png)
            tgt = 'ppt/media/%s.png' % name
            if tgt not in emitted_media:
                put(tgt, open(src_png, 'rb').read())
                emitted_media.add(tgt)
            rels_i.append('<Relationship Id="%s" Type="%simage" Target="../media/%s.png"/>'
                          % (rid, RT, name))
        put('ppt/slides/_rels/slide%d.xml.rels' % i,
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s'
            '</Relationships>' % ''.join(rels_i))

    rels = ['<Relationship Id="rId1" Type="%sslideMaster" Target="slideMasters/slideMaster1.xml"/>' % RT,
            '<Relationship Id="rId2" Type="%snotesMaster" Target="notesMasters/notesMaster1.xml"/>' % RT]
    sldids = []
    for i in range(1, len(parts) + 1):
        rels.append('<Relationship Id="rId%d" Type="%sslide" Target="slides/slide%d.xml"/>' % (i + 2, RT, i))
        sldids.append('<p:sldId id="%d" r:id="rId%d"/>' % (255 + i, i + 2))
    n = len(parts) + 2
    for kind, tgt in [('presProps', 'presProps.xml'), ('viewProps', 'viewProps.xml'),
                      ('theme', 'theme/theme1.xml'), ('tableStyles', 'tableStyles.xml')]:
        n += 1
        rels.append('<Relationship Id="rId%d" Type="%s%s" Target="%s"/>' % (n, RT, kind, tgt))
    put('ppt/_rels/presentation.xml.rels',
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s</Relationships>'
        % ''.join(rels))
    put('ppt/presentation.xml',
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" saveSubsetFonts="1">'
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        '<p:sldIdLst>%s</p:sldIdLst>'
        # must sit directly after sldIdLst: PowerPoint refuses the file otherwise when the
        # notes master and slide master share one theme part
        '<p:notesMasterIdLst><p:notesMasterId r:id="rId2"/></p:notesMasterIdLst>'
        '<p:sldSz cx="9144000" cy="5143500"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>'
        % ''.join(sldids))
    put('_rels/.rels',
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="%sofficeDocument" Target="ppt/presentation.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/'
        'metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="%sextendedProperties" Target="docProps/app.xml"/></Relationships>'
        % (RT, RT))

    CT = {'slides': 'slide', 'slideLayouts': 'slideLayout', 'slideMasters': 'slideMaster',
          'notesSlides': 'notesSlide', 'notesMasters': 'notesMaster'}
    MIME = {'rels': 'application/vnd.openxmlformats-package.relationships+xml', 'xml': 'application/xml',
            'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'gif': 'image/gif',
            'svg': 'image/svg+xml', 'emf': 'image/x-emf', 'wmf': 'image/x-wmf'}
    SINGLE = {'ppt/presentation.xml': 'presentationml.presentation.main',
              'ppt/presProps.xml': 'presentationml.presProps',
              'ppt/viewProps.xml': 'presentationml.viewProps',
              'ppt/tableStyles.xml': 'presentationml.tableStyles'}
    ov = ['<Override PartName="/%s" ContentType="application/vnd.openxmlformats-officedocument.%s+xml"/>' % (k, v)
          for k, v in SINGLE.items() if k in written]
    ov.append('<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>')
    ov.append('<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>')
    exts = {'xml', 'rels'}
    for nn in written:
        if nn.endswith('.rels') or nn in SINGLE or nn.startswith('docProps/'):
            continue
        if nn.startswith('ppt/theme/'):
            ov.append('<Override PartName="/%s" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>' % nn)
        elif nn.startswith('ppt/media/'):
            exts.add(nn.rsplit('.', 1)[1].lower())
        else:
            f = nn.split('/')[1]
            if f in CT:
                ov.append('<Override PartName="/%s" ContentType="application/vnd.openxmlformats-officedocument.presentationml.%s+xml"/>' % (nn, CT[f]))
    put('[Content_Types].xml',
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">%s%s</Types>'
        % (''.join('<Default Extension="%s" ContentType="%s"/>' % (e, MIME.get(e, 'application/octet-stream'))
                   for e in sorted(exts)), ''.join(ov)))
    out.close()
    return len(parts), warn

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('markdown')
    ap.add_argument('-o', '--out')
    a = ap.parse_args()
    outp = a.out or os.path.splitext(a.markdown)[0] + '-generated.pptx'
    n, warn = build(a.markdown, outp)
    print('wrote %s  ->  %d slides' % (outp, n))
    for w in warn:
        print('  WARNING: ' + w)
