import sublime
import sublime_plugin
from os import walk, path


class E2dincludeCompletions(sublime_plugin.EventListener):

    """Class for e2d include script completions."""

    def on_query_completions(self, view, prefix, locations):
        """Add files on completion if they are e2d files.

        Example in e2d file:

        {
            ...
            myIncludeFile = <filePath/fileNameToInclude.e2d>
            ...
        }

        """

        # Only trigger within E2D
        if not view.match_selector(locations[0],
                                   "source.e2d"):
            return []

        point = locations[0] - len(prefix) - 1
        chars = view.substr(sublime.Region(point - 1, point + 1))
        if chars != '=<' and chars != ' <':
            return []

        completions = list()
        file_dir = path.dirname(view.file_name())

        for root, dirs, files in walk(file_dir):
            for file_ in files:
                if path.splitext(file_)[1] == ".e2d" and \
                        file_ != path.basename(view.file_name()):
                    path_suggestion = root.replace(file_dir, "")
                    completions.append(
                        (
                            "{0}\t.{1}".format(
                                path.splitext(file_)[0], path_suggestion if path_suggestion != "" else "/"),
                            "{0}>".format(path.join(path_suggestion[1:] if path_suggestion != "" and path_suggestion[
                                          0] == "/" else path_suggestion, file_))
                        )
                    )

        return (sorted(completions), sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)


class E2dfilesCompletions(sublime_plugin.EventListener):

    """Class for e2d include script completions."""

    def on_query_completions(self, view, prefix, locations):
        """Add any files on completion when they have to be inserted in the e2d file.

        Example in e2d file:

        {
            ...
            myFile = "filePath/fileNameToInclude.fileExtension"
            ...
        }

        """

        # Only trigger within E2D
        if not view.match_selector(locations[0],
                                   "source.e2d"):
            return []

        point = locations[0] - len(prefix) - 1
        chars = view.substr(sublime.Region(point - 1, point + 1))
        if chars != '="' and chars != ' "':
            return []

        completions = list()
        file_dir = path.dirname(view.file_name())

        for root, dirs, files in walk(file_dir):
            for file_ in files:
                if file_ != path.basename(view.file_name()):
                    path_suggestion = root.replace(file_dir, "")
                    completions.append(
                        (
                            "{0}\t.{1}".format(
                                file_, path_suggestion if path_suggestion != "" else "/"),
                            "{0}".format(path.join(path_suggestion[1:] if path_suggestion != "" and path_suggestion[
                                0] == "/" else path_suggestion, file_))
                        )
                    )

        return (sorted(completions), sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
