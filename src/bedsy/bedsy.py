import serial
import serial.tools.list_ports
import threading
import queue
from datetime import datetime, timedelta
import time

class Bedsy(threading.Thread):
    def __init__(self, q: queue.Queue, ids: list[str], timeout: float = 0.1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = q
        self.comport = self._get_comport(ids)
        self.SerialObject = serial.Serial(timeout = timeout)
        self.SerialObject.port = self.comport
        self._thread = None

    def _get_comport(self, id_strings: list) -> str:
        devices = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        ports_filtered = [d[0] for d in devices if all(ids in d[2] for ids in id_strings)]
        if not ports_filtered:
            raise IOError("BeDSy not found!")
        if len(ports_filtered) != 1:
            raise IOError("More than 1 matching device found!")
        return ports_filtered[0]

    def start_bedsy(self, send_stop_on_open=True):
        self.SerialObject.open()
        self.SerialObject.reset_input_buffer()
        if send_stop_on_open:
            msg = None
            self.SerialObject.write(bytes("x", encoding="utf-8"))
            ts = datetime.now()
            while not msg and ((datetime.now()-ts) < timedelta(seconds=30)):
                msg = self.SerialObject.readline()
                msg = msg.decode("utf-8").rstrip()
                if "[STOP_PERMANENT]" in msg:
                    break
                msg = None
            if not msg:
                raise IOError("No response from BeDSy (couldn't perform initial stop) for 30 seconds.")
        self.SerialObject.reset_input_buffer()
        self.running = True
        self._thread = threading.Thread(target=self._read_bedsy, args=())
        self._thread.stop_flag = False
        self._thread.start()

    def _read_bedsy(self):
        self.SerialObject.write(bytes("s", encoding="utf-8"))
        t = threading.currentThread()
        internal_running_flag = True
        # this serves as a one-shot flag of when the stop message was received
        stop_timer = None
        while internal_running_flag:
            msg = None
            while not msg:
                msg = self.SerialObject.readline()
                msg = msg.decode("utf-8").rstrip()
                #print(msg)
                if getattr(t, "stop_flag"):
                    if not stop_timer:
                        # if we got the stop flag, and it's None, send the stop command and
                        # log the time for the timeout. this block then won't be executed again
                        self.SerialObject.write(bytes("x", encoding="utf-8"))
                        stop_timer = datetime.now()
                    else:
                        if "[STOP_PERMANENT]" in msg:
                            internal_running_flag = False
                        elif (datetime.now()-stop_timer) > timedelta(seconds=30):
                            raise IOError("Tried to stop BeDSy, but didn't receive response after 30 seconds.")
                time.sleep(0)
            self.q.put((datetime.now().isoformat(), msg))

    def stop_bedsy(self):
        self._thread.stop_flag = True
        self._thread.join()
        self.SerialObject.close()
        self.running = False

if __name__=="__main__":
    q = queue.Queue()
    bedsy = Bedsy(q, ["VID:PID=16C0:0483", "SER=13567420"]) # teensy 4.0
    #bedsy = Bedsy(q, ["VID:PID=16C0:0483", "SER=14487510"]) # teensy 4.1
    bedsy.start_bedsy()
    while True:
        try:
            msg = q.get()
            print(msg)
            time.sleep(100)
        except KeyboardInterrupt:
            bedsy.stop_bedsy()
            break
