"""Module to automatically upload modified GPX files from GPS Logger."""

import requests
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

_PATH = '/storage/emulated/0/Android/data/com.mendhak.gpslogger/files'


class GpxHandler(PatternMatchingEventHandler):

    def process(self, event):
        if event.src_path.endswith('.gpx'):
            print('Uploading %s' % event.src_path)
            upload_file(event.src_path)

    def on_modified(self, event):
        self.process(event)


def upload_file(fn):
    try:
        fh = open(fn, 'rb')
    except:
        print('Failed to open file %s' % fn)
        return
    files = {'file': fh}
    try:
        resp = requests.post('http://wheresbrendan.com/upload', files=files)
        print(resp.content)
    except Exception as e:
        print('Exception uploading: %s' % e)


def main():
    observer = Observer()
    observer.schedule(GpxHandler(), path=_PATH)
    observer.start()
    observer.join()


if __name__ == '__main__':
    main()
