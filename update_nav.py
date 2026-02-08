#!/usr/bin/env python3
"""Script to update navigation on all HTML files (excluding index.html)."""

import os
import glob
import re

WEBSITE_DIR = "/Users/admin/Downloads/JRNY Website"

# Get all HTML files except index.html
html_files = [f for f in glob.glob(os.path.join(WEBSITE_DIR, "*.html")) if not f.endswith("index.html")]
html_files.sort()

print(f"Found {len(html_files)} HTML files to update.\n")

success_count = 0
error_files = []

NAV_PHONE_SVG = '''            <a href="tel:0412345678" class="nav-phone">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 5px;">
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                </svg>
                (04) 1234 5678
            </a>'''

MOBILE_NAV_RIGHT_HTML = '''        <!-- Mobile Nav Right (Phone + Hamburger) -->
        <div class="mobile-nav-right">
            <a href="tel:0412345678" class="mobile-nav-phone" aria-label="Call us">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                </svg>
            </a>
            <button class="mobile-menu-toggle" aria-label="Toggle menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>'''

MOBILE_NAV_RIGHT_CSS = '''        .mobile-nav-right {
            display: none;
            align-items: center;
            gap: 15px;
        }

        .mobile-nav-phone {
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .mobile-nav-phone:hover {
            background: rgba(245, 166, 35, 0.2);
            color: #F5A623;
        }

'''

NAV_PHONE_CSS = '''        .nav-phone {
            color: #ffffff;
            text-decoration: none;
            font-size: 14px;
            display: flex;
            align-items: center;
            transition: color 0.3s ease;
        }

        .nav-phone:hover {
            color: #F5A623;
        }

'''

for filepath in html_files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes_made = []

    # =====================
    # HTML CHANGE 1: Add phone number to nav-links
    # Use regex to handle both blog.html">Resources and blog.html" class="active">Resources
    # Only match the first occurrence (desktop nav with nav-cta, not mobile with mobile-menu-cta)
    # =====================
    pattern1 = re.compile(
        r'(            <a href="blog\.html"(?:\s+class="active")?>Resources</a>)\n'
        r'(        </div>\n'
        r'        <a href="contact-us\.html" class="nav-cta">Get Free Strategy Session</a>)'
    )
    match1 = pattern1.search(content)
    if match1:
        replacement1 = match1.group(1) + '\n' + NAV_PHONE_SVG + '\n' + match1.group(2)
        content = content[:match1.start()] + replacement1 + content[match1.end():]
        changes_made.append("HTML1: Added nav-phone to nav-links")
    else:
        changes_made.append("HTML1: PATTERN NOT FOUND")

    # =====================
    # HTML CHANGE 2: Wrap hamburger with mobile-nav-right
    # Try with comment first, then without
    # =====================
    old_html2_with_comment = '        <!-- Mobile Menu Toggle Button -->\n        <button class="mobile-menu-toggle" aria-label="Toggle menu">\n            <span></span>\n            <span></span>\n            <span></span>\n        </button>'

    old_html2_without_comment = '        <button class="mobile-menu-toggle" aria-label="Toggle menu">\n            <span></span>\n            <span></span>\n            <span></span>\n        </button>'

    if old_html2_with_comment in content:
        content = content.replace(old_html2_with_comment, MOBILE_NAV_RIGHT_HTML, 1)
        changes_made.append("HTML2: Wrapped hamburger (with comment)")
    elif old_html2_without_comment in content:
        content = content.replace(old_html2_without_comment, MOBILE_NAV_RIGHT_HTML, 1)
        changes_made.append("HTML2: Wrapped hamburger (without comment)")
    else:
        changes_made.append("HTML2: PATTERN NOT FOUND")

    # =====================
    # CSS CHANGE 1: Add mobile-nav-right and mobile-nav-phone styles before .mobile-menu-toggle
    # =====================
    old_css1 = '        .mobile-menu-toggle {\n            display: none;\n            flex-direction: column;\n            justify-content: center;\n            align-items: center;\n            width: 44px;'

    if old_css1 in content:
        content = content.replace(old_css1, MOBILE_NAV_RIGHT_CSS + old_css1, 1)
        changes_made.append("CSS1: Added mobile-nav-right/phone styles")
    else:
        changes_made.append("CSS1: PATTERN NOT FOUND")

    # =====================
    # CSS CHANGE 2: Add mobile-nav-right display in mobile media query
    # =====================
    old_css2 = '            .mobile-menu-toggle {\n                display: flex;\n            }'

    new_css2 = '            .mobile-nav-right {\n                display: flex;\n            }\n\n            .mobile-menu-toggle {\n                display: flex;\n            }'

    if old_css2 in content:
        content = content.replace(old_css2, new_css2, 1)
        changes_made.append("CSS2: Added mobile-nav-right display in media query")
    else:
        changes_made.append("CSS2: PATTERN NOT FOUND")

    # =====================
    # CSS CHANGE 3: Add .nav-phone styles before .nav-cta
    # Handle both multi-line and single-line .nav-cta format
    # =====================
    # Multi-line format: "        .nav-cta {\n"
    old_css3_multiline = '        .nav-cta {\n'
    # Single-line format: "        .nav-cta { background-color:"
    old_css3_singleline_pattern = re.compile(r'(        \.nav-cta \{ )')

    if old_css3_multiline in content:
        content = content.replace(old_css3_multiline, NAV_PHONE_CSS + '        .nav-cta {\n', 1)
        changes_made.append("CSS3: Added nav-phone styles (multi-line)")
    elif old_css3_singleline_pattern.search(content):
        content = old_css3_singleline_pattern.sub(NAV_PHONE_CSS + r'\1', content, count=1)
        changes_made.append("CSS3: Added nav-phone styles (single-line)")
    else:
        changes_made.append("CSS3: PATTERN NOT FOUND")

    # Check for any issues
    had_errors = any("NOT FOUND" in c for c in changes_made)

    if had_errors:
        error_files.append((filename, changes_made))
        print(f"  WARNING {filename}:")
        for c in changes_made:
            print(f"    {c}")
    else:
        success_count += 1

    # Write the updated content
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK {filename}: {len(changes_made)} changes")
    else:
        print(f"  SKIP {filename}: No changes made")

print(f"\n{'='*60}")
print(f"Summary: {success_count}/{len(html_files)} files fully updated.")
if error_files:
    print(f"\nFiles with issues ({len(error_files)}):")
    for fn, changes in error_files:
        print(f"  {fn}:")
        for c in changes:
            if "NOT FOUND" in c:
                print(f"    ** {c}")
            else:
                print(f"    {c}")
