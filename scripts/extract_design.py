import sys
import json
import os
from collections import Counter
from playwright.sync_api import sync_playwright

def extract_design_dna(url, output_dir="."):
    print(f"[EXTRACTOR] Launching headless browser for: {url}")
    os.makedirs(output_dir, exist_ok=True)
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="msedge", headless=True)
        except Exception:
            browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception:
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            
        page.wait_for_timeout(2000)
        
        # Take screenshot
        screenshot_path = os.path.join(output_dir, "benchmark_preview.png")
        page.screenshot(path=screenshot_path)
        print(f"[EXTRACTOR] Captured screenshot: {screenshot_path}")
        
        # Extract computed styles across all DOM elements
        js_script = """() => {
            const allElements = document.querySelectorAll('*');
            const data = {
                bgColors: [],
                textColors: [],
                fontFamilies: [],
                fontSizes: [],
                borderRadii: [],
                borders: [],
                boxShadows: [],
                cssVariables: {}
            };
            
            // Extract root CSS variables
            const rootStyle = window.getComputedStyle(document.documentElement);
            for (let i = 0; i < document.styleSheets.length; i++) {
                try {
                    const sheet = document.styleSheets[i];
                    for (let j = 0; j < sheet.cssRules.length; j++) {
                        const rule = sheet.cssRules[j];
                        if (rule.selectorText === ':root' || rule.selectorText === '.dark' || rule.selectorText === 'html') {
                            for (let k = 0; k < rule.style.length; k++) {
                                const prop = rule.style[k];
                                if (prop.startsWith('--')) {
                                    data.cssVariables[prop] = rule.style.getPropertyValue(prop).trim();
                                }
                            }
                        }
                    }
                } catch (e) {}
            }
            
            allElements.forEach(el => {
                const s = window.getComputedStyle(el);
                if (s.display !== 'none' && s.visibility !== 'hidden') {
                    if (s.backgroundColor && s.backgroundColor !== 'rgba(0, 0, 0, 0)') data.bgColors.push(s.backgroundColor);
                    if (s.color) data.textColors.push(s.color);
                    if (s.fontFamily) data.fontFamilies.push(s.fontFamily.split(',')[0].replace(/['"]/g, '').trim());
                    if (s.fontSize) data.fontSizes.push(s.fontSize);
                    if (s.borderRadius && s.borderRadius !== '0px') data.borderRadii.push(s.borderRadius);
                    if (s.border && s.border !== 'none' && !s.border.includes('0px')) data.borders.push(s.border);
                    if (s.boxShadow && s.boxShadow !== 'none') data.boxShadows.push(s.boxShadow);
                }
            });
            
            return data;
        }"""
        
        extracted = page.evaluate(js_script)
        browser.close()
        
    def top_n(lst, n=5):
        return [item for item, _ in Counter(lst).most_common(n)]
        
    dna = {
        "url": url,
        "dominant_bg_colors": top_n(extracted["bgColors"], 6),
        "dominant_text_colors": top_n(extracted["textColors"], 5),
        "primary_fonts": top_n(extracted["fontFamilies"], 4),
        "common_font_sizes": top_n(extracted["fontSizes"], 6),
        "common_border_radii": top_n(extracted["borderRadii"], 6),
        "top_box_shadows": top_n(extracted["boxShadows"], 4),
        "sample_css_vars": dict(list(extracted["cssVariables"].items())[:15])
    }
    
    out_json = os.path.join(output_dir, "extracted_dna.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(dna, f, indent=2)
        
    print(f"[EXTRACTOR] Saved Design DNA to: {out_json}")
    print(json.dumps(dna, indent=2))
    return dna

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_design.py <target_url> [output_dir]")
        sys.exit(1)
    target = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "references"
    extract_design_dna(target, out)
