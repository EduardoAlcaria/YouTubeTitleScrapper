from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import re

def setup_driver(headless=True):

    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        print("Make sure you have Chrome and chromedriver installed")
        return None

def scroll_and_load_all_videos(driver, max_scrolls=1000):
    
    print("Starting to scroll and load all videos...")
    
    last_video_count = 0
    scroll_attempts = 0
    no_change_count = 0
    
    while scroll_attempts < max_scrolls:

        video_elements = driver.find_elements(By.CSS_SELECTOR, 
            'ytd-playlist-video-renderer, .ytd-playlist-video-renderer')
        current_count = len(video_elements)
        
        print(f"Scroll {scroll_attempts + 1}: Found {current_count} videos")
        

        if current_count == last_video_count:
            no_change_count += 1
            if no_change_count >= 5:
                print("No new videos loaded after 5 attempts. Finished loading.")
                break
        else:
            no_change_count = 0
            last_video_count = current_count
        
    
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        

        time.sleep(2)
        
     
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, 
                'ytd-continuation-item-renderer button, .load-more-button')
            if load_more_button.is_displayed():
                driver.execute_script("arguments[0].click();", load_more_button)
                print("Clicked 'Load more' button")
                time.sleep(3)
        except NoSuchElementException:
            pass
        
        scroll_attempts += 1
    
    final_count = len(driver.find_elements(By.CSS_SELECTOR, 
        'ytd-playlist-video-renderer, .ytd-playlist-video-renderer'))
    print(f"Finished scrolling. Total videos loaded: {final_count}")
    
    return final_count

def extract_all_titles(driver):
  
    print("Extracting video titles...")

    title_selectors = [
        'ytd-playlist-video-renderer #video-title',
        '.ytd-playlist-video-renderer #video-title',
        'ytd-playlist-video-renderer a#video-title',
        '.ytd-playlist-video-renderer a#video-title',
        'ytd-playlist-video-renderer .title a',
        'h3 a#video-title',
        'a#video-title',
    ]
    
    titles = []
    title_elements = []
    
    for selector in title_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                title_elements = elements
                print(f"Found {len(elements)} titles using selector: {selector}")
                break
        except Exception as e:
            continue
    
    if not title_elements:
        print("Could not find video title elements. Trying alternative approach...")

        title_elements = driver.find_elements(By.CSS_SELECTOR, '[title], [aria-label*="video"]')
    
    for i, element in enumerate(title_elements, 1):
        try:
            title = None
            
    
            title = element.get_attribute('title')
            if not title:
                title = element.get_attribute('aria-label')
            if not title:
                title = element.text
            if not title:
                title = element.get_attribute('alt')
            
            if title and title.strip() and len(title.strip()) > 1:
            
                clean_title = re.sub(r'\s+', ' ', title.strip())
                if clean_title not in titles: 
                    titles.append(clean_title)
                    
        except Exception as e:
            print(f"Error extracting title from element {i}: {e}")
            titles.append(f'[Error extracting title {i}]')
    

    unique_titles = []
    seen = set()
    for title in titles:
        if title not in seen:
            unique_titles.append(title)
            seen.add(title)
    
    return unique_titles

def main():
    playlist_url = "https://www.youtube.com/playlist?list=PLN39y5i_H0FlTkHw4iOCD-OVUuf993MZn"
    
    print("YouTube Playlist Complete Scraper")
    print("This will open a browser and scroll through the ENTIRE playlist")
    print("to get ALL video titles (may take several minutes for large playlists)\n")
    
    headless_choice = input("Run in background (faster) or show browser window? (b/s): ").lower()
    headless = headless_choice.startswith('b')
    
    driver = setup_driver(headless=headless)
    if not driver:
        return
    
    try:
        print(f"Loading playlist: {playlist_url}")
        driver.get(playlist_url)
        
        # Wait for page to load
        print("Waiting for page to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-playlist-video-renderer, .playlist-video"))
        )
        
    
        total_videos = scroll_and_load_all_videos(driver)
        
  
        titles = extract_all_titles(driver)
        
        if titles:
            print(f"\nSuccessfully extracted {len(titles)} video titles!\n")
            
     
            for i, title in enumerate(titles, 1):
                print(f"{i:4d}. {title}")
            
                 
            with open("complete_playlist_titles.txt", "w", encoding="utf-8") as f:
                f.write(f"Complete YouTube Playlist Titles (Total: {len(titles)})\n")
                f.write("=" * 70 + "\n\n")
                for i, title in enumerate(titles, 1):
                    f.write(f"{i:4d}. {title}\n")
            
            print(f"\nAll {len(titles)} titles saved to 'complete_playlist_titles.txt'")
   
            with open("titles_list.txt", "w", encoding="utf-8") as f:
                for title in titles:
                    f.write(f"{title}\n")
            print("Titles also saved to 'titles_list.txt' (one per line)")
            
        else:
            print("No titles were extracted. There might be an issue with the page structure.")
            
    except TimeoutException:
        print("Timeout waiting for page to load. The playlist might be private or unavailable.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()