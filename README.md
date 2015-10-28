# docktree

Displays the tree structure of your Docker images.

Usage example:

    (env)pi@raspberrypi [docktree/docktree] % ./docktree
    └╴ 71a76a74c237
       ├╴ 92b43b34adf9 test1:latest
       └╴ 2f5ca2d69bf4
          └╴ ba37442b01bb
             ├╴ 643e1371a625 test2:latest
             │  └╴ 7e548b8390f2 test3:latest
             └╴ c89a6bc5d884
                └╴ baee49e775b3 resin/rpi-raspbian:jessie
