import subprocess
import os

with open("test_app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Let's use node to check syntax error line
# Node has vm.Script
script = """
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync('test_app.js', 'utf8');
try {
  new vm.Script(code, { filename: 'test_app.js' });
  console.log('Valid JS!');
} catch (err) {
  console.log('Error name:', err.name);
  console.log('Error message:', err.message);
  console.log('Stack:', err.stack);
}
"""

with open("check_node.js", "w", encoding="utf-8") as f:
    f.write(script)

res = subprocess.run(["node", "check_node.js"], capture_output=True, text=True)
print(res.stdout)
print(res.stderr)
