import sublime
import sublime_plugin
import subprocess
import os


class PintFormatCommand(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        filename = view.file_name()
        if filename is None or (not filename.endswith('.php') or filename.endswith('.blade.php')):
            return

        if view.window() is None:
            return

        folder = view.window().folders()[0]

        pint = f'{folder}/vendor/bin/pint'

        if not os.path.exists(pint):
            return

        print("Formatting file", filename)

        subprocess.run([pint, filename])
