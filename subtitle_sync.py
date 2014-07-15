import sublime_plugin
import sublime

SUB_RE = '\d\d:\d\d:\d\d,\d\d\d'


def find_subtitles(view):
    subs = []
    sel = view.sel()

    for match in view.find_all(SUB_RE):
        if sel.contains(match):
            subs.append(match)

    # sel.clear()
    # sel.add_all(subs)
    return subs


def convert_to_time(sub):
    h, m, s = sub.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s.replace(',', '.'))


def convert_to_string(time):
    h = int(time / 3600)
    m = int((time % 3600) / 60)
    s = time % 60

    return str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + ("%.3f" % s).zfill(6).replace('.', ',')


class SubtitleSyncCommand(sublime_plugin.TextCommand):
    def run(self, edit, delta):
        subs = find_subtitles(self.view)

        for sub in subs:  # self.view.sel():
            time = convert_to_time(self.view.substr(sub))
            time += delta

            if time < 0:
                time = 0

            time = convert_to_string(time)
            self.view.replace(edit, sub, time)
