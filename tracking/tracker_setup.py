from distutils.core import setup, Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
setup (name = "iou_c",
    version = "0.1",
    ext_modules =  [Extension('tracker',['tracker.pyx'])],
    cmdclass = {'build_ext': build_ext}
    )