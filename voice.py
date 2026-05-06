# -*- coding: utf-8 -*-
import dashscope
import time
from pathlib import Path
from dashscope.audio.tts_v2 import SpeechSynthesizer

dashscope.api_key = "sk-36ee1c702e194855b9588f646a5836cc"

# 设置地域（国内用户）
dashscope.base_websocket_api_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'

synthesizer = SpeechSynthesizer(
    model="cosyvoice-v3.5-plus",  
    #Chenbingrun
    voice="cosyvoice-v3.5-plus-bailian-b4c014c43af24f829370644f10de3cc2"
)

raw_text = """突破壁障
稻盛先生说:
成功人士和非成功人士之差，不过薄纸一张。没有获得成功的人未必缺乏责任感，事实上其中不少人有诚意，有热情，工作努力，在这些方面他们与成功人士并没有什么区别。
尽管如此，有的人成功了，有的人却失败了，人们或许感叹世道不公。实际上，两者之间虽然只有一层薄纸之差，但是它竟是一层不易突破的壁障。
这个“差”是什么?是坚韧性和忍耐力。
失败人士在遭遇壁障的时候，一开始就认定壁障无法突破。换句话，他们努力是努力了，但努力到一定程度，就停顿了。这种人碰到障碍，总会寻找适当的借口，停止努力。
要实现看起来似乎不可能实现的事情，必须持续坚韧不拔的努力，必须打破自己头脑里“只能做到这一步了”的既成概念。如果持有这种顽固的固定观念，那么就不可能突破壁障，如果超越界限，就能达至成功。
壁障最终必能突破，这种自负和自信，可以形成坚韧的性格，而这种坚韧性又会把我们引向更大的成功。
所谓成功，就是做到成功为止，成功之前不言放弃，不断克服达至成功过程中的困难、失败和障碍。换句话说，就是要成功突破壁障。稻盛曾应邀为日立制作所的研究开发人员讲演，被问到京瓷开发新产品的成功率是多少时，稻盛答:百分之百。“这怎么可能!”日立的精英们不相信。稻盛说道:因为我们开发新产品的方针是必须成功，成功之前决不放弃。
成功人士有信念，他们遭遇壁障时，一开始就认定壁障必定会突破，然后千方百计努力突破壁障，结果就突破了壁障。非成功人士有时也很努力，但这种努力，因为缺乏信念支撑，在遭遇障碍和挫折时，就不能持续，结果往往功亏一篑，中途放弃了原本可以做成的事。可见成功人士与失败人士之差，仅仅是一念之差，但这一念之差，却是重大的观念之差、信念之差，于是“差之毫厘，失之千里”。"""
text = "".join(line.strip() for line in raw_text.splitlines())

print('111',text)
timeout_millis = 120000
    
print("开始生成语音，长文本通常需要接近 1 分钟，请勿提前中断。")
start_time = time.perf_counter()

try:
    audio = synthesizer.call(text, timeout_millis=timeout_millis)
except TimeoutError:
    print(f"生成超时，已等待 {timeout_millis / 1000:.0f} 秒。可以稍后重试，或缩短单次合成的文本长度。")
    raise
except Exception as exc:
    print(f"语音生成失败: {exc}")
    raise

from datetime import datetime

voice_name = "陈炳润"
output_dir = Path("sound")
output_dir.mkdir(exist_ok=True)
filename = output_dir / f"{voice_name}.m4a"

with open(filename, 'wb') as f:
    f.write(audio)

elapsed = time.perf_counter() - start_time
print(f"生成完成！文件: {filename}，耗时 {elapsed:.1f} 秒")