import os
import json
from playwright.sync_api import sync_playwright

def inspect_award_sites():
    sites = [
        {'id': 'unseen_studio', 'url': 'https://unseen.co/'},
        {'id': 'superlist', 'url': 'https://www.superlist.com/'},
        {'id': 'linear_app', 'url': 'https://linear.app/'},
        {'id': 'koto_studio', 'url': 'https://koto.studio/'}
    ]
    
    out_dir = 'references/award_research'
    os.makedirs(out_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(
            viewport={'width': 1440, 'height': 900},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        )
        
        results = {}
        for s in sites:
            sid = s['id']
            url = s['url']
            print(f'Visiting {sid}: {url}')
            page = context.new_page()
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                page.wait_for_timeout(3500)
                
                # Screenshot
                shot_path = os.path.join(out_dir, f'{sid}.png')
                page.screenshot(path=shot_path, full_page=False)
                
                # Extract visual & architectural metrics
                data = page.evaluate('''() => {
                    const headings = Array.from(document.querySelectorAll('h1, h2')).map(h => ({
                        tag: h.tagName,
                        text: h.innerText.trim().slice(0, 100),
                        fontSize: window.getComputedStyle(h).fontSize,
                        fontWeight: window.getComputedStyle(h).fontWeight,
                        letterSpacing: window.getComputedStyle(h).letterSpacing,
                        lineHeight: window.getComputedStyle(h).lineHeight
                    })).filter(h => h.text.length > 0).slice(0, 6);
                    
                    const buttons = Array.from(document.querySelectorAll('button, a[class*=\"btn\"], a[class*=\"button\"]')).map(b => ({
                        text: b.innerText.trim().slice(0, 40),
                        padding: window.getComputedStyle(b).padding,
                        borderRadius: window.getComputedStyle(b).borderRadius,
                        bgColor: window.getComputedStyle(b).backgroundColor,
                        color: window.getComputedStyle(b).color,
                        boxShadow: window.getComputedStyle(b).boxShadow
                    })).filter(b => b.text.length > 0).slice(0, 5);

                    const rootStyles = window.getComputedStyle(document.body);

                    return {
                        title: document.title,
                        bodyBg: rootStyles.backgroundColor,
                        bodyColor: rootStyles.color,
                        fontFamily: rootStyles.fontFamily,
                        headings: headings,
                        buttons: buttons
                    };
                }''')
                results[sid] = data
                print(f'Done {sid}')
            except Exception as e:
                print(f'Error {sid}: {e}')
            finally:
                page.close()
                
        browser.close()
        
    with open(os.path.join(out_dir, 'award_synthesis.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print('Synthesis written successfully.')

if __name__ == '__main__':
    inspect_award_sites()
