```markdown
# YouTube Video Summarizer

# Features

- **Search YouTube:** Search for videos on YouTube by entering a keyword.
- **Choose Videos:** Select from a list of top 10 search results to summarize.
- **Download & Transcribe:** Download the audio of the selected video and transcribe it using OpenAI's Whisper API.
- **Summarize with LLM:** Use OpenAI's GPT-3.5 or GPT-4 to summarize the transcribed text based on your prompt.

# Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yazanrisheh/Chat-with-Youtube.git
   cd Chat
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv env
   ```

3. **Activate the Environment:**
   ```bash
   env/Scripts/activate  # Windows
   source env/bin/activate  # macOS/Linux
   ```

4. **Install Dependencies:**
   ```bash
   pip install streamlit pytube openai serpapi pandas google-search-results
   ```

5. **Set Up Environment Variables:**
   * Create a `.env` file in the same directory as your script.
   * Copy the content from `.env.example` to `.env` and replace the placeholders with your actual API keys.
   * **Get your OpenAI API key from:** [https://openai.com/signup/](https://openai.com/signup/) and add it to the .env file:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```
   * **Get your SerpAPI key from:** [https://serpapi.com/users/sign_up](https://serpapi.com/users/sign_up) and add it to the .env file:
     ```
     SERPAPI_API_KEY=your_serpapi_api_key
     ```
   (Note: For the free version of SerpAPI, you will be asked to verify your account via phone number and email. This may take a few minutes to receive the confirmation for both.)

6. **Run the App:**
   ```bash
   streamlit run main.py
   ```

# Usage

1. **Choose a Video Source:**
   - Use YouTube Search: Enter a search term to find videos.
   - Directly Enter URL(s): Paste one or more YouTube video URLs, separated by spaces.
2. **Provide a Prompt:** Enter a prompt for the LLM to use when summarizing the video. For example: "Summarize the main points of this video."
3. **View Summary:** The app will display the generated summary of the video.

# Notes

- For videos longer than 30-45 minutes, it is recommended to use GPT-4. Otherwise, GPT-3.5 is fine.
- The app downloads audio for each video. Be aware that larger videos might take longer to process. 

# Contribution

Contributions are welcome! Please feel free to fork the repository and submit pull requests.

# License

This project is licensed under the MIT License.

# Upcoming updates

Add conversational feature with memory