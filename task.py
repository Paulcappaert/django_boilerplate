from channels.consumer import SyncConsumer
import json


class PrintConsumer(SyncConsumer):
    def chat(self, message):
        print("Test: " + message["message"])
