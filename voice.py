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

raw_text = """精于一业
稻盛先生说:
把精力倾注在一个领域，钻深钻透，就能明白人生的真理，理解大千世界，森罗万象。
比如一个优秀的工匠，经多年潜心研究，掌握了卓越的技术，这样的工匠，就是谈论人生，也会有精辟的见解。一个僧人，经反复修道，磨炼出高尚的人格，这样的僧人，即使涉及与“修心养性”的教义无关的领域，也能说出深刻的道理。其他例如绘画、著书等，任何精通一艺者，都会有同样的涵养，达到相同的境界。
可惜刚从学校毕业的年轻人不懂得这个道理。他们轻视自己从事的具体工作，缺乏耐心，怀疑手头的工作是否真有意义，他们常要求上司分配更重要的工作。其实，这样的人无论让他干什么，都不会满意，总是不肯尽心。
知识广而浅，似乎什么都懂，但什么都只懂一点皮毛，等于一无所知，一无所长。相反，精通一技、一艺、一业，就能融会贯通，举一反三，乃至领会宇宙的真理。精于一业就可理解一切，究明一个事物，就可理解一切事物，在一切事物的深处，都隐藏着普遍的真理。
稻盛先生在新颖陶瓷领域精耕细作15年，使这种新材料得到广泛的应用，被誉为创造了又一个“新石器时代”。但京瓷公司毕竟只是一个陶瓷元件厂，新颖工业陶瓷这个行业毕竟只是一个较小的行业。然而，稻盛先生倾注心血，在这一领域钻研很深，而“在一切事物的深处，都隐藏着普遍的真理”。“京瓷哲学”就是这种真理的结晶，是稻盛先生在这一段实践过程中悟得的经营和人生的真谛。而仅凭这个哲学，稻盛先生勇敢地闯入了对自己而言完全陌生的、全新的领域--通信事业，创建了日本第二电信电话公司，并且很快取得了令人难以置信的、卓越的成功。
2010年2月1日，航空事业的门外汉、78岁高龄的稻盛先生，受日本政府的邀请，在万众瞩目之下，出任破产重建的日本航空公司董事长，仅仅一年，不仅让日航起死回生，而且创造了日航60年历史中最高的利润。世人一片惊叹。
“DDI”和日航的成功，证明精于一业果然可以举一反三。可见“隔行不隔理”，比“隔行如隔山”更加正确，而这个“理”就是哲理，就是哲学。
我们提倡解剖麻雀，麻雀虽小，五脏六腑俱全。个性中包含共性，特殊性中包含普遍性。不管什么行业、什么领域，达到一定深度，就会触类旁通，柳暗花明，殊途同归，进入哲学的境界。"""
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