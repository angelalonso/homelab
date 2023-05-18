#!/usr/bin/env bash

echo none >/sys/class/leds/led0/trigger

echo 1 >/sys/class/leds/led0/brightness
sleep 0.4
echo 0 >/sys/class/leds/led0/brightness
sleep 0.1

echo 1 >/sys/class/leds/led0/brightness
sleep 0.4
echo 0 >/sys/class/leds/led0/brightness
sleep 0.1

echo 1 >/sys/class/leds/led0/brightness
sleep 0.4
echo 0 >/sys/class/leds/led0/brightness
sleep 0.1

echo 1 >/sys/class/leds/led0/brightness
sleep 0.4
echo 0 >/sys/class/leds/led0/brightness
sleep 0.1


echo mmc0 >/sys/class/leds/led0/trigger

