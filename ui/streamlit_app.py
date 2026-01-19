import json

import httpx
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("RAG Chatbot")

# FastAPI 서버 URL
API_URL = "http://localhost:8000/chat/stream"


def stream_response(message: str):
    """FastAPI SSE 스트리밍 응답을 처리합니다."""
    with httpx.Client(timeout=60.0) as client:
        with client.stream(
            "POST",
            API_URL,
            json={"message": message},
            headers={"Accept": "text/event-stream"},
        ) as response:
            for line in response.iter_lines():
                if line.startswith("data: "):
                    data = line[6:]  # "data: " 제거
                    if data == "[DONE]":
                        break
                    try:
                        parsed = json.loads(data)
                        if "token" in parsed:
                            yield parsed["token"]
                    except json.JSONDecodeError:
                        continue


# 채팅 히스토리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 히스토리 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("질문을 입력하세요..."):
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)

    # 사용자 메시지 히스토리에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 어시스턴트 응답 스트리밍
    with st.chat_message("assistant"):
        response = st.write_stream(stream_response(prompt))

    # 어시스턴트 응답 히스토리에 추가
    st.session_state.messages.append({"role": "assistant", "content": response})
