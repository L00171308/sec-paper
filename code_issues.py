#base needed imports
import subprocess
import requests
import yaml

#risky modules 




# test 1 input eval risk
compute = input('\nYour expression? => ')
if not compute:
    print ("No input")
else:
    print ("Result =", eval(compute))


# test 2 input risk
admin_pass = "admin"
if admin_pass == input("Please enter your password"):
  print ("Password is correct!")
else:
  print ("Password is incorrect!")



# test 3  insecure subprocess call

address = "127.0.0.1"
cmd = "ping -c 1 %s" % address
subprocess.open(cmd, shell=True)


# test 4 py yaml load 

example = '''
person:
name: Joe
age: 99
'''
print(yaml.load(example))

# test 5 unvalidated import of archive 

import tarfile
try:
  tf = tarfile.open('upload.tar.gz')
  tf.extractall('uploads')
except:
   pass