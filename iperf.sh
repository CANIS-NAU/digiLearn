#!/bin/bash
date >> /mnt/digidrive/iperf.log
sudo iperf -c 161.35.230.117 >> /mnt/digidrive/iperf.log