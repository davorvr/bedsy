import serial
import serial.tools.list_ports
import threading
import queue
from datetime import datetime
import time

class Bedsy(threading.Thread):
    def __init__(self, q: queue.Queue, ids: list[str], timeout: float = 0.1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = q
        self.comport = self._get_comport(ids)
        self.SerialObject = serial.Serial(timeout = timeout)
        self.SerialObject.port = self.comport
        self._running = False

    def _get_comport(self, id_strings: list) -> str:
        devices = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        ports_filtered = [d[0] for d in devices if any(ids in d[2] for ids in id_strings)]
        if not ports_filtered:
            raise IOError("BeDSy not found!")
        if len(ports_filtered) != 1:
            raise IOError("More than 1 matching device found!")
        return ports_filtered[0]

    def start_bedsy(self, flush_on_open=True):
        self.SerialObject.open()
        if flush_on_open:
            self.SerialObject.reset_input_buffer()
        self._running = True
        self.start()

    def run(self):
        self.SerialObject.write(bytes("s", encoding="utf-8"))
        while self._running:
            msg = None
            while not msg:
                msg = self.SerialObject.readline()
                msg = msg.decode("utf-8").rstrip()
                #print(msg)
                if not self._running:
                    return
            self.q.put((datetime.now().isoformat(), msg))

    def stop_bedsy(self):
        self.SerialObject.write(bytes("x", encoding="utf-8"))
        time.sleep(1)
        self._running = False
        time.sleep(0.1)
        self.SerialObject.close()

if __name__=="__main__":
    q = queue.Queue()
    bedsy = Bedsy(q, ["VID:PID=16C0:0483", "SER=13567420"])
    bedsy.start_bedsy()
    while True:
        try:
            msg = q.get()
            print(msg)
            time.sleep(100)
        except KeyboardInterrupt:
            bedsy.stop_bedsy()
            break
