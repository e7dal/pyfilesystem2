from __future__ import unicode_literals

import os

from six import PY2

from .base import original, Patch
from .translate_errors import raise_os
from .. import errors


class PatchOS(Patch):
    def get_module(self):
        import os
        return os

    @Patch.method()
    def chdir(self, path):
        if not self.is_patched:
            return original(chdir(path))
        with raise_os():
            return self._chdir(path)

    @Patch.method()
    def getcwd(self):
        if not self.is_patched:
            return original(getcwd)()
        return self.os_cwd

    @Patch.method()
    def listdir(self, path):
        if not self.is_patched:
            return original(listdir)(path)
        _path = self.from_cwd(path)
        with raise_os():
            dirlist = self.fs.listdir(_path)
        return dirlist