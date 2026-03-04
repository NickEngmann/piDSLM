#!/usr/bin/env python3
"""Fix for piDSLM busy window initialization issue.

This script patches the pidslm.py file to ensure the busy window is properly
initialized and hidden by default, fixing the test failures related to
self.busy not being properly set up.
"""

import re

# Read the original file
with open('pidslm.py', 'r') as f:
    content = f.read()

# Find and replace the busy window initialization section
# The fix ensures busy is properly initialized and hidden
old_pattern = r'(self\.busy = Window\(self\.app, width=400, height=300, bg="#000000"\)\n.*?self\.busy_image = Picture\(self\.busy, name="busy\.gif"\))'

new_code = '''self.busy = Window(self.app, width=400, height=300, bg="#000000")
        self.busy_title = Text(self.busy, text="Processing...", size=20, color="white")
        self.busy_image = Picture(self.busy, name="busy.gif")
        self.busy.hide()  # Hide busy window initially'''

# Apply the fix
content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

# Write the fixed file
with open('pidslm.py', 'w') as f:
    f.write(content)

print("Fixed pidslm.py - busy window now properly initialized and hidden")
