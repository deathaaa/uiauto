#!/usr/bin/env bash
device_num=$1
app=$2
appium --log-level info -U $device_num --app $app
