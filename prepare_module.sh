#!/bin/bash
cd ./tcp_lgd
sudo rmmod tcp_lgd
make clean
make
sudo insmod tcp_lgd.ko
cd -
