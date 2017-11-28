import c2xt
import xtlang
import os

def process_nanovg():
    nanovg_dir = '/Users/ben/Documents/research/extemporelang/nanovg'
    extempore_dir = '/Users/ben/Documents/research/extemporelang/extempore'
    pre_defined_types = {'NVGcolor': '(bind-type NVGcolor <float,float,float,float> "")'}
    opaque_types = ['NVGcontext', 'GLNVGcontext', 'GLNVGfragUniforms']

    with open(os.path.join(extempore_dir, 'libs', 'external', 'nanovg.xtm'), 'w') as outfile:
        print(xtlang.output_header('nanovg', 'Ben Swift', 'NanoVG bindings for Extempore', ['libs/external/gl.xtm']), file=outfile)
        c2xt.process_file(os.path.join(nanovg_dir, 'src', 'xtmnanovg.c'), 'libnanovg', outfile, [], pre_defined_types, opaque_types)
        print(xtlang.output_footer('nanovg', 'libs/external'), file=outfile)


def process_stb_image():
    nanovg_dir = '/Users/ben/Documents/research/extemporelang/stb'
    extempore_dir = '/Users/ben/Documents/research/extemporelang/extempore'

    with open(os.path.join(extempore_dir, 'libs', 'external', 'stb_image.xtm'), 'w') as outfile:
        print(xtlang.output_header('stb_image', 'Ben Swift', 'Sean T. Barrett\'s image library bindings for Extempore', []), file=outfile)
        c2xt.process_file(os.path.join(nanovg_dir, 'stb_image.h'), 'libstb_image', outfile, ['STBI_FAILURE_USERMSG'], {}, [])
        c2xt.process_file(os.path.join(nanovg_dir, 'stb_image_resize.h'), 'libstb_image', outfile, ['STBI_FAILURE_USERMSG'], {}, [])
        c2xt.process_file(os.path.join(nanovg_dir, 'stb_image_write.h'), 'libstb_image', outfile, ['STBI_FAILURE_USERMSG'], {}, [])
        print(xtlang.output_footer('stb_image', 'libs/external'), file=outfile)