import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class VTOPBackend:
    def __init__(self):
        print("Initializing VTOP Backend... 🚀")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.base_url = "https://vtopcc.vit.ac.in/vtop/open/page"
    
    def login_and_start(self):
        """Opens VTOP and waits for the user to manually log in."""
        print(f"Opening {self.base_url}...")
        self.driver.get(self.base_url)
        print("\n" + "="*50)
        print("ACTION REQUIRED: Please manually log in to VTOP in the browser window.")
        print("The Captcha is the final boss here, so I'll let you handle it. 😉")
        print("Once you are on the Dashboard (Home Page), press ENTER here to continue.")
        print("="*50 + "\n")
        input("Press Enter after you have successfully logged in...")

    def scrape_tables(self, page_name):
        """Scrapes all tables from the current page and returns them as DataFrames."""
        print(f"\n🔍 Scraping data for: {page_name}...")
        
        # specific wait to ensure table loads
        time.sleep(2) 
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        tables = soup.find_all('table')
        
        if not tables:
            print(f"⚠️ No tables found on the {page_name} page.")
            return None
        
        data_frames = []
        for i, table in enumerate(tables):
            try:
                # pandas reads html tables directly
                df = pd.read_html(str(table))[0]
                data_frames.append(df)
            except Exception as e:
                print(f"Could not parse table {i}: {e}")
        
        return data_frames

    def get_user_data(self):
        """Orchestrates the navigation and data fetching."""
        try:
            self.login_and_start()

            # 1. ATTENDANCE
            print("\n👉 Please Navigate to the 'Attendance' page in the browser.")
            input("Press Enter once the Attendance table is visible...")
            attendance_data = self.scrape_tables("Attendance")
            if attendance_data:
                print("\n✅ ATTENDANCE SUMMARY:")
                # Usually the main attendance is the last or largest table
                for df in attendance_data:
                    if len(df) > 1: # Filter out tiny layout tables
                        print(df.to_string())
                        print("-" * 20)

            # 2. CGPA / GRADES
            print("\n👉 Please Navigate to the 'Grades' / 'History of Grades' page.")
            input("Press Enter once the Grades table is visible...")
            grade_data = self.scrape_tables("Grades/CGPA")
            if grade_data:
                print("\n✅ ACADEMIC HISTORY (CGPA):")
                for df in grade_data:
                    print(df.head()) # Showing head to avoid spamming console
                    print("-" * 20)

            # 3. MESS / HOSTEL
            print("\n👉 Please Navigate to the 'Hostel' or 'Mess' details page.")
            input("Press Enter once the details are visible...")
            hostel_data = self.scrape_tables("Hostel/Mess")
            if hostel_data:
                print("\n✅ HOSTEL & MESS DETAILS:")
                for df in hostel_data:
                    print(df.to_string())
            
            print("\n🎉 Data extraction complete! You can close the browser.")

        except Exception as e:
            print(f"❌ An error occurred: {e}")
        finally:
            # self.driver.quit() # Uncomment to auto-close browser
            pass

if __name__ == "__main__":
    backend = VTOPBackend()
    backend.get_user_data()
