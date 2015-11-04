========
Docktree
========

Displays the tree structure of your Docker images.

Meant as a replacement for the removed functionality of `docker images -t`.

Usage: docktree [-h] [IMAGE]

Positional arguments:
    IMAGE       show only parents and children of IMAGE

Optional arguments:
    -h, --help       show this help message and exit
    -s, --show-size  show the virtual size of each layer

Usage example:
::

    (env2)pi@raspberrypi [work/docktree] % docktree
    └─ 71a76a74c237
       ├─ 92b43b34adf9 test1:latest
       └─ 2f5ca2d69bf4
          └─ ba37442b01bb
             ├─ 643e1371a625 test2:latest
             │  └─ 7e548b8390f2 test3:latest
             └─ c89a6bc5d884
                └─ baee49e775b3 resin/rpi-raspbian:latest,resin/rpi-raspbian:jessie,resin/rpi-raspbian:jessie-2015-10-21
    (env2)pi@raspberrypi [work/docktree] % docktree test2
    └─ 71a76a74c237
       └─ 2f5ca2d69bf4
          └─ ba37442b01bb
             └─ 643e1371a625 test2:latest
                └─ 7e548b8390f2 test3:latest
