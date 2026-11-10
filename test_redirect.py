import urllib.request

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirect)
req = urllib.request.Request('https://mydollarpilot.com/quiz/results.html', headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = opener.open(req)
    print('Status:', resp.status)
except urllib.error.HTTPError as e:
    print('Code:', e.code)
    print('Location:', e.headers.get('Location'))
    for k, v in e.headers.items():
        print(f'  {k}: {v}')
