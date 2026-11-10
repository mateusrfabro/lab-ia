with open(r'C:\Users\mateu\AppData\Local\npm-cache\_npx\43414d9b790239bb\node_modules\@paperclipai\server\dist\routes\issues.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'router\.post\([^,]+issues', text)]
for idx in matches:
    print(text[idx:idx+400])
    print('='*50)
