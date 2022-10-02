import time, json, pathlib, converter, os 
from contextlib import contextmanager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Monitor:

    def __init__(self, monitorLocation, observer):
        self.observer = observer
        self.datadir = monitorLocation
    
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.datadir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    def on_any_event(self, event):
        if event.is_directory or pathlib.Path(event.src_path).suffix not in [".m3u",".m3u8"]:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print ("Copying music from new playlist file - %s." % event.src_path)
            with observer.ignore_events():
                oldsize = -1
                while (oldsize != os.path.getsize(event.src_path)):
                    oldsize = os.path.getsize(event.src_path)
                    time.sleep(1)
                converter.convert(event.src_path)
                converter.copy(event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print ("Received modified event - %s" % event.src_path)


class PausingObserver(Observer):
    def dispatch_events(self, *args, **kwargs):
        if not getattr(self, '_is_paused', False):
            super(PausingObserver, self).dispatch_events(*args, **kwargs)

    def pause(self):
        self._is_paused = True

    def resume(self):
        time.sleep(self.timeout)
        self.event_queue.queue.clear()
        self._is_paused = False

    @contextmanager
    def ignore_events(self):
        self.pause()
        yield
        self.resume()


if __name__ == '__main__':
    try:
        with open("data.json","r") as datafile:
            confdat = json.load(datafile)
            datadir = confdat["playlistsource"]
    except:
        print("Data file not initialized or misconfigured, quitting")
        quit(1)
    observer = PausingObserver()
    w = Monitor(datadir, observer)
    w.run()
