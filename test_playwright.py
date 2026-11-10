from playwright.sync_api import sync_playwright

test_html = """<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0; background:#000;">
  <div style="position:relative; width:100%; max-width:400px; margin:0 auto; padding-top:125%;">
    <iframe 
      id="vturb-iframe"
      src="https://scripts.converteai.net/f0aeecae-2e61-4c86-8c78-5571d1efbda9/players/6aabfaaad1a5582ed949f5b5/v4/embed.html" 
      style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" 
      allow="autoplay; fullscreen; encrypted-media; picture-in-picture" 
      allowfullscreen>
    </iframe>
  </div>
</body>
</html>
"""

with open("test_vsl_iframe.html", "w", encoding="utf-8") as f:
    f.write(test_html)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("file://" + __file__.replace("\\\\", "/").replace("test_playwright.py", "test_vsl_iframe.html"))
    page.wait_for_timeout(3000)
    
    frame = page.frame_locator("#vturb-iframe")
    print("Frame found")
    # Take screenshot of the player
    page.screenshot(path="player_test.png")
    print("Screenshot saved to player_test.png")
    browser.close()
