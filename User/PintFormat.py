import sublime
import sublime_plugin
import subprocess
import os


class PintFormatCommand(sublime_plugin.EventListener):
    IGNORED_FOLDERS = ["wp", "vendor"]

    def find_closest_config(self, view):
        filename = view.file_name()
        path = view.file_name()
        parent_folder = view.window().folders()[0]

        while path != parent_folder:
            path = os.path.dirname(path)

            config = f"{path}/pint.json"

            if os.path.exists(config):
                return config

        return None

    def on_post_save_async(self, view):
        filename = view.file_name()
        if filename is None or (not filename.endswith('.php') or filename.endswith('.blade.php')):
            return

        for folder in self.IGNORED_FOLDERS:
            if folder in filename:
                print(f"Skipping file {filename} because it's in an ignored folder ('{folder}')")
                return None

        if view.window() is None:
            return

        folder = view.window().folders()[0]

        pint = os.path.normpath(f'{folder}/vendor/bin/pint')
        if not os.path.exists(pint):
            return

        args: list[str] = []

        if os.name == 'nt':
            pint += '.bat'

        args.append(pint)

        pint_conf = self.find_closest_config(view)
        if pint_conf is not None:
            args.append('--config')
            args.append(pint_conf)

        args.append(filename)

        print("Formatting file", filename)

        if os.name == 'nt':
            _ = subprocess.run(args, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            _ = subprocess.run(args)
