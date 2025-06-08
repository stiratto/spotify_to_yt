Welcome to the Spotify to YouTube Music migration project!

# Prerequisites:
Before you begin, ensure you have Python and pip installed on your system.

Step 1: Install Requirements
Open your terminal and navigate to the project's folder:
`cd path/to/spotify_to_yt-main`

Install the required packages by running:
`pip install -r requirements.txt`

Step 2: Authenticate with YouTube Music API
Run the following command in the console:

`ytmusicapi oauth`

Follow the indicated process to authenticate your YouTube Music account. This step is crucial for accessing and modifying your playlists.

Step 3: Get ChromeDriver Executable
Follow the video tutorial at this link to download and set up the ChromeDriver executable. Once downloaded, copy the chromedriver executable into the project's folder.

# Usage:
Now that you have set up everything, you're ready to migrate your Spotify liked albums and playlists to YouTube Music.

Run the Python script:
`python spotify_to_yt.py`

The script will prompt you to enter the method that you'll use to log in and then your email and password. This information is required to access your liked albums and playlists.

Sit back and relax! The migration process may take 5-10 minutes, depending on the number of liked items.

Important Note:
Make sure you keep your authentication tokens and sensitive information secure. Do not share them publicly.

Feel free to reach out if you encounter any issues or have questions. Enjoy your migrated playlists on YouTube Music!
