from flask import Flask, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

app = Flask(__name__)

# Global driver to keep the browser open
driver = None

def init_driver():
    global driver
    if driver is None:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/launch-vtop')
def launch_vtop():
    """Opens VTOP so you can log in."""
    init_driver()
    driver.get("https://vtopcc.vit.ac.in/vtop/open/page")
    return jsonify({"status": "Browser Opened. Please Log in manually!"})

@app.route('/scrape-data')
def scrape_data():
    """Navigates to pages and scrapes data once you are logged in."""
    global driver
    if not driver:
        return jsonify({"error": "Browser not started"}), 400

    data = {
        "student": {"name": "Fetched User", "regNo": "Fetched ID", "cgpa": "--"}, 
        "attendance": [],
        "hostel": {"block": "--", "room": "--", "mess": "--"}
    }

    try:
        # 1. SCRAPE ATTENDANCE
        # You must navigate to the page. VTOP URLs are dynamic, so we rely on user clicking or menu navigation.
        # Ideally, we automate the menu click, but VTOP menus are tricky. 
        # For this v1, we assume the user is on the dashboard or we try to find the menu.
        
        # Simpler approach: We look at whatever page is open. 
        # But to be useful, let's try to grab the Student Profile info first if available on home screen.
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Try to find Name/RegNo on the dashboard (Sidebar or Topbar)
        # Note: Selectors below are guesses based on standard VTOP structure; might need tweaking.
        try:
            profile_text = soup.find(text=lambda t: "Welcome" in t or "Reg No" in t)
            if profile_text:
                data['student']['name'] = "Found User" # VTOP hides this well
        except:
            pass

        # 2. INSTRUCT USER (The limitation of VTOP Automation)
        # Since VTOP uses dynamic sessions, fully automated navigation often breaks.
        # We will scrape the CURRENT active table on the screen.
        
        tables = pd.read_html(driver.page_source)
        
        # LOGIC: If we find a table that looks like attendance, we parse it.
        for
