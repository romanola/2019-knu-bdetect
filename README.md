# 2019-knu-bdetect
2019 Internship

# Pre Requirements:
 - Andoid Studio + AVD(Emulator)
 - SDK Android 8.0 (API level 26)
 - adb tools

# Instal apk to device 
> adb install game_knu.apk

# Download logs from device to PC (current directory)
> adb pull sdcard/GameBot/log/ ./


# Logs structure
# Game log
Time|Event|X - coord|Y-coord
2238|Touch|1326.5259|761.6821

Events:
 - Touch - touch event on device screen
 - Fight - fight with enemy
 - Drop - take coin


# System touch event log
timestamp-sec|timestamp-ms|touch-event|X - coord|Y-coord |contact-major|contact-minor
1548087923   |815	  |0	      |1326.5259|761.6821|5.8410645    |5.8410645

touch-event:
 - 2 - Down
 - 1 - Move
 - 0 - Up
