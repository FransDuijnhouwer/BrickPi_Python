# Test program for ThreadSafeBrickPi sensors

import ThreadSafeBrickPi
import threading
import time

BPi = ThreadSafeBrickPi

running = True

class myThreadOne( threading.Thread ):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run( self ):
        time.sleep(1)
        bpc = BPi.BrickPiCom()
        us = bpc.register_sensor(
            "BrickPiLegoUltraSonicSensor",
            "LEGO-Sensors",
            BPi.PORT_1)
        ls = bpc.register_sensor(
            "BrickPiLegoLightSensor",
            "LEGO-Sensors",
            BPi.PORT_2,
            1)
        ss = bpc.register_sensor(
            "BrickPiLegoSoundSensor",
            "LEGO-Sensors",
            BPi.PORT_3)
        tstart = time.time()
        while running:
            bpc.update()
            print("%s: Ultra sonic sensor value  : %d" 
                  % (self.name, us.get_value()))
            print("%s: Light sensor value        : %d" 
                  % (self.name, ls.get_value()))
            print("%s: Sound sensor value        : %d" 
                  % (self.name, ss.get_value()))
            time.sleep(0.6)
            telapsed = time.time() - tstart
            if telapsed > 5:
                tstart = time.time()
                ls.toggle_light()

class myThreadTwo( threading.Thread ):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        time.sleep(1)
        bpc = BPi.BrickPiCom()
        us = bpc.register_sensor(
            "BrickPiLegoUltraSonicSensor",
            "LEGO-Sensors",
            BrickPi.PORT_1)
        cs = bpc.register_sensor(
            "BrickPiLegoColorSensor",
            "LEGO-Sensors",
            BrickPi.PORT_4)
        tstart = time.time()
        while running:
            bpc.update()
            print("%s: Ultra sonic sensor value  : %d"
                  % ( self.name, us.get_value()))
            print("%s: Color sensor color        : %s"
                  % ( self.name, cs.get_color()))
            print("%s: Color sensor value        : %d"
                  % ( self.name, cs.get_value()))
            time.sleep(0.5)
            telapsed = time.time() - tstart
            if telapsed > 5:
                tstart = time.time()
                cs.set_mode((cs.get_mode() + 1) % 5)

thread1 = myThreadOne( 1, "Thread-1" )
thread2 = myThreadTwo( 2, "Thread-2" )

thread1.setDaemon( True )
thread2.setDaemon( True )

thread1.start()
thread2.start()

while True:
  try:
    print "Press enter to quit."
    c = raw_input( "" )
    running = False
    time.sleep(0.2)
    print "Bye"
    break;
  except KeyboardInterrupt:     #Triggered by pressing Ctrl+C
    running = False
    time.sleep(0.2)
    print "Bye"
    break;
time.sleep( 1 )