"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).
"""
import pyaudio
import numpy as np
from win10toast import ToastNotifier
import plyer.platforms.win.notification
from plyer import notification
import datetime
import time
import sys



if len(sys.argv) > 1:

    LOWTHRESHOLD = int(sys.argv[1])
    HIGHTHRESHOLD = int(sys.argv[2])

else:
    LOWTHRESHOLD = 40
    HIGHTHRESHOLD = 90


now = datetime.datetime.now()
toaster = ToastNotifier()

CHUNK = 2**11
RATE = 20000

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)
flag = 0
if __name__ == "__main__":

    try:
        while True:
            if now.hour < 8 or now.hour > 18:
                data = np.frombuffer(stream.read(CHUNK),dtype=np.int16)
                peak=np.average(np.abs(data))*2
                print(peak)
                #print("%04d %05d"%(i,peak))
                if peak > LOWTHRESHOLD and peak <= HIGHTHRESHOLD + 10:
                    if flag != 0:
                        flag += 1
                        #print(flag)
                    else:
                        flag = 1
                    #stream.stop_stream()
                    # print(now.year, now.month, now.day, now.hour, now.minute, now.second)
                    # 2015 5 6 8 53 40
                    if flag > 4:
                        #   toaster.show_toast("%dh%s" % (now.hour,now.minute), "Ferme ta ras HMAR",duration = 5)
                        now = datetime.datetime.now()
                        notification.notify("%dh%s" % (now.hour,now.minute), "Ferme ta ras HMAR",timeout=5)
                        time.sleep(6)
                        stream.start_stream()
                        flag = 0
                elif peak > HIGHTHRESHOLD:
                    stream.stop_stream()
                    now = datetime.datetime.now()
                    peak = 0
                    notification.notify("%dh%s" % (now.hour, now.minute), "Ferme ta ras HMAR", timeout=5)
                    time.sleep(6)
                    stream.start_stream()
                    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
                    flag = 0
                else:
                    flag = 0
            else:
                time.sleep(60)
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()