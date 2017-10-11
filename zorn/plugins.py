import os
import shutil

from zorn import Plugin


class StaticFilesMoverPlugin(Plugin):
    def run(self):
        for dir in self.get_setting('STATIC_DIRS'):
            full_dir = os.path.join(self.settings.OUTPUT_DIR, dir)
            if os.path.exists(full_dir):
                shutil.rmtree(full_dir)
            shutil.copytree(os.path.join(self.settings.ROOT_DIR, dir), full_dir)
