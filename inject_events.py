import re

# Read the generated events HTML
with open('events_section.html', 'r') as f:
    events_html = f.read()

# Read index.html
with open('index.html', 'r') as f:
    index_html = f.read()

# Replace the events container content
pattern = r'<div id="events-container">.*?</div>'
replacement = f'<div id="events-container">\n{events_html}\n            </div>'
new_html = re.sub(pattern, replacement, index_html, flags=re.DOTALL)

# Write back to index.html
with open('index.html', 'w') as f:
    f.write(new_html)

print("Injected events into index.html")
