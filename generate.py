import requests
import json
from datetime import datetime
import pytz
import os

# API URL (hidden in GitHub Secrets)
url = os.getenv("API_URL")

if not url:
    print("❌ API_URL not set. Please add it as GitHub Secret.")
    exit()

try:
    response = requests.get(url, verify=False, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
    exit()
except json.JSONDecodeError:
    print("Failed to decode JSON response.")
    exit()

if not data or data.get("res_code") != "0000":
    print("Failed to fetch or parse data.")
    exit()

tz = pytz.timezone("Asia/Bangkok")
now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S") + " UTC+07 ICT"

output_file = "FREETV.m3u"

with open(output_file, "w", encoding="utf-8") as f:
    # Header
    f.write(f"""#EXTM3U url-tvg="https://akkradet.github.io/IPTV-THAI/guide.xml" refresh="3600"

# =======================================================
# Last Update: {now}
# =======================================================

""")

    # Channel list
    for channel in data["res_data"]:
        f.write(
            f'#EXTINF:-1 tvg-chno="{channel["ch_no"]}" ch-number="{channel["ch_no"]}" '
            f'tvg-id="{channel["ch_name"]}.th" tvg-name="{channel["ch_name"]}" '
            f'tvg-logo="{channel["img_y"]}" group-title="Digital TV", {channel["ch_name"]}\n'
        )
        f.write("#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 14; K) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                "Chrome/127.0.6533.103 Mobile Safari/537.36\n")
        f.write(channel["link"] + "\n\n")

    # Custom IPTV-THAI channel
    f.write("""#EXTINF:-1 tvg-chno="999" ch-number="999" tvg-id="IPTV-THAI.th" tvg-name="IPTV-THAI" tvg-logo="https://raw.githubusercontent.com/akkradet/IPTV-THAI/master/logo/iptvth.png" group-title="Digital TV", IPTV-THAI
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.103 Mobile Safari/537.36
https://raw.githubusercontent.com/akkradet/IPTV-THAI/master/intro.mp4

""")

print(f"✅ {output_file} generated successfully!")
