# TESS Critical Fixes Required

## Immediate Action Required

### 1. orchestrator.py - Add Missing Import
```python
# Line 9 - Add:
from pathlib import Path
```

### 2. main.py - Fix Relative Imports
```python
# Lines 374, 381, 388 - Change FROM:
from .google_setup_wizard import run_google_setup
from .core.notion_client import NotionClient
from .telegram_setup_wizard import run_telegram_setup

# Change TO:
from tess_configurable.google_setup_wizard import run_google_setup
from tess_configurable.core.notion_client import NotionClient
from tess_configurable.telegram_setup_wizard import run_telegram_setup
```

### 3. main.py - Fix Sys.argv Iteration
```python
# Lines 278-294 - Replace with:
for i in range(1, len(sys.argv)):
    arg = sys.argv[i]
    if arg in ('-setup', '-s'):
        sys.argv[i] = '--setup'
    elif arg in ('-settings', '-config'):
        sys.argv[i] = '--settings'
    # ... rest
```

### 4. playwright_browser.py - Fix Resource Cleanup
```python
# Lines 109-120 - Replace close() method:
async def close(self):
    """Close browser."""
    try:
        if self.context:
            await self.context.close()
            self.context = None
    except Exception:
        pass
    try:
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
    except Exception:
        pass
    self.page = None
```

### 5. playwright_browser.py - Fix Sync Wrappers
```python
# Add helper method and update sync wrappers:
import concurrent.futures

def _run_sync(self, coro):
    """Run coroutine safely in any context."""
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, coro)
                return future.result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

def goto_sync(self, url: str, wait_until: str = "networkidle"):
    return self._run_sync(self.goto(url, wait_until))
# ... update other sync wrappers similarly
```

### 6. orchestrator.py - Add Handler Exception Handling
```python
# Lines 338-342 - Replace with:
handler = handlers.get(action_type)
if handler:
    try:
        return handler(action, output, brain)
    except Exception as e:
        error_msg = f"Error in {action_type}: {str(e)}"
        output(f"[ERROR] {error_msg}")
        return error_msg
else:
    return f"Unhandled action type: {action_type}"
```

### 7. playwright_browser.py - Fix WhatsApp Selectors
```python
# Add fallback selector strategy:
CHAT_LIST_SELECTORS = [
    '[data-testid="chat-list"]',
    '[data-testid="conversations"]',
    'div[role="grid"]',
    '#side div[role="list"]',
]

SEARCH_SELECTORS = [
    '[data-testid="chat-list-search"]',
    '[data-testid="search-input"]',
    '[title="Search input textbox"]',
    'div[contenteditable="true"][data-tab="3"]',
]

async def wait_for_any_selector(self, selectors, timeout=10000):
    """Wait for any of the provided selectors."""
    for selector in selectors:
        try:
            return await self.page.wait_for_selector(selector, timeout=timeout // len(selectors))
        except:
            continue
    raise TimeoutError(f"None of the selectors found")
```

### 8. playwright_browser.py - Fix CSS Injection
```python
# Add helper:
def _escape_css_string(self, value: str) -> str:
    """Escape string for use in CSS attribute selector."""
    return value.replace('\\', '\\\\').replace('"', '\\"')

# Usage:
escaped_contact = self._escape_css_string(contact)
contact_selector = f'span[title="{escaped_contact}"]'
```

### 9. playwright_browser.py - Add URL Encoding
```python
# Line 222 - Replace with:
from urllib.parse import quote_plus

async def search(self, query: str) -> str:
    encoded_query = quote_plus(query)
    await self.browser.goto(f"https://www.google.com/search?q={encoded_query}")
```

### 10. brain.py - Add API Key Sanitization
```python
# Add to error handling:
def _sanitize_error(self, error_msg: str) -> str:
    """Remove potential API keys from error messages."""
    import re
    patterns = [
        r'gsk_[a-zA-Z0-9]+',
        r'sk-[a-zA-Z0-9]+',
        r'AIza[a-zA-Z0-9_-]+'
    ]
    for pattern in patterns:
        error_msg = re.sub(pattern, '[REDACTED]', error_msg)
    return error_msg
```

### 11. schemas.py - Add Missing Actions
```python
# Add to schemas.py:
class TripPlannerAction(BaseAction):
    action: Literal["trip_planner_op"]
    destination: str
    dates: Optional[str] = None
    budget: Optional[str] = None

class DocumentAction(BaseAction):
    action: Literal["document_op"]
    sub_action: Literal["extract_text", "summarize", "ocr"]
    path: str

# Add to TessAction union:
TessAction = Union[
    # ... existing ...
    TripPlannerAction,
    DocumentAction,
]
```

## Testing Checklist

After applying fixes:
- [ ] `tess --setup` works without import errors
- [ ] `tess chat with <contact> on whatsapp` works
- [ ] `tess research about <topic>` works
- [ ] `tess convert image.jpg to pdf` works
- [ ] Multiple API key rotation works
- [ ] Error messages don't contain API keys
