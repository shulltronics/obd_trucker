import serial

class Elm327:    

    def __init__(self):
        self.s = None
    
    def init(self):
        if self.connect():
            # turn off local echo
            self.s.write(b'ate0\r')
            r1 = self.get_response()
            # turn on carraige return for responses
            self.s.write(b'atl1\r')
            r2 = self.get_response()
            # auto detect protocol
            self.s.write(b'atsp1\r')
            r3 = self.get_response()
            self.s.write(b'atst10\r')
            r4 = self.get_response()
            return True
        else:
            return False

    def connect(self):
        try:
            self.s = serial.Serial('/dev/ttyUSB0',
                                   9600,
                                   timeout=0.1,
                                   bytesize = serial.EIGHTBITS,
                                   parity = serial.PARITY_NONE,
                                   stopbits = serial.STOPBITS_ONE
                                  )
            return True
        except serial.SerialException:
            return False

    def is_connected(self):
        if self.s:
            return True
        else:
            return False

    def get_response(self):
        resp = ''
        while True:
            c = self.s.read()
            if c == b'>':
                break
            elif c == b'\r' or c == b'\n':
                resp += "\n"
            else:
                resp += c.decode()
        return resp.strip()
            
    def reset(self):
        if self.is_connected():
            self.s.timeout = 3
            self.s.write(b'atz\r')
            r = self.get_response()
            self.s.timeout = 0.1
            return r
        else:
            return ""

    def set_header(self, bytestring):
        self.s.write(b'atsh' + bytestring + b'\r')
        return self.get_response()

    def request_voltage(self):
        self.s.write(b'atrv\r')
        return self.get_response()
        
    # pid is an integer
    def request_pid(self, pid):
        pid = hex(pid)
        pid_bytes = [pid[2:4], pid[4:6], pid[6:]]
        self.s.timeout = 0.1
        self.s.write(pid[2:].encode() + b'\r')
        resp = self.get_response()
        resp_bytes = resp.split()
        if (resp_bytes[0] == '62'): 
            return resp[9:]
        else:
            return "Error"
