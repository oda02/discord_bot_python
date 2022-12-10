from urllib.parse import urlparse
from urllib.parse import parse_qs
url = 'https://youtu.be/ITdwRAc9CyY?list=PL_owtWwcLVIFOyaQ4b_szof6MeBvDHEZj&t=1904'
parsed_url = urlparse(url)
captured_value = parse_qs(parsed_url.query)['ts'][0]
print(captured_value)