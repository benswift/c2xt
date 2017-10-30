import site
site.addsitedir("/usr/local/opt/llvm/lib/python2.7/site-packages/")
import clang.cindex as clang
clang.Config.set_library_path("/usr/local/opt/llvm/lib/")
