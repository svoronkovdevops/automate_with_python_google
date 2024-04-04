# Google IT Automation with Python Professional Certificate - My notes


## Content


[OS with python](#os-with-python)

[debug and throubleshot](#debug-and-throubleshot)

[Configuration management](#configuration-management)

[Automating tasks](#automating-tasks)

## Practical tasks [link to folder](practicals)




## What should be automated

`time_to_automate<(time_perform*amount_times_done)`

[Content](#content)

## OS with python

os
shutil - --module that provides a higher-level interface for file operations

```python
du= shutil.disk_usage("/")
du.free/du.total*100

```


psutil --cpu usage

```python
psutil.cpu_percent(1)

```


csv - work with csv files
 
re - regex

```python
os.path.abspath("file.txt") #abs path to file
os.getcwd()   #cur path
os.environ.get("HOME", "")

```



sys - module provides access to some variables used or maintained 
by the interpreter and to functions that interact with the interpreter
sys.argc  -command-line arguments passed to the script
sys.stdout: Standard output stream (usually the console).
sys.stderr: Standard error output stream (usually the console).
sys.exit()  # Exits the program with status code 0
sys.exit(1)  # Exits the program with status code 1

subprocess -module allows you to spawn new processes, 
connect to their input/output/error pipes, and obtain their return codes


### files in os

In linux and MacOs the portions of a file split by (/)
on windows split using (\)

-------------this code work for all OS--------

```python
dir=os.listdir("website") # show what inside
for name in dir:
   fullname=os.path.join("website", name)
   if os.path.isdir(fullname):
     print("{} is a directory".format(fullname))
   else:
     print("{} is a file".format(fullname))

```




### find in log process id


```python
import re

log="July 31 07:51:40 mycomputer bad_process[12345]: ERROR Performing package upgrade"
regex=r"\[\d+)\]"
result=re.search(regex,log)
print(result[1]) 

```

### Loops

```python
for i in range(10):
    print('Hello world!')

```


```sh
for i in {1..10}; do
    echo "Hello world!"
done

```


```bat
for ($i=1; $i -le 10; $i++) {
    Write-Host "Hello world!"
}

```

### Python script in different OS


1)create file hello.py:

```python
#!/usr/bin/env python3
print("Hello world!")

```

2)then in linux:
`chmod +x hello.py`

3) run:
 `./hello.py`

4) windows run cmd and navigate to folder with file
then run: `python hello.py`


[Content](#content)

## debug and throubleshot


`strace -o failure.strace ./purplebox.py`

then read

`less failure.strace`

### Logs

#### Linux:

/var/log/syslog
.xsession-errors

#### MacOS:

/Library/logs

#### Windows:

Event Viever

### tools

ltrace 

tools are used to analyze network traffic to isolate problems:

tcpdump
wireshark


### Find where is broken part of csv file(binary search)


wc -l contacts.csv --show amount of lines in file

we can find what breken by use parts of file

head -50 contacts.csv | ./import.py --server test

if fail we split this part

head -50 contacts.csv | head -25| ./import.py --server test

if suceed we use other part

head -50 contacts.csv | tail -25| ./import.py --server test

if error we split 

head -50 contacts.csv | tail -25| head -13| ./import.py --server test

if succeed check other part

head -50 contacts.csv | tail -25| tail -12| head -6| ./import.py --server test

if error we find 6 entries

head -50 contacts.csv | tail -25| tail -12| head -6| head -3| ./import.py --server test

we can look at them

head -50 contacts.csv | tail -25| tail -12| head -6| head -3|

and we can edit file


### slow execution



### Check equipment and network

Linux:

iotop - disk
top -process
iftop - netw

MacOS:

Activity monitor

Windows:

Resource monitor
Performance monitor


### check server response time

ab -n 500 site.example.com/

then if response time too big we can connect to the server and check resources

if we see in top that ffmpeg use too much processor time we can decrease its priority 

for pid in $(pidof ffmpeg); do renice 19 $pid; done ******make lower priority for processes ffmpeg

if doesn't help we can find process

ps ax | less ***and then find process 
/ffmpeg
here you can find info abot files that processed by program
locate static/001.webm
t
hen we can navigate to that directory

cd /srv/dep_vid/static
ls -l

then we can find script

grep ffmpeg *

then we can inspect file (use demonize to run separate processes and delete part)

killall -STOP ffmpeg ** sends stop signal but doesn't end processes

for pid in $(pidoff ffmpeg); do while kill -CONT $pid; do sleep 1; done; done


### Good code 

cProfiler ** profiler for python

use right data structures

check time for 1 user and more

time ./send_rem.py "2020-01-13|Example|test1"

time ./send_rem.py "2020-01-13|Example|test1,test2,test3"

pprofile -f callgrind -o profile.out ./send_rem.py "2020-01-13|Example|test1,test2,test3"

kcachegrind profile.out

then based on calls amount check most used code

Adding threads:

```python

executor=futures.ThreadPoolExecutor()
#
executor.submit(method_name,params)

```



#### rsync

rsync(remote sync) is a utility for efficiently 
transferring and synchronizing files between a 
computer and an external hard drive and across 
networked computers

rsync [Options] [Source-Files-Dir] [Destination]

Copy or sync files locally:
rsync -zvh [Source-Files-Dir] [Destination]

Copy or sync directory locally:
rsync -zavh [Source-Files-Dir] [Destination]

Copy files and directories recursively locally:
rsync -zrvh [Source-Files-Dir] [Destination]

-----
dailysync.py

```python

#!/usr/bin/env python3

from multiprocessing import Pool
import multiprocessing
import subprocess
import os
home_path = os.path.expanduser('~')
src = home_path + "/data/prod"
dest = home_path + "/data/prod_backup/"
if __name__ == "__main__":
    pool = Pool(multiprocessing.cpu_count())
    pool.apply(subprocess.call, args=(["rsync", "-arq", src, dest],))

```



/multisync.py
```python

#!/usr/bin/env python3
from multiprocessing import Pool
import multiprocessing
import subprocess
import os
src = "/data/prod"
dest = "/data/prod_backup/"

if __name__ == "__main__":
    pool = Pool(multiprocessing.cpu_count())
    pool.apply(subprocess.call, args=(["rsync", "-arq", src, dest],))

```   



### crash app

Linux:

strace

MacOS:

dtruss

Windows:

Process monitor

To find the root cause of a crashing app,
we'll want to look at all logs, figure out
what changed, trace the system or library
calls the program makes, and create the 
smallest possible reproduction case.

If program crashes on new OS or different environment
you can containerize it

Watchdog - process checks a program is running
and if not starts it(script)

sudo netstat -nlp | grep :80   ***check port 80

cd /var/log

ls -l /etc/nginx/

ls -l /etc/nginx/sites-enabled

cat *.conf

```conf
location / {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:3031;
}

```



`uwsgi_pass 127.0.0.1:3031;` this means we connect to app dynamic content 

ls -l /etc/uwsgi

ls -l /etc/uwsgi/apps-enabled

cat *.ini

show file,logs, server
in file enable debug mode

sudo service uwsgi reload

ls -l site*

and we can see that log file empty
so app doesn't have permissions to write

sudo chown www-data.www-data site.log


### Core files - files about crash

ulimit -c unlimited **allow linux unlimited 

then we can run our program

./example

ls -l core

gdb -c core example

print info termination reason
and we can see commands that root:
backtrace

using command up we can see lines
up

using list command you can see block
list

and we can print variables
print i

print argv[0]

print argv[1]

if 0x0 means null pointer

!!! for (int i=0; i<=argc;i++){...}

common mistake if we have one argument use:

for (int i=0; i<argc;i++){...}



### debugger pdb3

pdb3 update_product.py products.csv
comands: next, continue, print...


### resources

deleted files - app open files and it
is temp file marked as deleted

sudo lsof | grep deleted ***find opened files


network

latency - delay between sending and receiving

bandwith - amount we can sent or receive in a sec

10Mbit/s bandwidth you can sent 1.25Mbytes/s

iftop - show how much each connection sent

network limited resource, and less traffic than better

Traffic shaping - mark data packets with priority



[Content](#content)

## Configuration management

### Puppet Resources
 
https://puppet.com/docs/puppet/latest/lang_resources.html

https://puppet.com/blog/deploy-packages-across-your-windows-estate-with-bolt-and-chocolatey/

 https://puppet.com/docs/puppet/latest/style_guide.html
 https://puppet.com/docs/puppetserver/latest/install_from_packages.html

http://www.masterzen.fr/2010/11/14/puppet-ssl-explained/

 https://rspec-puppet.com/tutorial/
http://puppet-lint.com/


### Clouds

https://cloud.google.com/compute/docs/quickstart-linux
https://cloud.google.com/compute/docs/instances/create-vm-from-instance-template
https://cloud.google.com/sdk/docs

Getting started on GCP with Terraform

Creating groups of unmanaged instances

Official documentation is here:

 https://cloud.google.com/load-balancing/docs/https/

https://geekflare.com/gcp-load-balancer/

Interesting articles about hybrid setups:

 https://blog.inkubate.io/create-a-centos-7-terraform-template-for-vmware-vsphere/

 https://www.terraform.io/docs/enterprise/before-installing/reference-architecture/gcp.html

 https://www.hashicorp.com/resources/terraform-on-premises-hybrid-cloud-wayfair

Quotas you’ll find in various cloud providers

https://cloud.google.com/compute/quotas#understanding_vm_cpu_and_ip_address_quotas

 https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html

 https://docs.microsoft.com/en-us/azure/azure-subscription-service-limits#service-specific-limits
    
Monitoring and Alerting

 https://www.datadoghq.com/blog/monitoring-101-collecting-data/

 https://www.digitalocean.com/community/tutorials/an-introduction-to-metrics-monitoring-and-alerting

 https://en.wikipedia.org/wiki/High_availability

 https://landing.google.com/sre/books/


Debug

https://cloud.google.com/compute/docs/troubleshooting/troubleshooting-instances

https://docs.microsoft.com/en-us/azure/virtual-machines/troubleshooting/

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-troubleshoot.htm

### commands when the problem with apache and root cause other programm

sudo systemctl status apache2

sudo systemctl restart apache2

sudo systemctl status apache2

sudo netstat -nlp

ps -ax | grep python3

cat /usr/local/bin/jimmytest.py

sudo kill [process-id]

ps -ax | grep python3

sudo systemctl --type=service | grep jimmy

sudo systemctl stop jimmytest && sudo systemctl disable jimmytest

sudo netstat -nlp

sudo systemctl start apache2



[Content](#content)

## Automating tasks

Application Programming Interfaces (APIs) help different 
pieces of software talk to each other. When you write 
a program, you typically use a bunch of existing libraries 
for the programming language of your choice. These libraries 
provide APIs in the form of external or public functions, classes, 
and methods that other code can use to get their job done without 
having to create a lot of repeated code.


from PIL import Image
im = Image.open("bride.jpg")
im.rotate(45).show()

### Lab


resize.py
```python

#!/usr/bin/env python3
import os
from PIL import Image
old_path = os.path.expanduser('~') + '/images/'
new_path = '/opt/icons/'
for image in os.listdir(old_path):
        if '.' not in image[0]:
                img = Image.open(old_path +image)
                img.rotate(-90).resize((128,128)).convert("RGB").save(new_path + image.split('.')[0], 'jpeg')
                img.close()

```   


### Web app

A web application is an application that you interact with over HTTP. 
Instead of browsing to a web page to type and click around, 
you can use your program to send a message known as an API 
call to the web service. The part of the program that listens 
on the network for API calls is called an API endpoint.

### Serialization

Comma-Separated Value (CSV) file is one example of a technique 
called data serialization. Data serialization is the process 
of taking an in-memory data structure, like a Python object, 
and turning it into something that can be stored on disk 
or transmitted across a network. 

#### Data Serialization Formats

JSON (JavaScript Object Notation)
YAML (Yet Another Markup Language)
Python pickle, Protocol Buffers, or the eXtensible Markup Language (XML)


### Libs



```python

import json

```   


Python Requests library

```python

import requests

``` 

### Frameworks

Django is a full-stack web framework written in Python
Alternative Python-based web frameworks similar to Django
 include Flask, Bottle, CherryPy, and CubicWeb.

    • Python Image Library (PIL) - Tutorial
    • Requests (HTTP client library) - Quickstart
    • ReportLab (PDF creation library)
    • email (constructing email)
    • psutil (processes and system utilization)
    • shutil (file operations)
    • smtplib (sending email)



[Content](#content)