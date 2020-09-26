import subprocess
proc=subprocess.Popen("v4l2-ctl --list-devices | grep \"Intel(R) RealSense(TM)\" -A3", shell=True, stdout=subprocess.PIPE,)

output=proc.communicate()[0].decode('utf-8').split("\n")

test = output[-2].replace("\\t","")

print(output[-2][1:])