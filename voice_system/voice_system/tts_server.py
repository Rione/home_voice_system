import rclpy
from rclpy.node import Node
from voice_system_interfaces.srv import TextToSpeech

from gtts import gTTS
from io import BytesIO
from mpg123 import Mpg123, Out123

class TTS_server(Node):
    def __init__(self):
        super().__init__("text_to_speech")

        self.mp3 = Mpg123()
        self.out = Out123()

        self.service = self.create_service(TextToSpeech, "/voice/tts", self.callback)

        self.get_logger().info("text_to_speech is ready")

    def callback(self, request, response):
        text = request.text

        self.get_logger().info(f"Speaking \"{text}\"")

        try:
            tts = gTTS(text, lang="en")

            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            self.mp3.feed(fp.read())

            for i in self.mp3.iter_frames(self.out.start):
                self.out.play(i)

            response.result = True
            return response
        except:
            self.get_logger().info(f"Error happened while speaking \"{text}\"")

            response.result = False
            return response


def main():
    rclpy.init()

    node = TTS_server()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()