import c2xt
import xtlang
import os

def process_nanovg():
    nanovg_dir = '/Users/ben/Documents/research/extemporelang/nanovg'
    extempore_dir = '/Users/ben/Documents/research/extemporelang/extempore'
    pre_defined_types = {'NVGcolor': '(bind-type NVGcolor <float,float,float,float> "")'}
    opaque_types = ['NVGcontext']

    with open(os.path.join(extempore_dir, 'libs', 'external', 'nanovg.xtm'), 'w') as outfile:
        print(xtlang.output_header('nanovg', 'Ben Swift', 'NanoVG bindings for Extempore'), file=outfile)
        c2xt.process_file(os.path.join(nanovg_dir, 'src', 'xtmnanovg.c'), 'libnanovg', outfile, [], pre_defined_types, opaque_types)
        print(xtlang.output_footer('nanovg', 'libs/external'), file=outfile)
