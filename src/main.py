import datetime
import os
from typing import Any

import numpy as np
import sounddevice as sd
from slack_sdk import WebClient, errors


class Notifier:

    notified_at: datetime.datetime
    slack_token: str

    def __init__(self):
        self.notified_at = datetime.datetime.now() - datetime.timedelta(seconds=10)
        self.slack_token = os.environ["SLACK_TOKEN"]

    def _slack_notify(self):
        client = WebClient(token=self.slack_token)
        try:
            _ = client.chat_postMessage(
                channel="インターホン通知",
                text="<!channel> インターホンが鳴りました",
            )

        except errors.SlackApiError as e:
            print(e.response["error"])

    def _notify(self):
        print("notify")
        self._slack_notify()
        self.notified_at = datetime.datetime.now()

    def _audio_callback(
        self, indata: np.ndarray, frames: int, time: Any, status: sd.CallbackFlags
    ):
        if datetime.datetime.now() - self.notified_at < datetime.timedelta(seconds=5):
            return

        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > 50:  # 音量の閾値を設定
            print("音が検出されました！")
            self._notify()

    def start(self):
        with sd.InputStream(
            callback=self._audio_callback,
            channels=1,
            samplerate=44100,
            blocksize=44100 * 2,
        ):
            print("音声入力を監視しています...")
            sd.sleep(10000)
            while True:
                pass


def main():
    notifier = Notifier()
    notifier.start()


if __name__ == "__main__":
    main()
