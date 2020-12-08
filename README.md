# RaspCar Server

Cars are amazing, and we spend a lot of time in them, then why not having your own linux server running in it?

This repo contains a set of services you can install on a raspberry PI zero to have:

1) a NAS in your car: connect your raspberry PI zero to the USB port of your car multimedia system. When your car is in your WIFI range, your raspberry PI zero will wirelessly connect to your PC and automatically download the latest music you purchased! The music will then be accessible from your car multimedia system and seen as an external mass storage (with the benefit that you can use all your car multimedia controls, instead of the limited set compatibile with bluetooth music streaming). Note: for this a rasperry with an OTG USB is needed!

2) an OBD logger: if you have a bluetooth OBD adapter in your car, your raspberry PI zero will connect to it and record relevant data from your vehicle. You can then analyze it, reverse engineer your car, and learn how you can improve your driving! For some ideas on how to analyze the data checkout [this repo](https://github.com/maximiliano1985/process__OBDcar_data).

3) a GPS recorder (WIP): connect a GPS to your raspberry GPIO to track your trips!


## To install
Download the repo in your raspberry PI Zero

> sudo sh install.sh

NB: your raspberry will need access to internet to install some Python packages.

