import os
import json
from playwright.sync_api import sync_playwright

def inspect_urls():
    targets = [
        {
            'id': 'medium_10_sites',
            'url': 'https://medium.com/@ayushsoni_io/here-are-10-beautifully-designed-well-executed-websites-i-found-this-week-f2539c44383b'
        },
        {
            'id': 'adobe_best_designs',
            'url': 'https://business.adobe.com/blog/basics/best-website-design-examples'
        },
        {
            'id': 'squarespace',
            'url': 'https://www.squarespace.com/'
        }
    ]
    
    out_dir = 'references/deep_research'
    os.makedirs(out_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(
            viewport={'width': 1440, 'height': 900},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        )
        
        for item in targets:
            url_id = item['id']
            url = item['url']
            print(f'=== Researching: {url_id} ({url}) ===')
            page = context.new_page()
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=40000)
                page.wait_for_timeout(4000)
                
                ss_path = os.path.join(out_dir, f'{url_id}.png')
                page.screenshot(path=ss_path, full_page=False)
                print(f'Saved screenshot: {ss_path}')
                
                page_data = page.evaluate('''() => {
                    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4')).map(h => ({
                        tag: h.tagName,
                        text: h.innerText.trim()
                    }));
                    
                    const paragraphs = Array.from(document.querySelectorAll('p, li, blockquote')).map(p => p.innerText.trim()).filter(t => t.length > 20);
                    
                    const links = Array.from(document.querySelectorAll('a')).map(a => ({
                        text: a.innerText.trim(),
                        href: a.href
                    })).filter(l => l.href.startsWith('http'));
                    
                    return {
                        title: document.title,
                        headings: headings.slice(0, 60),
                        sample_paragraphs: paragraphs.slice(0, 50),
                        external_links: links.slice(0, 40)
                    };
                }''')
                
                json_path = os.path.join(out_dir, f'{url_id}.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(page_data, f, indent=2)
                print(f'Saved research JSON: {json_path}')
            except Exception as e:
                print(f'Error inspecting {url}: {e}')
            finally:
                page.close()
                
        browser.close()

if __name__ == '__main__':
    inspect_urls()
