# -*- coding: utf-8 -*-
"""Render a .pptx to PNGs via the PowerPoint COM interface.

Copies the deck to a scratch dir first so it never contends with a file the
user has open, and strips mark-of-the-web so Protected View doesn't block it.

    python render.py <deck.pptx> <outdir> [slide numbers...]
"""
import os, sys, glob, shutil, time
import win32com.client

SCRATCH = r'C:\Users\EdTice\AppData\Local\Temp\claude\C--Data-ssdlc-mythos\faa80074-4532-4aeb-8445-277c7240f75f\scratchpad\render_tmp'

def render(src, outdir, only=None, width=1600):
    os.makedirs(SCRATCH, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    for f in glob.glob(os.path.join(outdir, '*.png')):
        os.remove(f)

    work = os.path.join(SCRATCH, os.path.basename(src))
    shutil.copy2(src, work)
    for z in (work + ':Zone.Identifier',):          # clear mark-of-the-web if present
        try: os.remove(z)
        except OSError: pass

    # PowerPoint is single-instance: DispatchEx does NOT get a private process, it
    # returns whatever POWERPNT.EXE is already running - possibly the user's session.
    # So this script must never call app.Quit(); it only closes the presentation it
    # opened and leaves the application alone.
    app = win32com.client.DispatchEx('PowerPoint.Application')
    pres = app.Presentations.Open(os.path.abspath(work), ReadOnly=True,
                                  Untitled=False, WithWindow=False)
    try:
        h = int(width * pres.PageSetup.SlideHeight / pres.PageSetup.SlideWidth)
        n = pres.Slides.Count
        targets = only or range(1, n + 1)
        for i in targets:
            out = os.path.abspath(os.path.join(outdir, 'slide-%02d.png' % i))
            pres.Slides(i).Export(out, 'PNG', width, h)
        print('rendered %d of %d slides -> %s  (%dx%d)'
              % (len(list(targets)), n, outdir, width, h))
    finally:
        try:
            pres.Close()            # close only our presentation; never Quit the app
        except Exception:
            pass
        del app

if __name__ == '__main__':
    src, outdir = sys.argv[1], sys.argv[2]
    only = [int(a) for a in sys.argv[3:]] or None
    render(src, outdir, only)
