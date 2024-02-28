from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from ytmusicapi import YTMusic

from typing import List, Set
from config import *



import time


class SpotifyToYoutube:
    def __init__(self):
        # ---------------- SETUP
        self.ytmusic_instance = YTMusic("oauth.json")
        self.service = webdriver.chrome.service.Service(executable_path="../chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service)
        
    def accept_cookies(self):
      # Waits for the cookie banner to be located
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, COOKIE_BANNER_CLOSE_CLASSNAME))
        ).click()

    def login_with_facebook(self, email, password):
      # Waits for the facebook method button to be located
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, FACEBOOK_METHOD_XPATH))
        ).click()
        
        # Waits for the email input to be located and types the email

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, FACEBOOK_EMAIL_INPUT_ID))
        ).send_keys(email)
        
       # Same with the password
       

        self.driver.find_element(By.ID, FACEBOOK_PASSWORD_INPUT_ID).send_keys(password + Keys.ENTER)
        
    def login_with_spotify(self, email, password):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ALREADY_HAVE_ACCOUNT_XPATH))
        ).click()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, LOGIN_USERNAME_ID))
        ).send_keys(email)   
        
    
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, LOGIN_PASSWORD_ID))
        ).send_keys(password)
        
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, LOGIN_BUTTON_ID))
        ).click()
        
   
        
    def loop_through_albums(self):
      # Find the album container (the left side)
        albums = self.driver.find_elements(By.CLASS_NAME, ALBUMS_CONTAINER_CLASSNAME)
        albums_urls: List[str] = []

      # For each album in the album container, click it, append its url to the albums_url object
      # Go back and to the same with the following album
        print("Looping through all the albums...")
        for album in albums:
            album.click()
            albums_urls.append(self.driver.current_url)
            self.driver.back()
            
        print(albums_urls)    
            
            
        # We were having problems when storing the elements into an empty [] 
        # so we are using a set to have unique elements 
        unique_songs_names: Set[str] = set() 

        # For each album url, get it
        print("Doing all the process to transfer your albums to youtube music...\n ")
        for album_url in albums_urls:
            self.driver.get(album_url)
            time.sleep(2)  # Espera 2 segundos (ajusta el tiempo según sea necesario)


        # Wait for the songs container to be located
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, SONGS_CONTAINER_CLASSNAME))
            )
            
            try:
    # Find the songs container
                album_songs_name = self.driver.find_elements(By.CLASS_NAME, SONGS_CONTAINER_CLASSNAME)
                 # For each song in the songs container, add its name to the unique_songs_name set
                for song in album_songs_name:
                    unique_songs_names.add(song.text)
            except TimeoutException as te:
                print(f"Timed out waiting for songs container: {str(te)}")
            except Exception as e:
                print(f"Error finding songs container: {str(e)}")

        print(unique_songs_names)    
        print(len(unique_songs_names))    
           
                

        try:
          # Create the playlist
            playlist_with_albums = self.ytmusic_instance.create_playlist(title="Spotify to Youtube Playlist", description="Spotify to Youtube playlist")
            print("Playlist on Youtube Music created\n")
        except Exception as e:
            print(f"Error creating playlist: {str(e)}")

        # For each song in the unique_songs_names set
        print("Transferring songs...")
        
        for song in unique_songs_names:
            try:
                self.driver.implicitly_wait(2)
              
                # Search the song on Youtube
                search_results = self.ytmusic_instance.search(query=song, filter="videos", limit=5)
               
                # Add the song to the playlist we created before
                self.ytmusic_instance.add_playlist_items(playlistId=playlist_with_albums, videoIds=[search_results[0]["videoId"]])
                      
            except Exception as e:
                print(f"Error adding song '{song}' with the ID of '{search_results[0]["videoId"]}' to playlist: {str(e)}")
        
        print(playlist_with_albums)         

    def main(self):
      # Initialize the service and execute the webdriver
        print(" \n")
        print(" \n")
        print("Welcome to the Spotify to Youtube Music tool.\n")
        print("It will create a playlist on Youtube Music with the albums that you've liked on your Spotify account\n")
        
        
        
        try:
            self.driver.get("https://spotify.com")
            
            time.sleep(2)
            
            self.accept_cookies()
            print("Cookies accepted.\n")

            # Wait for the login button to be located and then click it
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, LOGIN_BUTTON_CLASSNAME))
            ).click()
            
            
            
            while True:
                user_choose = int(input("Which log in method will you use? Type 1 for Spotify, 2 for Facebook: "))
                email = input("Type your email here: ")
                password = input("Type your password here: ")
    
                if user_choose == 1:
                    self.login_with_spotify(email, password)
                    break
                if user_choose == 2:
                    self.login_with_facebook("jesusdavidmorales199@gmail.com", "420123Ce.")
                    break
                else:
                    print("Invalid choice. Please type 1 for Spotify or 2 for Facebook.")

            # Wait for the album container to be located
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, ALBUMS_CONTAINER_CLASSNAME))
            )
            
            # Looping through the albums
            self.loop_through_albums()

            time.sleep(2)
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    app = SpotifyToYoutube()
    app.main()
