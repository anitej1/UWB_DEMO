Preparation
-----------
1.Modify the startup.sh to include location of UWB driver and UWB demo on your RPI

2.Add startup.sh to run on startup each time RPI is booted
```
chmod +x /home/user/startup.sh
$ crontab -e
```

Run
---
Run publisher script on RPI and subscriber on PC
