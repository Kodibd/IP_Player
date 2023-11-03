#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
https://wiki.videolan.org/Documentation:Command_line/
"""

import PySimpleGUI as sg
import requests
import vlc  #kurmak için: pip install python-vlc

def get_radio_stations(m3u_url):
    stations = []
    response = requests.get(m3u_url)
    for line in response.text.split("\n"):
        if line.startswith("#EXTINF"):
            station_name = line.split(",")[1]
        elif line.startswith("http"):
            stations.append((station_name, line))
    return stations

def main():
    m3u_url = "https://kodibd.github.io/IP/index.m3u"
    stations = get_radio_stations(m3u_url)
    layout = [
        [sg.Text("Radyo İstasyonları")],
        [sg.Listbox(values=[station[0] for station in stations], size=(40, 20), key="stations")],
        [sg.Slider(range=(0, 100), default_value=50, orientation="h", size=(35, 20), key="volume"),
         sg.Push(),
         sg.Button("Dinle"),
         sg.Button("Durdur"),
         sg.Button("Çıkış")]
    ]
    window = sg.Window("Radyo İstasyonları", layout, finalize=True)
    window['volume'].bind('<ButtonRelease-1>', ' Release')
    
    player = None
    while True:
        event, values = window.read()
        if event == "Dinle":
            if player:
                player.stop()
            try:
                station_name = values["stations"][0]
                #print(station_name)
            except:
                station_name = "M Türk"#kanal seçmeden "Dinle" butonuna basılırsa arızaya düimeden bir kanal çalması için
            station_url = [station[1] for station in stations if station[0] == station_name][0]
            print(station_url)
            player = vlc.MediaPlayer(station_url)            
            try:                
                player.audio_set_volume(int(values["volume"]))
                player.video_set_scale(0.50) #ekrandaki büyüklük oranı, bu olmazsa video büyüklüğü kadar
                
                player.play()
                
                
            except Exception as e:
                print(e)
        elif event == "Durdur":
            if player:
                #player.pause()
                player.stop()
        elif event in (sg.WIN_CLOSED, "Çıkış"):
            if player:
                #player.pause()
                player.stop()
            break
        elif event == 'volume Release':            
            player.audio_set_volume(int(values["volume"]))
        
    window.close()
