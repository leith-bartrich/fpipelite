import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "fiepipelite",
    version = "0.1.0.dev1",
    author= "Bradley Friedman",
    author_email = "brad@fie.us",
    description = ("A lighter approach to pipeline from fiellc"),
    license = "MIT",
    keywords = "pipeline,workflow,fie,desktop",
    url = "http://www.fie.us",
    py_modules=["fiepipelite"],
    packages = find_packages(),

    install_requires=["pytest","atomicfile","rx"],
    entry_points={
#        'fiepipe.plugin.shell.gitlabserver.shell.v1' : [
#            'container = fiepipedesktoplib.container.shells.gitlabserver:FIEPipeShellPlugin',
#            'registered_entity = fiepipelib.legalentity.registry.shell.gitlabserver:FIEPipeShellPlugin',
#        ],
        'console_scripts': [
            'fpipelite = fpipelite.cli.fpipelite:main',
            'fpipelite.project.print = fpipelite.cli.projects:print_project_data',
            'fpipelite.project.new = fpipelite.cli.projects:new_project',
        ],
 #       'fiepipe.plugin.shell.gitasset.v1': [
 #           'watchfolders = fiepipedesktoplib.watchfolder.shell.watchfolder:git_asset_shell_plugin',
 #       ],

    },
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        ],
)