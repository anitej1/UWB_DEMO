Preparation
-----------
1. Clone this repository inside the folder resembling "/_uwbiot-top_build/uwbiot-top-sr150_linux"

2. Change location of audio file inside UWB_subscriber.py and UWB_publisher.py

3.Modify the startup.sh to include location of UWB driver and UWB demo on your RPI

4.Add startup.sh to run on startup each time RPI is booted

```
chmod +x /home/user/startup.sh
$ crontab -e
```

Run
---
Run publisher script on RPI and subscriber on PC
