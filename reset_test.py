from classes.logs import LOGS
import threading, subprocess, time, os, signal


class RESET():
    def __init__(self) -> None:
        pass
    def re(self):
        os.kill(process.pid, signal.SIGTERM)
        time.sleep(61)
        bot_thread = threading.Thread(target=RESET().reset().run_bot)
        bot_thread.start()
    def reset(self):
        process=""
        def run_bot():
            global process
            process = subprocess.Popen(["python", "bot.py"])

        bot_thread = threading.Thread(target=run_bot)
        bot_thread.start()

        while True:
            x = "02:00"
            time1 = LOGS().tim()
            if time1 in x:
                re()
            else:
                time.sleep(40)

