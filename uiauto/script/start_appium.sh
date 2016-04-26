#!/usr/bin/env bash
appium_path=$1
app_path=$2
device_num=$3
server_port=$4
bootstrap_port=$5
appium --log-level info --no-reset --app $app_path -U $device_num -p $server_port -bp $bootstrap_port --selendroid-port 8080 --chromedriver-port 9515 --app-pkg com.Qunar --app-activity com.mqunar.splash.SplashActivity --platform-name Android --platform-version 18 --automation-name Appium --session-override --pre-launch
