"""
Playwright Browser - Modern browser automation.
Replaces Selenium with Playwright for better reliability.
"""

import asyncio
from typing import Optional, Dict, Any
from pathlib import Path


class PlaywrightBrowser:
    """
    Modern browser automation using Playwright.
    More reliable than Selenium for web apps like WhatsApp Web.
    """
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
    
    async def _init(self):
        """Initialize Playwright."""
        if self.browser:
            return
        
        try:
            from playwright.async_api import async_playwright
            
            self.playwright = await async_playwright().start()
            
            # Launch Chromium with stealth options
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--single-process',  # Required for some environments
                    '--disable-gpu'
                ]
            )
            
            # Create context with persistent storage
            from ..config_manager import get_config_manager
            config = get_config_manager()
            user_data = Path(config.config.paths.data_dir) / "browser_data"
            user_data.mkdir(parents=True, exist_ok=True)
            
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_data_dir=str(user_data),
                permissions=['notifications']
            )
            
            self.page = await self.context.new_page()
            
        except ImportError:
            raise ImportError("Playwright not installed. Run: pip install playwright && playwright install chromium")
    
    async def goto(self, url: str, wait_until: str = "networkidle"):
        """Navigate to URL."""
        await self._init()
        await self.page.goto(url, wait_until=wait_until)
    
    async def click(self, selector: str, timeout: int = 5000):
        """Click element with auto-wait."""
        await self.page.click(selector, timeout=timeout)
    
    async def fill(self, selector: str, text: str, timeout: int = 5000):
        """Fill input field."""
        await self.page.fill(selector, text, timeout=timeout)
    
    async def type(self, selector: str, text: str, delay: int = 50):
        """Type text with human-like delay."""
        await self.page.type(selector, text, delay=delay)
    
    async def get_text(self, selector: str, timeout: int = 5000) -> str:
        """Get element text content."""
        element = await self.page.wait_for_selector(selector, timeout=timeout)
        return await element.text_content() if element else ""
    
    async def get_inner_html(self, selector: str) -> str:
        """Get element inner HTML."""
        return await self.page.inner_html(selector)
    
    async def wait_for_selector(self, selector: str, timeout: int = 10000):
        """Wait for element to appear."""
        return await self.page.wait_for_selector(selector, timeout=timeout)
    
    async def wait_for_navigation(self, timeout: int = 10000):
        """Wait for page navigation."""
        await self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    async def screenshot(self, path: str):
        """Take screenshot."""
        await self.page.screenshot(path=path, full_page=True)
    
    async def evaluate(self, script: str) -> Any:
        """Execute JavaScript."""
        return await self.page.evaluate(script)
    
    async def get_cookies(self) -> list:
        """Get all cookies."""
        return await self.context.cookies()
    
    async def close(self):
        """Close browser."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    # ===== Sync wrappers for easier use =====
    
    def goto_sync(self, url: str, wait_until: str = "networkidle"):
        return asyncio.run(self.goto(url, wait_until))
    
    def click_sync(self, selector: str, timeout: int = 5000):
        return asyncio.run(self.click(selector, timeout))
    
    def fill_sync(self, selector: str, text: str, timeout: int = 5000):
        return asyncio.run(self.fill(selector, text, timeout))
    
    def get_text_sync(self, selector: str, timeout: int = 5000) -> str:
        return asyncio.run(self.get_text(selector, timeout))
    
    def screenshot_sync(self, path: str):
        return asyncio.run(self.screenshot(path))


class WhatsAppPlaywright:
    """
    WhatsApp Web using Playwright - more reliable than Selenium.
    """
    
    def __init__(self, brain=None):
        self.brain = brain
        self.browser = PlaywrightBrowser(headless=False)
        self.logged_in = False
    
    async def login(self) -> str:
        """Login to WhatsApp Web."""
        try:
            await self.browser.goto("https://web.whatsapp.com")
            
            # Wait for QR code scan (user needs to scan)
            # Check if logged in by looking for chat list
            try:
                await self.browser.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
                self.logged_in = True
                return "✓ Logged in successfully!"
            except:
                return "⚠ QR code not scanned within 60 seconds"
                
        except Exception as e:
            return f"Login error: {e}"
    
    async def send_message(self, contact: str, message: str) -> str:
        """Send message to contact."""
        if not self.logged_in:
            result = await self.login()
            if "error" in result.lower():
                return result
        
        try:
            # Search for contact
            search_selector = '[data-testid="chat-list-search"]'  # or '[title="Search input textbox"]'
            await self.browser.fill(search_selector, contact)
            await asyncio.sleep(1)
            
            # Click on contact
            contact_selector = f'span[title="{contact}"]'
            await self.browser.click(contact_selector)
            await asyncio.sleep(1)
            
            # Type message
            input_selector = '[data-testid="conversation-compose-box-input"]'  # or 'div[contenteditable="true"]'
            await self.browser.type(input_selector, message)
            
            # Send (press Enter)
            from playwright.async_api import async_playwright
            page = self.browser.page
            await page.press(input_selector, "Enter")
            
            return f"✓ Message sent to {contact}"
            
        except Exception as e:
            return f"Send error: {e}"
    
    async def close(self):
        """Close browser."""
        await self.browser.close()
    
    # Sync wrappers
    def login_sync(self) -> str:
        return asyncio.run(self.login())
    
    def send_message_sync(self, contact: str, message: str) -> str:
        return asyncio.run(self.send_message(contact, message))


class WebSearchPlaywright:
    """
    Web search using Playwright.
    """
    
    def __init__(self):
        self.browser = PlaywrightBrowser(headless=True)
    
    async def search(self, query: str) -> str:
        """Search Google and return results."""
        try:
            await self.browser.goto(f"https://www.google.com/search?q={query}")
            
            # Wait for results
            await self.browser.wait_for_selector("#search", timeout=10000)
            
            # Extract results
            page = self.browser.page
            
            # Get search results
            results = await page.query_selector_all("div.g")
            output = []
            
            for i, result in enumerate(results[:5], 1):
                try:
                    title_elem = await result.query_selector("h3")
                    title = await title_elem.text_content() if title_elem else "No title"
                    
                    snippet_elem = await result.query_selector("div.VwiC3b")
                    snippet = await snippet_elem.text_content() if snippet_elem else ""
                    
                    output.append(f"{i}. {title}\n{snippet[:150]}...")
                except:
                    continue
            
            return "\n\n".join(output) if output else "No results found"
            
        except Exception as e:
            return f"Search error: {e}"
        finally:
            await self.browser.close()
    
    def search_sync(self, query: str) -> str:
        return asyncio.run(self.search(query))


# Factory function to migrate gradually
def get_browser(use_playwright: bool = False):
    """Get browser instance. Set use_playwright=True to use new system."""
    if use_playwright:
        return PlaywrightBrowser()
    else:
        # Fallback to old Selenium WebBrowser
        from .web_browser import WebBrowser
        return WebBrowser()
