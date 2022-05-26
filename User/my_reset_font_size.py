import sublime
import sublime_plugin


class MyResetFontSize(sublime_plugin.ApplicationCommand):
    def run(self, *args):
        s = sublime.load_settings("Preferences.sublime-settings")

        s.set('font_size', 12)

        sublime.save_settings("Preferences.sublime-settings")
