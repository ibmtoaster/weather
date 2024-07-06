import os
t = os.popen('vcgencmd measure_temp').readline()
print("CPU",t)
t2 = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
print(t2)

from subprocess import PIPE, Popen

def get_cpu_temperature():
    """get cpu temperature using vcgencmd"""
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

def get_cpu_temperature2():
    t = os.popen('vcgencmd measure_temp').readline()
    return float(t[t.index('=') + 1:t.rindex("'")])


if __name__ == '__main__':
 print ("get_cpu_temperature2():",get_cpu_temperature2())