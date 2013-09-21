import sublime, sublime_plugin
from os import walk

FILE_DIR = lambda s: str("\\".join(s.split("\\")[:-1])) + "\\"
GET_EXT = lambda s: s.split(".")[-1]
FILE_NAME = lambda s: ".".join(s.split(".")[:-1])

def get_path(base, path):
    string = path.replace("%s" % base, "")
    string = string.replace("\\", "/")
    return string

def get_final_path(path, file_):
    path += "/" + file_
    return path

class E2dincludeCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within E2D
        if not view.match_selector(locations[0],
                "source.e2d"):
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch != '<':
            return []

        completions = list()
        file_dir = FILE_DIR(view.file_name())
        for root, dirs, files in walk(file_dir):
            if root != file_dir:
                for file_ in files:
                    if GET_EXT(file_) == "e2d":
                        path = get_path(file_dir, root)
                        completions.append(
                            (
                                "%s\t%s" % (file_, path), 
                                "%s>" % get_final_path(path, file_)
                            )
                        )

        return (sorted(completions), sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

class E2dfilesCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within E2D
        if not view.match_selector(locations[0],
                "source.e2d"):
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch != '=':
            return []

        completions = list()
        file_dir = FILE_DIR(view.file_name())
        for root, dirs, files in walk(file_dir):
            if root != file_dir:
                for file_ in files:
                    path = get_path(file_dir, root)
                    completions.append(
                        (
                            "%s\t%s" % (file_, path), 
                            "\"%s\"" % get_final_path(path, file_)
                        )
                    )

        return (sorted(completions), sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)