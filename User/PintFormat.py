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

        pint = os.path.normpath(f'{folder}/vendor/bin/pint')
        if not os.path.exists(pint):
            return

        args = []

        if os.name == 'nt':
            pint += '.bat'

        args.append(pint)

        pint_conf = os.path.normpath(f'{folder}/pint.json')
        if os.path.exists(pint_conf):
            args.append('--config')
            args.append(pint_conf)

        args.append(filename)

        print("Formatting file", filename)

        if os.name == 'nt':
            subprocess.run(args, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.run(args)
