from pipeline.compilers import CompilerBase
from django.utils.encoding import smart_str
from django.conf import settings

from django_pyscss.scss import Scss, DjangoScss, config as scss_config
import os
import fnmatch
from django.contrib.staticfiles import finders


def finder(glob):
    for finder in finders.get_finders():
        for path, storage in finder.list([]):
            if fnmatch.fnmatchcase(path, glob):
                yield path, storage

scss_config.STATIC_ROOT = finder
scss_config.STATIC_URL = settings.STATIC_URL

scss_config.ASSETS_ROOT = os.path.join(settings.MEDIA_ROOT, 'assets/')
scss_config.ASSETS_URL = settings.MEDIA_URL + 'assets/'


def add_to_scss_path(path):
    load_paths = scss_config.LOAD_PATHS.split(
        ',')  # split it up so we can a path check.
    if path not in load_paths:
        load_paths.append(path)
        scss_config.LOAD_PATHS = ','.join(load_paths)


class CompassCompiler(CompilerBase):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith(('.scss', '.sass'))

    def compile_file(self, content, path, force=False, outdated=False):
        add_to_scss_path(os.path.dirname(
            path))  # add the current path of the parsed
                    # file to enable the local @import
        if force or outdated:
            caller = Scss if settings.DEBUG else DjangoScss
            self.save_file(path, caller(scss_opts={
                'compress': False,
                'debug_info': settings.DEBUG,
            }).compile(None, content))

    def save_file(self, path, content):
        return open(path, 'w').write(smart_str(content))

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scss_path = os.path.join(root, 'static', 'styles', 'compass')
add_to_scss_path(scss_path)
