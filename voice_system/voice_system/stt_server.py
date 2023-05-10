import rclpy
from rclpy.node import Node
from voice_system_interfaces.srv import SpeechToText

import speech_recognition as sr

class STT_server(Node):
    def __init__(self):
        super().__init__("speech_to_text")

        self.rec = sr.Recognizer()
        self.service = self.create_service(SpeechToText, "/voice/stt", self.callback)

        self.get_logger().info("spech_to_text is ready")

    def callback(self, request, response):
        duration = request.duration

        # TODO remove unnecessary terminal output when opening microphone

        with sr.Microphone() as source:
            self.get_logger().info(f"Listening to microphone for {duration} seconds")

            audio_data = self.rec.record(source, duration=duration)

            try:
                text = self.rec.recognize_google(audio_data, language="en-US")

            except sr.UnknownValueError:
                self.get_logger().info(f"Error happened during speech recognition")

                response.result = False
                response.text= ""
                return response

            if text != "":
                self.get_logger().info(f"Recognized \"{text}\"")

                response.result = True
                response.text= text
                return response

def main():
    rclpy.init()

    node = STT_server()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()