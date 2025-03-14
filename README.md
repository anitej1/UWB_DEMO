Preparation
-----------
1. Clone this repository inside the UWB demo folder, with location resembling "/_uwbiot-top_build/uwbiot-top-sr150_linux"
2. Change location of audio file inside UWB_subscriber.py and UWB_publisher.py
3. Modify MQTT attributes inside above mentioned files.
   IP : Run hostname -I on RPI terminal to get IP (use for both publisher and subscriber)
4. Modify the startup.sh to include location of UWB driver on your RPI
5. Add startup.sh to run on startup each time RPI is booted

```
chmod +x /location/startup.sh
$ crontab -e
```

Run
---
Run publisher script on RPI and subscriber on PC
