import urllib.request
import re

req = urllib.request.Request('https://mydollarpilot.com/', headers={'User-Agent': 'Mozilla/5.0'})
content = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

scripts = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', content)
links = re.findall(r'<link[^>]*href=[\'"]([^\'"]+)[\'"]', content)
print('Homepage Scripts:', scripts)
print('Homepage Links:', links)

req_quiz = urllib.request.Request('https://mydollarpilot.com/quiz/results', headers={'User-Agent': 'Mozilla/5.0'})
quiz_content = urllib.request.urlopen(req_quiz).read().decode('utf-8', errors='ignore')
quiz_scripts = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', quiz_content)
quiz_links = re.findall(r'<link[^>]*href=[\'"]([^\'"]+)[\'"]', quiz_content)
print('Quiz Scripts:', quiz_scripts)
print('Quiz Links:', quiz_links)
