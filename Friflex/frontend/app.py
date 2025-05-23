import streamlit as st
import requests
import time
from typing import Optional

API_GATEWAY_URL = "http://api_gateway:8000"

def main():
    st.title("Chess Video Processing Service")
    
    with st.form("video_form"):
        video_url = st.text_input("Enter YouTube Video URL")
        target_language = st.selectbox(
            "Target Language",    
            ["en", "es", "fr", "de", "ru"],
            index=0
        )
        submitted = st.form_submit_button("Process Video")
    
    if submitted and video_url:
        response = requests.post(
            f"{API_GATEWAY_URL}/process-video",
            json={
                "video_url": video_url,
                "target_language": target_language
            }
        )
        
        if response.status_code == 200:
            job_id = response.json()["job_id"]
            st.success(f"Job submitted successfully! Job ID: {job_id}")
            
            with st.empty():
                while True:
                    status_response = requests.get(
                        f"{API_GATEWAY_URL}/job-status/{job_id}"
                    )
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data["status"]
                        
                        if status == "completed":
                            st.success("Processing completed!")
                            if status_data.get("output_data"):
                                st.json(status_data["output_data"])
                            break
                        elif status == "failed":
                            st.error(f"Processing failed: {status_data.get('error', 'Unknown error')}")
                            break
                        else:
                            st.info(f"Status: {status}")
                            time.sleep(2)
                    else:
                        st.error("Failed to get job status")
                        break
        else:
            st.error("Failed to submit job")

if __name__ == "__main__":
    main() 