#!/usr/bin/env bash
device_num=$1
app=$2
pkill -9 node
sleep 2
start_appium_for_ios.sh  $device_num $app &