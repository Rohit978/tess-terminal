"""
WhatsApp Client - Send messages and monitor chats.
Uses Selenium for WhatsApp Web.
"""

import time
import threading
from typing import Optional, Callable


class WhatsAppClient:
    """
    WhatsApp Web automation client.
    """
    
    def __init__(self, brain=None):
        self.brain = brain
        self.driver = None
        self.logged_in = False
        self.message_queue = []
    
    def _ensure_driver(self):
        """Initialize WebDriver."""
        if self.driver:
            return True
        
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            options = Options()
            # WhatsApp needs visible browser for QR scan
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-tools")
            options.add_argument("--remote-debugging-port=0")
            
            # Keep user data for session persistence
            from pathlib import Path
            user_data = Path.home() / ".tess" / "whatsapp_session"
            user_data.mkdir(parents=True, exist_ok=True)
            options.add_argument(f"--user-data-dir={user_data}")
            
            # Additional stability options
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            return True
            
        except Exception as e:
            print(f"WhatsApp driver error: {e}")
            return False
    
    def login(self) -> str:
        """Open WhatsApp Web and wait for QR scan."""
        if not self._ensure_driver():
            return "Failed to initialize browser"
        
        try:
            self.driver.get("https://web.whatsapp.com")
            print("Waiting for QR code scan...")
            
            # Wait for chat list to appear (logged in)
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            try:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='grid']"))
                )
                self.logged_in = True
                return "Logged in successfully!"
            except:
                return "Login timeout - please scan QR code"
                
        except Exception as e:
            return f"Login error: {e}"
    
    def find_chat(self, contact: str) -> bool:
        """Find and open a chat."""
        if not self.driver:
            return False
        
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            
            # Click search box
            search = self.driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
            search.click()
            search.clear()
            search.send_keys(contact)
            time.sleep(1)
            search.send_keys(Keys.ENTER)
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"Find chat error: {e}")
            return False
    
    def send_message(self, contact: str, message: str) -> str:
        """Send message to contact."""
        if not self.logged_in:
            result = self.login()
            if "error" in result.lower():
                return result
        
        try:
            if not self.find_chat(contact):
                return f"Could not find chat with {contact}"
            
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            
            # Find input box
            input_box = self.driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='1']")
            input_box.click()
            
            # Type message
            input_box.send_keys(message)
            time.sleep(0.5)
            
            # Send
            input_box.send_keys(Keys.ENTER)
            
            return f"Message sent to {contact}"
            
        except Exception as e:
            return f"Send error: {e}"
    
    def monitor_loop(self, contact: str, mission: Optional[str] = None, 
                     stop_event: Optional[threading.Event] = None):
        """
        Monitor a chat for new messages.
        
        Args:
            contact: Contact to monitor
            mission: Optional AI mission (auto-reply logic)
            stop_event: Threading event to stop monitoring
        """
        if not self.logged_in:
            self.login()
        
        if not self.find_chat(contact):
            print(f"Could not find chat with {contact}")
            return
        
        print(f"Monitoring chat with {contact}...")
        
        last_messages = set()
        
        try:
            from selenium.webdriver.common.by import By
            
            while not (stop_event and stop_event.is_set()):
                # Get messages
                messages = self.driver.find_elements(By.CSS_SELECTOR, "div.message-in, div.message-out")
                
                for msg in messages[-5:]:  # Check last 5
                    msg_id = msg.get_attribute("data-id")
                    if msg_id and msg_id not in last_messages:
                        last_messages.add(msg_id)
                        
                        try:
                            text_elem = msg.find_element(By.CSS_SELECTOR, "span.selectable-text")
                            text = text_elem.text
                            
                            # Check if incoming
                            if "message-in" in msg.get_attribute("class"):
                                print(f"[{contact}]: {text}")
                                
                                # AI response if mission specified
                                if mission and self.brain:
                                    response = self._generate_response(text, mission)
                                    if response:
                                        self.send_message(contact, response)
                        except:
                            pass
                
                time.sleep(2)
                
        except Exception as e:
            print(f"Monitor error: {e}")
    
    def _generate_response(self, incoming_msg: str, mission: str) -> Optional[str]:
        """Generate AI response to incoming message."""
        if not self.brain:
            return None
        
        prompt = f"""Mission: {mission}

Incoming message: "{incoming_msg}"

Generate a brief, natural response:"""
        
        try:
            response = self.brain.think(prompt)
            return response.strip() if response else None
        except:
            return None
    
    def close(self):
        """Close browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None
