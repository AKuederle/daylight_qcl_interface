# -*- coding: utf-8 -*-


class RangeError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class QCL(object):
    """Simple python wrapper for a selection of serial port commands to control a daylight solution tunable QCL.
    """

    from collections import namedtuple
    _control = namedtuple("control", ["wn", "freq", "pw", "startwn", "stopwn", "rate", "cycles", "mode", "pause", "step"])
    _state = namedtuple("state", ["wn", "freq", "pw", "startwn", "stopwn", "rate", "cycles", "mode", "pause", "step", "whours", "scancoun"])
    _query = namedtuple("query", ["wn", "freq", "pw", "startwn", "stopwn", "rate", "cycles", "mode", "pause", "step", "whours", "scancount", "all"])

    def __init__(self, port=0, log=False):
        import serial
        super(QCL, self).__init__()
        self.ser = serial.Serial(port)      # opens the COM1 port to communicate with the laser
        self.ser.baudrate = 115200       # set the baudrate to 115200 to use the right speed to send data over
        self.ser.timeout = 1             # set timeout for port to 1 second
        self.log = log
        self.log_file = []
        self._Range = self._control(wn=(980.04, 1244.99), freq=(1.0, 100.0), pw=(0.04, 0.5), startwn=(980.04, 1244.99), stopwn=(980.04, 1244.99), rate=(1.0, 6.0), cycles=(1.0, 10000.0), mode=(1.0, 4.0), pause=(0.0, 10.0), step=(0.01, 264.95))
        self.Set = self._control(wn=self.set_wn, freq=self.set_freq, pw=self.set_pw, startwn=self.set_startwn, stopwn=self.set_stopwn, rate=self.set_rate, cycles=self.set_cycles, mode=self.set_mode, pause=self.set_pause, step=self.set_step)
        self.Get = self._query(wn=self.get_wn, freq=self.get_freq, pw=self.get_pw, startwn=self.get_startwn, stopwn=self.get_stopwn, rate=self.get_rate, cycles=self.get_cycles,
                               mode=self.get_mode, pause=self.get_pause, step=self.get_step, whours=self.get_whours, scancount=self.get_scancount, all=self.get_all)
        self.Stat = self._state(wn=None, freq=None, pw=None, startwn=None, stopwn=None, rate=None, cycles=None, mode=None, pause=None, step=None, whours=None, scancount=None)
        self.get_all()

    def _log_write(self, string):
        if self.log is True:
            self.log_file.append(str(string))
        else:
            pass

    def get_wn(self):
        """get the current wavenumber."""
        command = ":laser:set?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(13)
        self._log_write(answer)
        rlvalue = float(answer[:-6])
        self.Stat = self.Stat._replace(wn=rlvalue)
        return rlvalue

    def set_wn(self, value):
        """set wavenumber."""
        if float(value) < self._Range.wn[0] or float(value) > self._Range.wn[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":laser:set {}\n".format(str(value))
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_wn()
        return rlvalue

    def get_freq(self):
        """get the current frequency."""
        command = ":pulse:freq?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(10)
        self._log_write(answer)
        rlvalue = float(answer[:-5])
        self.Stat = self.Stat._replace(freq=rlvalue)
        return rlvalue

    def set_freq(self, value):
        """set frequency."""
        if float(value) < self._Range.freq[0] or float(value) > self._Range.freq[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":pulse:freq {}\n".format(value)
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_freq()
        return rlvalue

    def get_pw(self):
        """get the current pulsewidth."""
        command = ":pulse:width?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(10)
        self._log_write(answer)
        rlvalue = float(answer[:-6])
        self.Stat = self.Stat._replace(pw=rlvalue)
        return rlvalue

    def set_pw(self, value):
        """set pulsewidth."""
        if float(value) < self._Range.pw[0] or float(value) > self._Range.pw[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":pulse:width {}\n".format(value)
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_pw()
        return rlvalue

    def get_startwn(self):
        """get the current start wavenumber."""
        command = ":scan:start?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(13)
        self._log_write(answer)
        rlvalue = float(answer[:-6])
        self.Stat = self.Stat._replace(startwn=rlvalue)
        return rlvalue

    def set_startwn(self, value):
        """set start wavenumber."""
        if float(value) < self._Range.startwn[0] or float(value) > self._Range.startwn[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":scan:start {}\n".format(value)
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_startwn()
        return rlvalue

    def get_stopwn(self):
        """get the current stop wavenumber."""
        command = ":scan:stop?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(13)
        self._log_write(answer)
        rlvalue = float(answer[:-6])
        self.Stat = self.Stat._replace(stopwn=rlvalue)
        return rlvalue

    def set_stopwn(self, value):
        """set stop wavenumber."""
        if float(value) < self._Range.stopwn[0] or float(value) > self._Range.stopwn[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":scan:stop {}\n".format(value)
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_stopwn()
        return rlvalue

    def get_rate(self):
        """get the current scanrate."""
        command = ":scan:rate?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(3)
        self._log_write(answer)
        rlvalue = float(answer[:-2])
        self.Stat = self.Stat._replace(rate=rlvalue)
        return rlvalue

    def set_rate(self, value):
        """set scanrate."""
        if float(value) < self._Range.rate[0] or float(value) > self._Range.rate[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":scan:rate {}\n".format(value)
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_rate()
        return rlvalue

    def get_cycles(self):
        """get the number of scans."""
        command = ":scan:cycles?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(20)
        self._log_write(answer)
        rlvalue = float(answer[:-2])
        self.Stat = self.Stat._replace(cycles=rlvalue)
        return rlvalue

    def set_cycles(self, value):
        """set number of scans."""
        if float(value) < self._Range.cycles[0] or float(value) > self._Range.cycles[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":scan:cycles {}\n".format(value)
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_cycles()
        return rlvalue

    def get_mode(self):
        """get the current wavenumber."""
        command = ":scan:mode?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(3)
        self._log_write(answer)
        rlvalue = float(answer[:-2])
        self.Stat = self.Stat._replace(mode=rlvalue)
        return rlvalue

    def set_mode(self, value):
        """set wavenumber."""
        if float(value) < self._Range.mode[0] or float(value) > self._Range.mode[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":scan:mode {}\n".format(str(int(value)))
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_mode()
        return rlvalue

    def get_pause(self):
        """get the current wavenumber."""
        command = ":scan:pause?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(9)
        self._log_write(answer)
        rlvalue = float(answer[:-5])
        self.Stat = self.Stat._replace(pause=rlvalue)
        return rlvalue

    def set_pause(self, value):
        """set wavenumber."""
        if float(value) < self._Range.pause[0] or float(value) > self._Range.pause[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = ":scan:pause {}\n".format(str(value))
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_pause()
        return rlvalue

    def get_step(self):
        """get the current wavenumber."""
        if self.Stat.mode != 1:
            pass
        else:
            command = ":scan:step?\n"
            self._log_write(command)
            self.ser.write(command)
            answer = self.ser.read(9)
            self._log_write(answer)
            rlvalue = float(answer[:-5])
            self.Stat = self.Stat._replace(step=rlvalue)
            return rlvalue

    def set_step(self, value):
        """set stepsize."""
        if self.Stat.mode != 1:
            pass
        else:
            if float(value) < self._Range.step[0] or float(value) > self._Range.step[1]:
                raise RangeError("{} is out of range!".format(str(value)))
            command = ":scan:step {}\n".format(str(value))
            self._log_write(command)
            self.ser.write(command)
            rlvalue = self.get_step()
            return rlvalue

    def get_whours(self):
        """get the working hours."""
        command = ":info:hhrs?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(11)
        self._log_write(answer)
        rlvalue = float(answer[:-5])
        self.Stat = self.Stat._replace(whours=rlvalue)
        return rlvalue

    def get_scancount(self):
        """get the number of scans during a measurment."""
        command = ":scan:count?\n"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(6)
        self._log_write(answer)
        rlvalue = int(answer[:-2])
        self.Stat = self.Stat._replace(scancount=rlvalue)
        return rlvalue

    def scan_start(self):
        """send start command."""
        command = ":scan:run 1\n"
        self._log_write(command)
        self.ser.write(command)

    def scan_stop(self):
        """send stop command."""
        command = ":scan:run 0\n"
        self._log_write(command)
        self.ser.write(command)

    def get_all(self):
        """get the full current laser state."""
        for command in self.Get[:-1]:
            command()
        return self.Stat

    def wait_for_finish(self, interval=3.0, asynchron=False):
        """Give information, when current scans are finished.

        The function query the current scancount every few seconds (defined by the intervall parameter). If no callback_function is provided, a synchrone sleeptimer is used.
        Therefore the script will be blocked until the current scans are finished (indicated by a scancount of 0).
        If a callback_function is provided, a asynchron timer in a different thread is used.
        Furthermore the given callback_function is called with the current scancount as primary parameter,
        as a way of retrieving the scancount.
        Latter must only be used for multithreading applications, such like GUIs, while the synchrone timer is a way to delay the execution of a simple script, until scans have finished
        """
        def asynchron_timer(interval=interval):
            self.scancount = self.get_scancount()
            if self.scancount != 0:
                timer = Timer(interval, asynchron_timer)
                timer.start()
            else:
                pass

        if asynchron is False:
            from time import sleep
            while True:
                self.scancount = self.get_scancount()
                if self.scancount == 0:
                    break
                sleep(interval)

        else:
            from threading import Timer
            asynchron_timer()

    def close(self):
        """close the port."""
        self.ser.close()
