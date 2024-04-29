import streamlit as st
# from streamlit_chromadb_connection.chromadb_connection import ChromadbConnection
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

HOST_IP = os.environ.get("HOST_IP")

st.title('💊 Medicine Chatbot')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "disable_chat_input" not in st.session_state:
    st.session_state.disable_chat_input = False
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        

if prompt := st.chat_input("궁금한 점을 물어보세요.", key='input_question', disabled=st.session_state.disable_chat_input):
        
    # 유저가 보낸 내용은 내용 그대로 사람 아이콘과 함께 화면에 출력하기 
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # 답변이 올 때 까지 질문 막음
    st.session_state.disable_chat_input = True
    st.rerun()
    
if st.session_state.disable_chat_input:
    
    prompt = st.session_state.messages[-1]['content']

    with st.spinner('답변을 기다리는 중...'):
        response = requests.post(f"http://{HOST_IP}:8000/question/", json={"question": prompt})

        try:
            if response.status_code == 200:
                result = response.json()
                print("\n\n\n\n반환 받은 거 전체:\n\n", result)

                st.session_state.messages.append(
                        {"role": "assistant", "content": result['answer']}
                    )
                with st.chat_message("assistant"):
                    st.markdown(result['answer'])
                    # st.write_stream(result['answer'])

            else:
                st.session_state.messages.append(
                        {"role": "system", "content": "System Error"}
                    )
                with st.chat_message("system"):
                    st.markdown("System Error")
        except:
            st.session_state.messages.append(
                    {"role": "system", "content": "System Error"}
                )
            with st.chat_message("system"):
                st.markdown("System Error")
                
    st.session_state.disable_chat_input = False
    st.rerun()
    
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []