import site
import os

LLVM_LIB_PATH = '/usr/local/opt/llvm/lib'
site.addsitedir(os.path.join(LLVM_LIB_PATH, 'python2.7', 'site-packages'))

try:
    import clang.cindex as clang
    clang.Config.set_library_path(LLVM_LIB_PATH)
except ImportError:
    print('Error: could not find LLVM python bindings')
    raise
