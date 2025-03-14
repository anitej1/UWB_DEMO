import paho.mqtt.client as mqtt
import pygame
import time

# MQTT settings
MQTT_BROKER = "192.168.157.249"  # Replace with your broker's IP
MQTT_PORT = 1883
MQTT_CONTROL_TOPIC = "audio/control"            # Used to receive control commands from the publisher
MQTT_POSITION_REPLY_TOPIC = "audio/position_reply"  # Used to reply with current playback position

# Audio file path
AUDIO_FILE = "test_audio.mp3"  #enter audio file location

# Initialize pygame for audio playback
pygame.mixer.init()

remote_audio_start_time = None
is_playing = False

# Set up MQTT client
mqtt_client = mqtt.Client()

def on_message(client, userdata, msg):
    global remote_audio_start_time, is_playing
    payload = msg.payload.decode()
    if msg.topic == MQTT_CONTROL_TOPIC:
        if payload == "switch_back":
            if is_playing and remote_audio_start_time is not None:
                pos = time.time() - remote_audio_start_time
                print(f"Switch back command received. Current remote playback position: {pos:.2f} seconds.")
                # Stop remote playback
                pygame.mixer.music.stop()
                is_playing = False
                # Publish current playback position so that the publishe        r can resume local playback from there.
                client.publish(MQTT_POSITION_REPLY_TOPIC, str(pos))
        else:
            try:
                # Assume the payload is a float value representing the playback position (in seconds)
                pos = float(payload)
                print(f"Received command to start/resume playback from {pos:.2f} seconds on remote device.")
                pygame.mixer.music.load(AUDIO_FILE)
                pygame.mixer.music.play(start=pos)
                remote_audio_start_time = time.time() - pos
                is_playing = True
            except ValueError:
                print("Received invalid command on control topic.")

mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_CONTROL_TOPIC)
mqtt_client.loop_forever()
