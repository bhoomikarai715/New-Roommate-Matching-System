import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the complete matching <script> block at the end (the long one)
pattern = re.compile(r'<script>.*?</script>', re.DOTALL)
scripts = pattern.findall(content)

# Assuming the last one is the large block we want to replace
if scripts:
    content = content.replace(scripts[-1], '<script src="frontend_script.js"></script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html to use external script")
