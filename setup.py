from distutils.core import setup
from distutils.sysconfig import get_python_lib
import py2exe, os

includes = [
    'numpy',
    'wx',
    'wx.*',
    'traits',
    'traitsui',
    'traitsui.editors',
    'traitsui.editors.*',
    'traitsui.wx',
    'traitsui.wx.*',
    'pyface',
    'pyface.*',
    'pyface.wx',
    'pyface.ui.wx',
    'pyface.ui.wx.init',
    'pyface.ui.wx.*',
    'pyface.ui.wx.grid.*',
    'pyface.ui.wx.action.*',
    'pyface.ui.wx.timer.*',
    'pyface.ui.wx.wizard.*',
    'pyface.ui.wx.workbench.*',
    ]

# images needed for GUI need to be stored in the data_files tuple
#dist_image_folder = 'images'
data_folders = [
    'pyface\images',
    'pyface\ui\wx\images',
    'pyface\ui\wx\grid\images',
    'traitsui\image\library',
    ]
data_files = []
for folder in data_folders:
    data_files.append(
        (folder,
         [os.path.join(get_python_lib(), folder, file) for file in
          os.listdir(os.path.join(get_python_lib(), folder))]))

setup(
    windows=['micropoint_logscale_conversion.py'],
    name="Micropoint Power Utility",
    version="1.0",
    description="Andor MicroPoint attenuator power conversion utility",
    author="Pariksheet Nanda",
    author_email="p.nanda@andor.com",
    url="https://github.com/omsai/micropoint-util",
    options={
        "py2exe": {
            "optimize": 0,
            "includes": includes,
            "dll_excludes": ["libzmq.dll", "MSVCP90.dll"],
            "dist_dir": 'dist',
            # bundle-files not yet supported on win64
            #"bundle_files": 2, 
            "xref": False,
            "skip_archive": True,
            "ascii": False,
            "custom_boot_script": '',
            "compressed": False,
            }
        },
    data_files=data_files
    )
