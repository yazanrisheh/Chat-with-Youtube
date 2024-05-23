import csv
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pytube import YouTube
from serpapi import GoogleSearch

load_dotenv()

def setup():
    st.set_page_config(
        page_title="	✨ YouTube Video Summarization",     layout="centered"
    )
    st.header(":sparkles: Summarize YouTube Videos", anchor=False, divider="orange")

    st.sidebar.header("About this app:", divider="rainbow")
    st.sidebar.write("1. Choose how you want to provide URL")
    st.sidebar.write("2. Provide LLM a prompt to summarize or answer question")
    with st.sidebar:
        st.divider()

    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

def get_video_source():
    tip1 = "Use YouTube search option to find videos based on your search term, or directly enter or paste an url."
    choice = st.sidebar.radio(
        ":red[Choose source for URL:]",
        [":red[Use YouTube Search]", ":red[Directly Enter URL(s)]"],
        help=tip1,
    )
    return choice

def getgptresponse(client, model, temperature, message, streaming):
    try:
        response = client.chat.completions.create(
            model=model, messages=message, temperature=temperature, stream=streaming
        )

        output = response.choices[0].message.content
        tokens = response.usage.total_tokens
        yield output, tokens

    except Exception as e:
        print(e)
        yield ""

def split_audio(input_file, chunk_duration=300):
    """Splits audio into chunks of specified duration using ffmpeg.

    Args:
        input_file (str): Path to the input audio file.
        chunk_duration (int, optional): Duration of each chunk in seconds. Defaults to 300 (5 minutes).
    """
    output_filename = os.path.splitext(input_file)[0]
    os.system(f"ffmpeg -i {input_file} -c copy -f segment -segment_time {chunk_duration} {output_filename}%03d.mp4")

def main():
    setup()
    choice = get_video_source()
    if choice == ":red[Use YouTube Search]":
        url = st.text_input("Enter search term for YouTube search and hit enter.")
        if url:
            params = {
                "engine": "youtube",
                "search_query": f"{url}",
                "api_key": f"{SERP_API_KEY}",
                "num": "10",
            }

            search = GoogleSearch(params)
            results = search.get_dict()
            yt_results = results['video_results']

            with open(
                "serpapi_ytresults.csv", "w", newline="", encoding='utf-8'
            ) as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Title", "Link", "Length", "Published_date"])
                for result in yt_results:
                    csv_writer.writerow(
                        [
                            result["title"],
                            result["link"],
                            result["length"],
                            result["published_date"],
                        ]
                    )
            df_yt = pd.read_csv("serpapi_ytresults.csv", index_col=0)
            st.write(
                "Top 10 results from the search, copy the url of the video of interest:"
            )
            st.dataframe(df_yt.head(10))
            st.divider()

            st.write(
                "Copy-paste an url from above list for the video you want a LLM to summarize the content of the video"
            )
            yt_url = st.text_input(
                "Paste or enter the YouTube URL you want to talk to."
            )
            if yt_url:
                yt = YouTube(f"{yt_url}")
                yt.streams.filter(only_audio=True).first().download(
                    filename="trialmp.mp4"
                )
                audio_file = open("trialmp.mp4", "rb")

                if os.path.getsize("trialmp.mp4") > 25000000:  # Check if file is too large
                    st.write("Audio file too large. Splitting into segments...")
                    split_audio("trialmp.mp4")

                try:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1", response_format="text", file=audio_file
                    )
                except openai.APIStatusError as e:
                    st.error(f"Error transcribing audio: {e}")
                    st.write("Consider splitting or reducing audio file size.")

                model = "gpt-3.5-turbo-0125" 
                prompt = st.text_input(
                    "Enter prompt for LLM, e.g. Summarize the following youtube transcript."
                )
                if prompt:
                    message = []
                    message.append({"role": "system", "content": f"{prompt}"})
                    message.append({"role": "user", "content": f"{transcript}"})
                    for result in getgptresponse(
                        client, model, temperature=0, message=message, streaming=False
                    ):
                        output = result[0]
                        st.write(output)

    else:
        yt_url2 = st.text_input(
            "Paste or enter each YouTube URL you want to download audio for, separate urls with a space if you wanna chat with multiple at once."
        )
        if yt_url2:
            urls = yt_url2.split(" ")
            zlen = len(urls)
            transcripts = []
            for i in range(zlen):
                yt_url3 = urls[i]
                yt = YouTube(f"{yt_url3}")
                yt.streams.filter(only_audio=True).first().download(
                    filename="trialmp.mp4"
                )

                audio_file = open("trialmp.mp4", "rb")
                try:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1", response_format="text", file=audio_file
                    )
                    transcripts.append(transcript)
                except openai.APIStatusError as e:
                    st.error(f"Error transcribing audio: {e}")
                    st.write("Consider splitting or reducing audio file size.")

            model = "gpt-3.5-turbo-0125"  
            prompt2 = st.text_input(
                "Enter prompt for LLM, e.g. Summarize the following youtube transcript."
            )
            if prompt2:
                message2 = []
                message2.append({"role": "system", "content": f"{prompt2}"})
                message2.append({"role": "user", "content": f"{transcripts}"})
                for result2 in getgptresponse(
                    client, model, temperature=0, message=message2, streaming=False
                ):
                    output2 = result2[0]
                    st.write(output2)

if __name__ == "__main__":
    SERP_API_KEY = os.environ.get("SERPAPI_KEY")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)
    main()