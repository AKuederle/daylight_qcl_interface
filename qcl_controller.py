
class RangeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class QCL(object):
    """docstring for QCL"""
    _wn_range = (980.04, 1244.99)
    _freq_range = (1.0, 100.0)
    _pw_range = (0.04, 0.5)
    _startwn_range = (980.04, 1244.99)
    _stopwn_range = (980.04, 1244.99)
    _rate_range = (1.0, 6.0)
    _scan_range = (1, 10000)

    def __init__(self, port=0, log=False):
        import serial
        super(QCL, self).__init__()
        self.ser = serial.Serial(port)      # opens the COM1 port to communicate with the laser
        self.ser.baudrate = 115200       # set the baudrate to 115200 to use the right speed to send data over
        self.ser.timeout = 1             # set timeout for port to 1 second
        self.log = log
        self.log_file = []
        self.get_all()

    def _log_write(self, string):
        if self.log is True:
            self.log_file.append(str(string))
        else:
            pass

    def get_wn(self):
        """get the current wavenumber"""
        command = ":laser:set?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(13)
        self._log_write(answer)
        return answer[:-6]

    def set_wn(self, value):
        """set wavenumber"""
        if float(value) < self._wn_range[0] or float(value) > self._wn_range[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":laser:set {}\n".format(str(value))
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_wn()
        return rlvalue

    def get_freq(self):
        """get the current frequency"""
        command = ":pulse:freq?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(10)
        self._log_write(answer)
        return answer[:-5]

    def set_freq(self, value):
        """set frequency"""
        if float(value) < self._freq_range[0] or float(value) > self._freq_range[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":pulse:freq {}\n".format(value)
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_freq()
        return rlvalue

    def get_pw(self):
        """get the current pulsewidth"""
        command = ":pulse:width?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(10)
        self._log_write(answer)
        return answer[:-6]

    def set_pw(self, value):
        """set pulsewidth"""
        if float(value) < self._pw_range[0] or float(value) > self._pw_range[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":pulse:width {}\n".format(value)
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_pw()
        return rlvalue

    def get_startwn(self):
        """get the current start wavenumber"""
        command = ":scan:start?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(13)
        self._log_write(answer)
        return answer[:-6]

    def set_startwn(self, value):
        """set start wavenumber"""
        if float(value) < self._stopwn_range[0] or float(value) > self._stopwn_range[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":scan:stop {}\n".format(value)
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_startwn()
        return rlvalue

    def get_stopwn(self):
        """get the current stop wavenumber"""
        command = ":scan:stop?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(13)
        self._log_write(answer)
        return answer[:-6]

    def set_stopwn(self, value):
        """set stop wavenumber"""
        if float(value) < self._stopwn_range[0] or float(value) > self._stopwn_range[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":scan:stop {}\n".format(value)
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_stopwn()
        return rlvalue

    def get_rate(self):
        """get the current scanrate"""
        command = ":scan:rate?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(3)
        self._log_write(answer)
        return answer[:-2]

    def set_rate(self, value):
        """set scanrate"""
        if float(value) < self._rate_range[0] or float(value) > self._rate_range[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":scan:rate {}\n".format(value)
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_rate()
        return rlvalue

    def get_scans(self):
        """get the number of scans"""
        command = ":scan:cycles?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(20)
        self._log_write(answer)
        return answer[:-2]

    def set_scans(self, value):
        """set number of scans"""
        if float(value) < self._scan_range[0] or float(value) > self._scan_range[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":scan:cycles {}\n".format(value)
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_scans()
        return rlvalue

    def get_whours(self):
        """get the working hours"""
        command = ":info:hhrs?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(11)
        self._log_write(answer)
        return answer[:-5]

    def get_scancount(self):
        """get the number of scans during a measurment"""
        command = ":scan:count?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(6)
        self._log_write(answer)
        return answer[:-2]

    def scan_start(self):
        """send start command"""
        command = ":scan:run 1\n"
        self._log_write(command)
        self.ser.write(command)

    def scan_stop(self):
        """send stop command"""
        command = ":scan:run 0\n"
        self._log_write(command)
        self.ser.write(command)

    def get_all(self):
        all_stats = []
        all_stats.append(self.get_wn())
        all_stats.append(self.get_freq())
        all_stats.append(self.get_pw())
        all_stats.append(self.get_startwn())
        all_stats.append(self.get_stopwn())
        all_stats.append(self.get_rate())
        all_stats.append(self.get_scans())
        return all_stats
