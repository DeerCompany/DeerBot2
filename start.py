from classes.logs import LOGS
import threading, subprocess, time, os, signal


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
        os.kill(process.pid, signal.SIGTERM)
        time.sleep(61)
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.start()
    else:
        time.sleep(40)