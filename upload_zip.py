import urllib.request

zip_path = r'C:\Users\mateu\Projects\lab-ia\pacotes-prontos-hostinger\PACOTE-2-REWARDEDTASKS-ADSENSE-BR.zip'
with open(zip_path, 'rb') as f:
    data = f.read()

boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="file"; filename="rewardedtasks_br.zip"\r\n'
    f'Content-Type: application/zip\r\n\r\n'
).encode('utf-8') + data + f'\r\n--{boundary}--\r\n'.encode('utf-8')

req = urllib.request.Request('https://0x0.st', data=body, headers={
    'User-Agent': 'curl/7.68.0',
    'Content-Type': f'multipart/form-data; boundary={boundary}'
})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        url = resp.read().decode('utf-8').strip()
        print('Upload 0x0.st SUCCESS:', url)
        with open('zip_live_url.txt', 'w') as out:
            out.write(url)
except Exception as e:
    print('Upload error:', e)
