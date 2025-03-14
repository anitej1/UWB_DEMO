import subprocess
import ast
import time
import pygame
import paho.mqtt.client as mqtt
import UWB_RMS_distance

# MQTT settings
MQTT_BROKER = "192.168.157.249"  # Replace with your broker's IP
MQTT_PORT = 1883
MQTT_CONTROL_TOPIC = "audio/control"            # Used to send commands to the remote device
MQTT_POSITION_REPLY_TOPIC = "audio/position_reply"  # Used to receive the remote playback position

# Audio file path
AUDIO_FILE = "/home/anitej/test_audio.mp3"

# Initialize pygame for audio playback
pygame.mixer.init()

# State variables
control_state = "local"  # either "local" or "remote"
local_audio_start_time = None

# Set up MQTT client (for both publishing and subscribing)
mqtt_client = mqtt.Client()

def on_message(client, userdata, msg):
    global control_state, local_audio_start_time
    if msg.topic == MQTT_POSITION_REPLY_TOPIC:
        try:
            pos = float(msg.payload.decode())
            print(f"Received remote playback position: {pos:.2f} seconds. Switching back to local playback.")
            # Start local playback from the remote's current position
            pygame.mixer.music.load(AUDIO_FILE)
            pygame.mixer.music.play(start=pos)
            local_audio_start_time = time.time() - pos
            control_state = "local"
        except Exception as e:
            print("Error processing remote playback position:", e)

mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_POSITION_REPLY_TOPIC)
mqtt_client.loop_start()  # Run the MQTT loop in a background thread

def play_local_audio_from_start():
    global local_audio_start_time
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.play()
    local_audio_start_time = time.time()

def get_local_playback_position():
    if local_audio_start_time is None:
        return 0
    return time.time() - local_audio_start_time

def send_control_message(message):
    mqtt_client.publish(MQTT_CONTROL_TOPIC, str(message))

def get_distance_data():
    """
    Runs the external script 'distance_provider.py' which must print a 3-element list:
    [distance (in meters), angle_of_attack_azimuthal, angle_of_attack_elevation]
    """
    try:
        distance = subprocess.check_output(["python", "UWB_RMS_distance.py"], text=True)
        return eval(distance)
    except Exception as e:
        print("Error obtaining distance data:", e)
        return None

# Start local playback initially
play_local_audio_from_start()
control_state = "local"

try:
    while True:
        data = get_distance_data()
        if data is None or not isinstance(data, list) or len(data) < 3:
            print("Invalid distance data received. Skipping this cycle.")
            time.sleep(2)
            continue

        distance, azimuth, elevation = data
        print(f"Distance: {distance} cm, Azimuth: {azimuth}°, Elevation: {elevation}°")

        # If distance is less than 1m:
        if distance < 100:
            if control_state == "remote":
                # Request the remote device to switch back to local control.
                print("Distance less than 1m but control is remote. Requesting switch back.")
                send_control_message("switch_back")
            # Otherwise, local control continues (audio plays locally)
        else:  # distance >= 1m:
            if control_state == "local":
                # Send current playback position to remote device and switch control.
                pos = get_local_playback_position()
                print(f"Distance >= 1m and control is local. Sending playback position {pos:.2f} seconds to remote device.")
                send_control_message(pos)
                pygame.mixer.music.stop()
                control_state = "remote"

        time.sleep(2)

except KeyboardInterrupt:
    print("Process stopped by user.")
    mqtt_client.loop_stop()
