from playwright.sync_api import sync_playwright
import os

file_path = os.path.abspath(r"c:\Users\mateu\Projects\rewarded-tasks\app-facebook\index.html")
url = "file:///" + file_path.replace("\\", "/") + "?pitch=true"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    
    print("Navigating to:", url)
    page.goto(url)
    page.wait_for_timeout(1000)
    
    # Click with force=True
    print("Step 0: Clicking Start...")
    page.click("#btn-start", force=True)
    page.wait_for_timeout(1000)
    
    # Verify Task 1 (Amazon)
    text = page.inner_text("#task-post-container")
    assert "Amazon.com" in text, "Task 1 Amazon not found!"
    print("Task 1 Amazon verified. Answering...")
    page.click("button:has-text('Relevant')", force=True)
    page.wait_for_timeout(600)
    
    print("Clicking Continue in Reward Modal 1...")
    page.click("#modal-reward button", force=True)
    page.wait_for_timeout(600)
    
    # Task 2 (Apple)
    text = page.inner_text("#task-post-container")
    assert "Apple" in text, "Task 2 Apple not found!"
    print("Task 2 Apple verified. Answering...")
    page.click("button:has-text('Relevant')", force=True)
    page.wait_for_timeout(600)
    
    print("Clicking Continue in Reward Modal 2...")
    page.click("#modal-reward button", force=True)
    page.wait_for_timeout(600)
    
    # Task 3 (Starbucks)
    text = page.inner_text("#task-post-container")
    assert "Starbucks" in text, "Task 3 Starbucks not found!"
    print("Task 3 Starbucks verified. Answering...")
    page.click("button:has-text('Relevant')", force=True)
    page.wait_for_timeout(600)
    
    print("Clicking Continue in Reward Modal 3...")
    page.click("#modal-reward button", force=True)
    page.wait_for_timeout(2000)
    
    # Step 4: VSL Screen
    print("Step 4 reached! Checking VSL screen...")
    assert page.is_visible("#screen-vsl"), "VSL screen is not visible!"
    
    push_text = page.inner_text("#push-notification")
    print("Push banner text:", push_text.replace("\n", " "))
    assert "FACEBOOK WALLET" in push_text, "Push banner FACEBOOK WALLET not found!"
    
    cta_visible = page.is_visible("#cta-pitch-container")
    assert cta_visible, "CTA Pitch Button not visible with ?pitch=true!"
    checkout_href = page.get_attribute("#btn-checkout", "href")
    print("Checkout CTA button URL:", checkout_href)
    assert "checkout.cooud.com/01M32DGN4ZTTHTAM6456KCRKJE" in checkout_href
    
    iframe_src = page.get_attribute("#vturb-vsl-frame", "src")
    print("Iframe src:", iframe_src)
    assert "converteai.net" in iframe_src
    
    page.screenshot(path="full_flow_vsl_verified.png")
    print("Screenshot saved to full_flow_vsl_verified.png!")
    print(">>> SUCCESS: 100% COMPLETE VERIFICATION PASSED! <<<")
    browser.close()
