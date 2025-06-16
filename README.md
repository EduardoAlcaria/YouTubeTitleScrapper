
---
# YouTubeTitleScraper

Just a simple tool I made to help me get all the video titles from a playlist, so I can add them to my weekly to-do list.

## 🧰 Features

* ✅ Scrapes all video titles from any **public YouTube playlist**
* 🚀 Automatically scrolls through the entire playlist page (up to 1000 scrolls)
* 🧠 Smart detection of video title elements using multiple CSS selectors
* 💾 Saves titles in two formats:

  * `complete_playlist_titles.txt` (numbered list with header)
  * `titles_list.txt` (raw titles, one per line)
* 🧱 Built using `Selenium` and supports headless mode
* 🔎 Attempts to click "Load more" if necessary

## ⚙️ How It Works

1. **Browser Setup**:
   Initializes a Chrome browser using Selenium. You can choose between headless (background) or visible browser mode.

2. **Load the Playlist**:
   Navigates to the playlist URL and waits until video items are loaded.

3. **Scroll Mechanism**:
   Repeatedly scrolls down the page and checks if new videos are being loaded. Stops after 5 consecutive scrolls with no new content or after hitting the max scroll limit.

4. **Title Extraction**:
   Uses several CSS selectors and fallback attributes (`title`, `aria-label`, `text`, `alt`) to extract video titles. Filters out duplicates and errors.

5. **Saving Output**:
   Writes two output files with the list of all video titles for easy access and use.

## 📝 Requirements

* Python 3.8+
* Google Chrome installed
* [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/) installed and in your system PATH
* Selenium

Install dependencies:

```bash
pip install selenium
```

## ▶️ Running the Script

Just run:

```bash
python your_script_name.py
```

Then follow the prompt:

* `b` to run headless (faster, no browser UI)
* `s` to show the browser

---
