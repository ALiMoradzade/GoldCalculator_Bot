import requests
from bs4 import BeautifulSoup
import date_time

# Install requests, html5lib, bs4 package

gold_real_oz = gold750_market_g = gold18_market_mith = gold740_market_g = 0
goldStocks = coins = coins_bubble = coins_other = monetaries = []
persian_date = ''


def get_real_price(global_gold_price_oz: float, global_gold_carat: int, object_gold_mass: float, object_gold_carat: int) -> float:
    troy_oz = 31.1034768
    price = global_gold_price_oz * object_gold_mass / troy_oz
    price *= object_gold_carat / global_gold_carat
    return price


def get_gold_bubble(x2: float, x1: float, end='\n\n') -> str:
    delta_x = x2 - x1
    s = f'\n{delta_x / 10:+,.0f} ' + 'یا' + f' {delta_x / x1:+.2%} ' + 'حباب' + end
    return s


def get_coin_bubble(delta_x: float, x1: float, end='\n\n') -> str:
    s = f'\n{delta_x / 10:+,.0f} ' + 'یا' + f' {delta_x / x1:+.2%} ' + 'حباب' + end
    return s


def normalize(values: list):
    normaled = []
    for value in values:
        normaled.append(float(value.text.strip().replace(',', '')))
    return normaled


def get_html(url):
    #header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"}
    header = {"User-Agent": 'Mozilla/5.1.7 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def set_variables():
    global gold_real_oz, gold750_market_g, gold18_market_mith, gold740_market_g
    global goldStocks, coins, coins_bubble, coins_other, monetaries
    global persian_date

    # Date
    # Request Page Html
    soup = get_html('https://www.tgju.org/')
    tmp = soup.find_all('div', class_='date')
    tmp = tmp[0].text
    persian_date = tmp[0:tmp.index('-')].strip()

    # Gold
    tmp = soup.find_all('td', class_='nf')[::2][:29]
    tmp = normalize(tmp)
    gold_real_oz = tmp[3]
    gold750_market_g = tmp[7]
    gold740_market_g = tmp[9]
    gold18_market_mith = tmp[11]

    # Monetary
    tmp = soup.find_all('td', class_='market-price')[:36]
    tmp = normalize(tmp)
    i = len(tmp)
    tmp.extend(tmp[:5])
    tmp.append(tmp[6])
    tmp.extend(tmp[15:17])
    tmp.append(tmp[21])
    tmp.append(tmp[27])
    tmp.append(tmp[29])
    tmp.append(tmp[35])
    tmp.extend(tmp[30:32])
    tmp.append(tmp[34])
    monetaries = tmp[i:]
    # Request Page Html
    soup = get_html('https://www.tgju.org/currency-minor')
    tmp = soup.find_all('td', class_='nf')[::2][87]
    tmp = normalize(tmp)
    monetaries.insert(len(monetaries) - 1, tmp[0])

    # Stock
    soup = get_html('https://www.tgju.org/gold-chart')
    tmp = soup.find_all('td', class_='nf')[::2][13:]
    goldStocks = normalize(tmp)

    # Coin
    soup = get_html('https://www.tgju.org/coin')
    tmp = soup.find_all('td', class_='nf')[::2]
    tmp = normalize(tmp)
    coins = tmp[0:5]
    coins_bubble = tmp[5:10]
    coins_other = tmp[10:15]


def get_gold():
    mith18 = 4.3318
    gold_real_value_oz = gold_real_oz * monetaries[0]
    gold18_real_mith = get_real_price(gold_real_value_oz, 24, mith18, 18)
    gold750_real_g = get_real_price(gold_real_value_oz, 24, 1, 18)
    gold740_real_g = get_real_price(gold_real_value_oz, 1000, 1, 740)

    status = 'زمان ' + ('خرید' if gold18_market_mith - gold18_real_mith < 100000 else 'فروش')

    text = 'هر انس: ' + f'{gold_real_oz:,.2f} ' + 'دلار' + '\n\n'
    text += 'هر مثقال: ' + f'{gold18_market_mith / 10:,.0f} ' + 'تومان' + get_gold_bubble(gold18_market_mith, gold18_real_mith, '') + f' : {status}\n\n'
    text += 'هر گرم 750: ' + f'{gold750_market_g / 10:,.0f} ' + 'تومان' + get_gold_bubble(gold750_market_g, gold750_real_g)
    text += 'هر گرم 740: ' + f'{gold740_market_g / 10:,.0f} ' + 'تومان' + get_gold_bubble(gold740_market_g, gold740_real_g, '')
    return text


def get_stock():
    names = ['عیار', 'لوتوس', 'زر', 'گوهر', 'گنج', 'نفیس', 'نهال', 'کهربا', 'زرفام', 'مثقال', 'آلتون', 'تابش', 'جواهر', 'ناب']
    text = ''
    for i in range(len(names)):
        text += f'{names[i]}: {goldStocks[i] / 10:,.0f} ' + 'تومان' + '\n'
    return text.strip()


def get_coin():
    names = ['امامی', 'تمام', 'نیم', 'ربع', 'یک گرمی']
    names_other = ['صادرات', 'ملت', 'رفاه', 'آینده', 'سامان']
    text = ''
    for i in range(len(names)):
        status = 'زمان ' + ('خرید' if coins_bubble[i] / coins[i] < 0.20 else 'فروش')
        text += f'{names[i]}: {coins[i] / 10:,.0f} ' + 'تومان' + get_coin_bubble(coins_bubble[i], coins[i], '') + f' : {status}\n\n'

    for i in range(len(names_other)):
        text += f'{names_other[i]}: {coins_other[i] / 10:,.0f} ' + 'تومان' + '\n'
    return text.strip()


def get_monetary():
    names = ['دلار 🇺🇸', 'یورو 🇪🇺', 'درهم امارات 🇦🇪', 'پوند 🇬🇧', 'لیر 🇹🇷', 'یوان 🇨🇳', 'دینار عراق 🇮🇶', 'لیر سوریه 🇸🇾', 'ریال عربستان 🇸🇦', 'بات تایلند 🇹🇭', 'روبل روسیه 🇷🇺', 'منات ترکمنستان 🇹🇲', 'منات آذربایجان 🇦🇿', 'درام ارمنستان 🇦🇲', 'سوم ازبکستان 🇺🇿', 'سامانی تاجیکستان 🇹🇯']
    text = ''

    coin_mass = 8.13598
    dollar_real_price = coins[1] / get_real_price(gold_real_oz, 1000, coin_mass, 900)

    for i in range(len(names)):
        text += f'{names[i]}: {monetaries[i] / 10:,.0f} ' + 'تومان'
        if i == 0:
            text += ' (قیمت واقعی: ' + f'{dollar_real_price / 10:,.0f} ' + 'تومان)'
        text += '\n'

    return text.strip()


def message():
    set_variables()

    gold = get_gold()
    coin = get_coin()
    stock_market = get_stock()
    monetary = get_monetary()

    text = '🗓 تاریخ:' + f'\n {persian_date} {date_time.tehran_datetime("%X")}\n\n\n'
    text += '🥇 طلا:' + f'\n{gold}\n\n\n'
    text += '🪙 سکه:' + f'\n{coin}\n\n\n'
    text += '💰 صندوق های طلا:' + f'\n{stock_market}\n\n\n'
    text += '💵 ارز:' + '\n' + monetary
    return text
