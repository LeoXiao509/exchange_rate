import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
import logging
import webbrowser
from threading import Timer

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# 定義每個租屋網站的名稱和URL
RENTAL_SITES = [
    {
        'name': 'Suumo',
        'url': 'https://suumo.jp/',
        'img': 'static/suumo.png',
        'description': '提供日本各地的租屋資訊，有多語言支援(Google翻譯)。'
    },
    {
        'name': 'Homes',
        'url': 'https://www.homes.co.jp/',
        'img': 'static/Lifull homes.jpg',
        'description': '提供詳細的房屋租賃資訊和多種搜索選項，支持多語言服務。'
    },
    {
        'name': 'Leopalace21',
        'url': 'https://www.leopalace21.com/tw',
        'img': 'static/Leopalace21.jpg',
        'description': '專門為國際學生和外國人提供短期和長期的租賃服務，提供多語言服務。'
    },
    {
        'name': 'GaijinPot Apartments',
        'img': 'static/GaijinPot Apartments.jpg',
        'url': 'https://apartments.gaijinpot.com/zh_TW/rent',
        'description': '專門為外國人提供的租屋資訊網站，涵蓋日本主要城市的房屋租賃，提供了詳細的資訊。'
    },
    {
        'name': 'Real Estate Japan',
        'url': 'https://realestate.co.jp/zh_CN',
        'img': 'static/Real Estate Japan.jpg',
        'description': '提供針對外國人的租屋和購房資訊，也有英文版網站，支持多種搜索選項。'
    },
    {
        'name': 'Sakura House',
        'url': 'https://www.sakura-house.com/tw/',
        'img': 'static/Sakura House.jpg',
        'description': '專門為外國人提供租屋服務，包含短期和長期，也有多語言服務。'
    },
    {
        'name': 'Tokyo Room Finder',
        'url': 'https://blog.tokyoroomfinder.com/',
        'img': 'static/Tokyo Room Finder.png',
        'description': '提供東京地區的租屋資訊，是英文版網站，有多語言支援(Google翻譯)。'
    },
    {
        'name': 'Village House',
        'url': 'https://www.villagehouse.jp/',
        'img': 'static/Village House.png',
        'description': '提供日本全國範圍內的低價租屋資訊，有英文版網站，也有多語言支援(Google翻譯)。'
    },
    {
        'name': 'Apamanshop',
        'url': 'https://www.apamanshop.com/',
        'img': 'static/Apamanshop.jpg',
        'description': '提供日本各地的租屋資訊，有英文版、中文版網站，也有多語言支援(Google翻譯)。'
    }
]

def get_bank_rate(bank_name):
    url = 'https://www.findrate.tw/JPY/'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查HTTP回應狀態碼
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.find_all('tr')  # 找到所有的<tr>標籤
    
    for row in rows:
        columns = row.find_all('td')
        if not columns:
            continue
        
        # 假設銀行名稱出現在第一個<td>標籤
        bank_column = columns[0].text.strip()
        if bank_name in bank_column:
            # 假設買入現鈔的匯率在某個特定位置，例如第二個<td>標籤
            rate_column = columns[1].text.strip()  # 根據實際情況調整索引
            return rate_column
    
    print(f"Could not find the rate for {bank_name}.")
    return None

def get_all_bank_rates():
    banks = [
        '陽信銀行', '彰化銀行', '渣打銀行', '永豐銀行',
        '凱基銀行', '遠東商銀', '富邦銀行', '星展銀行',
        '臺灣銀行', '第一銀行', '臺灣企銀', '國泰世華',
        '台新銀行','土地銀行','安泰銀行','三信商銀',
        '台中銀行','玉山銀行','新光銀行','兆豐銀行',
        '瑞興銀行','高雄銀行','元大銀行','板信銀行',
        '郵局','聯邦銀行','合作金庫','匯豐銀行',
        '王道銀行','上海商銀','京城銀行','華泰銀行'
    ]
    rates = {}
    for bank in banks:
        rate = get_bank_rate(bank)
        if rate:
            rates[bank] = rate
        else:
            rates[bank] = 'N/A'
    return rates

@app.route('/', methods=['GET', 'POST'])
def index():
    bank_rates = get_all_bank_rates()
    if request.method == 'POST':
        yen = request.form.get('yen')
        rate = request.form.get('rate')
        if yen and rate:
            twd = float(yen) * float(rate)
            result = f'台幣: {twd:.2f}'
        else:
            result = '請輸入有效的日元金額和匯率'
        return render_template('index.html', bank_rates=bank_rates, rental_sites=RENTAL_SITES, result=result)
    return render_template('index.html', bank_rates=bank_rates, rental_sites=RENTAL_SITES, result='')

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

@app.route('/get_answer', methods=['POST'])
def get_answer():
    user_message = request.json.get('message')
    # 這裡可以添加智能回答邏輯，例如調用聊天機器人API
    answer = "這是一個示範回應。"
    return jsonify({'answer': answer})

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)
