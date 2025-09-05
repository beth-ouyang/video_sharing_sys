import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv(override=True)


API_BASE = "http://backend_app:8000"

def __load_queue():
    response = requests.get(f"{API_BASE}/queue")
    queue = response.json()
    return queue

def __get_video_info(video_url, domain):
    if domain in ["www.youtube.com", "youtu.be"]:
        api_url = f"https://www.youtube.com/oembed?url={video_url}&format=json"
        res = requests.get(api_url)
        if res.status_code == 200:
            return res.json()["title"]

    elif domain == "www.bilibili.com":
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        bvid = video_url.split("video/")[-1].split("/")[0]
        api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        res = requests.get(api_url, headers=headers)
        if res.status_code == 200:
            info = res.json()
            title = info["data"]["title"]
            return title
    else:
        return "**Caution:** Cannot get video info!"

def block_page():
    st.header("Sorry!")
    st.subheader("This app is private. Please don't hack me :(")


def manager_page():
    st.set_page_config(page_title="Manage Video Queue")
    # st.title("Manage Video Queue")

    # Load queue
    queue = __load_queue()

    if queue:
        next_video_res = requests.get(f"{API_BASE}/next").json()
        next_video_url = next_video_res["url"]
        domain = next_video_res["domain"]

        if domain in ["youtu.be", "www.youtube.com"]:
            st.video(next_video_url, format="video/mp4")
        elif domain == "www.bilibili.com":
            components.iframe(next_video_url, height=600)

        st.subheader("Current queue")
        for i, item in enumerate(queue):
            col1, col2 = st.columns([5, 1])

            with col1:
                title = __get_video_info(item["url"], item["domain"])
                if title:
                    st.markdown(f"{i+1}. [{title}]({item["url"]})")
                else:
                    st.markdown(f"{i + 1}. {item["url"]}")

            with col2:
                if st.button("❌", key=f"del-{item['id']}"):
                    requests.delete(f"{API_BASE}/queue/{item['id']}")
                    st.rerun()
    else:
        st.info("Queue is empty.")

if __name__ == "__main__":
    user_ip = st.context.ip_address
    st.write(user_ip)

    # ip_address is expected to be None when running locally
    if user_ip and not user_ip in os.environ["AUTH_IP_ADDR"]:
        block_page()
    else:
        manager_page()
