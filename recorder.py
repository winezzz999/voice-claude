"""第1步：按住左Alt说话，松开后保存为test.wav（自诊断版）"""
import queue
import sys
import numpy as np
import sounddevice as sd
from pathlib import Path
from pynput import keyboard
import wave

SAMPLE_RATE = 16000   # 每秒采集16000个点，语音识别的标准采样率
CHANNELS = 1          # 单声道
OUTPUT_FILE = Path(__file__).parent / "test.wav"

audio_queue = queue.Queue()


def log(msg):
    print(msg, flush=True)   # flush=True：立即显示，不留在缓冲区里


def audio_callback(indata, frames, time_info, status):
    """声卡每攒够一小块音频就自动调用这个函数"""
    audio_queue.put(indata.copy())


log(f"① 程序启动（Python {sys.version.split()[0]}），文件将保存到：{OUTPUT_FILE}")

stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS,
                        dtype="float32", callback=audio_callback)
log("② 麦克风已就绪")


def on_press(key):
    log(f"   [按键] 按下 {key}")
    if key == keyboard.Key.esc:
        log("退出。")
        return False
    if key == keyboard.Key.alt_l:   # 左Alt
        stream.start()
        log("③ 开始录音（松开左Alt结束）")


def on_release(key):
    log(f"   [按键] 松开 {key}")
    if key == keyboard.Key.alt_l:
        stream.stop()
        sd.sleep(200)              # 等声卡把最后几块数据送完
        chunks = []
        while not audio_queue.empty():
            chunks.append(audio_queue.get())
        log(f"④ 队列里收到 {len(chunks)} 块音频数据")
        if chunks:
            try:
                audio = np.concatenate(chunks, axis=0)
                audio_16bit = (audio * 32767).astype(np.int16)  # 浮点转16位整数
                with wave.open(str(OUTPUT_FILE), "wb") as wf:
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(2)          # 16位 = 2字节
                    wf.setframerate(SAMPLE_RATE)
                    wf.writeframes(audio_16bit.tobytes())
                log(f"⑤ 已保存 {OUTPUT_FILE}（{len(audio) / SAMPLE_RATE:.1f} 秒）")
            except Exception as e:
                log(f"✗ 保存失败：{type(e).__name__}: {e}")
        else:
            log("✗ 队列是空的——说话时间太短或录音流没启动，试试按住超过1秒")


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    log("⑥ 现在按住【左Alt】说话（注意是左边的Alt），松开后看打印。Esc退出。")
    listener.join()
