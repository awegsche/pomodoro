from stopwatch import Stopwatch
from datetime import timedelta
import time

def test_serde():
    watch = Stopwatch("test1")

    with open("testfile", "w") as testfile:
        testfile.writelines([watch.serialise()])

    with open("testfile", "r") as testfile:
        watches = [Stopwatch.deserialise(line) for line in testfile]

        assert(len(watches) == 1)
        assert(watches[0] == watch)


def test_elapsing():
    TOWAIT = 3
    TOWAIT2 = 2

    watch = Stopwatch("test1")
    time.sleep(TOWAIT)
    watch.pause()

    assert(int(watch.elapsed.total_seconds()) == TOWAIT)

    time.sleep(2)
    watch.cont()
    time.sleep(TOWAIT2)
    watch.pause()

    assert(int(watch.elapsed.total_seconds()) == TOWAIT+TOWAIT2)



def test_notes():
    watch = Stopwatch("test1")
    TESTNOTE = "hello, world"
    watch.note = TESTNOTE

    with open("testfile", "w") as testfile:
        testfile.writelines([watch.serialise()])

    with open("testfile", "r") as testfile:
        watches = [Stopwatch.deserialise(line) for line in testfile]

        assert(len(watches) == 1)
        assert(watches[0].note == TESTNOTE)

