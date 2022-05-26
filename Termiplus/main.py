import collections
import os
import sublime
import sublime_plugin


def open_terminus_view_or_panel(cwd, window, panel):
    panel_name = "Terminus"

    if panel:
        existing_panel = window.find_output_panel(panel_name)
        if existing_panel:
            existing_panel.run_command("terminus_paste_text", {"text": "cd \"{}\"\n".format(cwd)})
            window.run_command("show_panel", {"panel": "output.{}".format(panel_name), "toggle": False})
            window.focus_view(existing_panel)
        else:
            window.run_command("terminus_open", {"cwd": cwd, "panel_name": panel_name})
    else:
        window.run_command("terminus_open", {"cwd": cwd})


class TermiplusOpenCommand(sublime_plugin.WindowCommand):
    def run(self, paths, panel):
        if len(paths) == 0:
            cwd = None
        else:
            cwd = paths[0]
            if not os.path.isdir(cwd):
                cwd = os.path.dirname(cwd)

        open_terminus_view_or_panel(cwd, self.window, panel)


class TermiplusOpenProjectPathCommand(sublime_plugin.WindowCommand):
    paths = []
    panel = True

    def run(self, panel=True):
        self.panel = panel
        self.paths.clear()

        list_items = []

        project_data = self.window.project_data()
        if "termiplus" in project_data:
            termiplus_paths = project_data["termiplus"]["paths"] or {}
            for key, value in termiplus_paths.items():
                self.paths.append(value)
                list_items.append(sublime.QuickPanelItem(key, kind=sublime.KIND_NAVIGATION))

        open_folders = self.window.folders()
        folder_names = {os.path.basename(folder): folder for folder in open_folders}
        for key, value in folder_names.items():
            self.paths.append(value)
            list_items.append(sublime.QuickPanelItem(key, annotation="root folder", kind=sublime.KIND_NAVIGATION))

        self.window.show_quick_panel(list_items, self.on_pick)

    def on_pick(self, item):
        if item == -1:
            return

        path = self.paths[item] or None
        if path is None:
            return

        st_vars = self.window.extract_variables()
        st_folder = st_vars["folder"]

        normalized_path = os.path.normpath(os.path.join(st_folder, path))

        open_terminus_view_or_panel(normalized_path, self.window, self.panel)


class TermiplusAddShortcutCommand(sublime_plugin.WindowCommand):
    folder = None

    def run(self, paths):
        folders = list(set(map(lambda f: f if os.path.isdir(f) else os.path.dirname(f), paths)))
        self.folder = folders[0]

        self.window.show_input_panel(
            "Enter shortcut name",
            os.path.basename(self.folder),
            self.on_done,
            None,
            None
        )

    def on_done(self, shortcut):
        project_data = self.window.project_data()
        st_vars = self.window.extract_variables()
        base_folder = st_vars["folder"]

        if "termiplus" not in project_data:
            project_data["termiplus"] = {"paths": {}}

        if "paths" not in project_data["termiplus"]:
            project_data["termiplus"]["paths"] = {}

        project_data["termiplus"]["paths"][shortcut] = os.path.relpath(self.folder, base_folder)

        self.window.set_project_data(project_data)
