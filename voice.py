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

text = "战胜自己,稻盛先生说:一个学生头脑不很聪明，但非常用功，以优异成绩毕业。另一个学生头脑很聪明，不用功照样轻松毕业。后者评论前者，说:“那家伙拼命死读书，成绩好有什么了不起，我要是认真起来，他才不是我的对手呢!“毕业之后踏上社会，看到前者获得成功，后者又会说:“那家伙学生时代并不怎么样，我可比他强多了。”贬低同学。言下之意，自己的能力比成功者更强，更大的成功属于他自己才对。事情果真如此吗?“拼命死读书”意味着少玩乐，少看电视，少追求眼前的快乐，意味着必须战胜自己。同样，事业上获得成功，也意味着必须抑制贪图享乐的欲望，全身心投入工作。战胜自己，需要强大的意志。在评价人的能力的时候，应该把意志的强弱考虑进去。意志软弱，回避与自身作斗争，一味选择安逸，这种人的能力归于低劣。在漫长的人生旅程中获取成功的能力，绝不仅仅限于所谓的“智能”能力是一个综合概念。稻盛先生为什么要把意志的强弱也归入能力的范畴?因为意志力，或自我克制力，是立即起作用的、最现实的能力。意志软弱的人即使聪明也难有出息。我们常说，最大的敌人是自己，只有先战胜自己，才可能战胜困难或者战胜对手。所谓“战胜自己”，就是让一个正直的自己战胜一个虚伪的自己;让一个积极的自己战胜一个消极的自己;让一个谦逊的自己战胜一个傲慢的自己;让一个勇敢的自己战胜一个卑怯的自己;让一个乐观的自己战胜一个悲观的自己;让一个踏实的自己战胜一个浮躁的自己;让一个不断追求理想的自己战胜一个一味追逐名利或者一味贪图安逸的自己。稻盛先生说，战胜自己与其说靠“智能”，不如说要靠意志。意志是什么?人的意志是人的“生命工具”。既然是工具，就可以而且应该好好使用，并在使用中磨炼。坚强的意志是成功的必要条件，它与先天的“智能”并没有多大的关系。懂得这一点极为重要。智商一流的名牌大学毕业的高材生，曾经在全国范围内专门选拔、集中培养的天才少年班的成员中，后来真正获得预期成功的也只是少数。因为他们虽然个个天资非凡，却未必都具备明确的信念和坚强的意志。"

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
filename = output_dir / f"{voice_name}_{datetime.now().strftime('%Y%m%d')}.mp3"

with open(filename, 'wb') as f:
    f.write(audio)

elapsed = time.perf_counter() - start_time
print(f"生成完成！文件: {filename}，耗时 {elapsed:.1f} 秒")