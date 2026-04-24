import streamlit as st   # type: ignore[import-not-found]
import os
from openai import OpenAI

# 全局配置
st.set_page_config(
    page_title="DeepSeek App",
    page_icon="😀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# 设置标题
# st.title('DeepSeek')

# 初始化名字
name = '小可爱'
character = '温柔可爱一口台湾腔的台湾妹子'

# 设置侧边栏
with st.sidebar:
    st.subheader("AI控制面板")
    text_val = st.text_input("名字", name, placeholder="请输入姓名")
    text_area_val = st.text_area("性格", character, placeholder="请输入性格")
# 存储数据记录
if 'message' not in st.session_state:
    st.session_state.message = []

prompt = st.chat_input("请输入内容")

# 缓存之前显示的数据
for message in st.session_state.message:
    st.caht_message(message['role']).write(message['content'])

system_message = f"你叫{name}，是一位{character}。你的声音像春日暖阳，语调平和舒缓。不要在用户明显难过时还开玩笑,要使用过于老土或过时的网络用语"
if prompt:
    # 客户请求内容
    st.chat_message("user").write(prompt)
    st.session_state.message.append({"role": "user", "content": prompt})
    # 调用deepseek
    client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": system_message}, *st.session_state.message],  # 使用滚雪球发进行数据记忆功能
        stream=True
    )

    # 使用 st.empty()
    with st.chat_message("assistant"):
        placeholder = st.empty()
        chunk_data = ""
        for chunk in response:
            chunk_data += chunk.choices[0].delta.content
            placeholder.markdown(chunk_data)

    st.session_state.message.append({"role": "assistant", "content": chunk_data})
