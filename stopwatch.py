import datetime

def decode_note(note: str) -> str:
    return note.replace('%komma%', ',')

def sanitise_note(note: str) -> str:
    return note.replace(',', '%komma%')

def format_timedelta(td: datetime.timedelta) -> str:
    hours, remainder = divmod(int(td.total_seconds()), 3600)
    minutes, secs = divmod(remainder, 60)

    return f"{hours:02}:{minutes:02}:{secs:02}"

class Stopwatch():
    def __init__(self, name: str) -> None:
        self.name = name
        self.starttime = datetime.datetime.now()
        self.running: bool = False
        self.elapsed: datetime.timedelta = datetime.timedelta(0)
        self.note: str = ""
        self.archived: bool = False
        self.category: str = "None"

    def __eq__(self, value: object) -> bool:
        return (self.name == value.name and
                self.starttime == value.starttime and
                self.running == value.running and
                self.elapsed == value.elapsed)

    def pause(self):
        self.running = False
        self.elapsed = self.elapsed + (datetime.datetime.now() - self.starttime)

    def get_elapsed(self) -> datetime.timedelta:
        if self.running:
            return self.elapsed + (datetime.datetime.now() - self.starttime)
        else:
            return self.elapsed

    def cont(self):
        if not self.running:
            self.running = True
            self.starttime = datetime.datetime.now()

    def __repr__(self) -> str:
        running = "RUN  " if self.running else "PAUSE"
        return f"{self.name:16} | {format_timedelta(self.get_elapsed())} | {running} | {self.category}"

    def serialise(self) -> str:
        return (f"{self.name}, "
                f"{self.starttime.isoformat()}, "
                f"{self.elapsed}, "
                f"{self.running}, "
                f"{sanitise_note(self.note)}, "
                f"{self.archived}, "
                f"{self.category}"
                )

    @staticmethod
    def deserialise(to_parse: str):
        w = Stopwatch("")
        words = [x.strip() for x in to_parse.split(',')]
        w.name = words[0]
        w.starttime = datetime.datetime.fromisoformat(words[1])
        hms = words[2].split(':')
        w.elapsed = datetime.timedelta(hours=int(hms[0]),
                                          minutes=int(hms[1]),
                                          seconds=float(hms[2]))
        w.running = words[3] == 'True'
        w.note = decode_note(words[4])
        w.archived = words[5] == 'True'

        if len(words) > 6:
            w.category = words[6]

        return w

