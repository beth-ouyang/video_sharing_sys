import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import urlparse
import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)

APP_PORT = os.environ["APP_PORT"]
API_BASE = "http://api:" + APP_PORT

def valid_domain(video_url):
    domain = urlparse(video_url).netloc
    if domain not in ["youtu.be", "www.youtube.com", "www.bilibili.com"]:
        st.error("Please enter a valid YouTube/Bilibili video link.")
        return None
    return domain

def submit_form():

    with st.form(key="client_form", clear_on_submit=True, enter_to_submit=False) as form:
        donator = st.text_input("Your nickname", key="donator_name_widget")
        donate_amount = st.number_input("Donate Amount", min_value=0, step=10, key="donate_amount_widget")

        video_url = st.text_input("Youtube Video Link", key="url_widget")

        submitted = st.form_submit_button("Submit")
        if submitted:
            if not (donator and video_url):
                st.error("Miss something? Nickname and video link are both required!")

            else:
                domain = valid_domain(video_url)
                if domain:
                    res = requests.post(f"{API_BASE}/submit", json={"url": video_url, "domain": domain})
                    if res.status_code == 200:
                        st.success("Video submitted!")
                    else:
                        st.error(f"Failed to submit video. \n {res}")

    st.markdown("### Preview")
    if video_url:
        domain = valid_domain(video_url)
        if domain in ["youtu.be", "www.youtube.com"]:
            st.video(video_url, format="video/mp4")
        elif domain == "www.bilibili.com":
            components.iframe(video_url, height=600)

def main():
    st.set_page_config(page_title="Video Sharing Submit Form")
    st.title("Video Sharing Submit Form")
    submit_form()

if __name__ == "__main__":
    main()