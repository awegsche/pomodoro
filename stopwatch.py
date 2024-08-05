import datetime

def decode_note(note: str) -> str:
    return note.replace('%komma%', ',')

def sanitise_note(note: str) -> str:
    return note.replace(',', '%komma%')

class Stopwatch():
    def __init__(self, name: str) -> None:
        self.name = name
        self.starttime = datetime.datetime.now()
        self.running = True
        self.elapsed: datetime.timedelta = datetime.timedelta(0)
        self.note: str = ""

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
        self.running = True
        self.starttime = datetime.datetime.now()

    def __repr__(self) -> str:
        hours, remainder = divmod(int(self.get_elapsed().total_seconds()), 3600)
        minutes, secs = divmod(remainder, 60)
        return f"{self.name:16} | {hours:02}:{minutes:02}:{secs:02} | {self.running}"

    def serialise(self) -> str:
        return f"{self.name}, {self.starttime.isoformat()}, {self.elapsed}, {self.running}, {sanitise_note(self.note)}"

    @staticmethod
    def deserialise(to_parse: str):
        w = Stopwatch("")
        words = to_parse.split(',')
        w.name = words[0].strip()
        w.starttime = datetime.datetime.fromisoformat(words[1].strip())
        hms = words[2].split(':')
        w.elapsed = datetime.timedelta(hours=int(hms[0]),
                                          minutes=int(hms[1]),
                                          seconds=float(hms[2]))
        w.running = words[3].strip() == 'True'
        w.note = decode_note(words[4].strip())

        return w

