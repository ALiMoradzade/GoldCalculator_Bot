import requests
from bs4 import BeautifulSoup
import timezone

# Install requests, html5lib, bs4 package

troy_oz = 31.1034768


def get_html(url):
    #header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"}
    header = {"User-Agent": 'Mozilla/5.1.7 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    req = requests.get(url, headers=header)
    soup = BeautifulSoup(req.content, "html.parser")
    return soup


def normalize(l: list):
    normaled = [float(x.text.strip().replace(',', '')) for x in l if x is not None]
    return normaled


def setVariables():
    global gold_oz_real, gold18_g_bazaar, gold18_mith_bazaar, gold740_g_bazaar
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
    gold_oz_real = tmp[3]
    gold18_g_bazaar = tmp[7]
    gold740_g_bazaar = tmp[9]
    gold18_mith_bazaar = tmp[11]

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
    monetaries.insert(len(monetaries) - 1,tmp[0])

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



def getGold():
    mith18 = 4.3318
    gold24_g_real = gold_oz_real * monetaries[0] / troy_oz
    gold18_mith_real = gold24_g_real * mith18 * 18 / 24
    gold18_g_real = gold24_g_real * 18 / 24
    gold740_g_real = gold24_g_real * 740 / 1000

    gold_mith_bubble = gold18_mith_bazaar - gold18_mith_real
    status = 'زمان ' + ('فروش' if gold_mith_bubble > 100000 else 'خرید')

    text = 'هر انس: ' + f'{gold_oz_real:,.2f} ' + 'دلار' + '\n\n'
    text += 'هر مثقال: ' + f'{gold18_mith_bazaar / 10:,.0f} ' + 'تومان' + f'\n{gold_mith_bubble / 10:+,.0f} ' + 'حباب' + f' : {status}\n\n'
    text += 'هر گرم 750: ' + f'{gold18_g_bazaar / 10:,.0f} ' + 'تومان' + f' {(gold18_g_bazaar - gold18_g_real) / 10:+,.0f} ' + 'حباب' +'\n'
    text += 'هر گرم 740: ' + f'{gold740_g_bazaar / 10:,.0f} ' + 'تومان' + f' {(gold740_g_bazaar - gold740_g_real) / 10:+,.0f} ' + 'حباب'
    return text

def getStock():
    names = ['عیار', 'لوتوس', 'زر', 'گوهر', 'گنج', 'نفیس', 'نهال', 'کهربا', 'زرفام', 'مثقال', 'آلتون', 'تابش', 'جواهر', 'ناب']
    text = ''
    for i in range(len(names)):
        text += f'{names[i]}: {goldStocks[i] / 10:,.0f} ' + 'تومان' + '\n'

    return text.strip()

def getCoin():
    names = ['امامی', 'تمام', 'نیم', 'ربع', 'یک گرمی']
    names_other = ['صادرات', 'ملت', 'رفاه', 'آینده', 'سامان']
    text = ''
    for i in range(len(names)):
        percentage = coins_bubble[i] / coins[i]
        status = 'زمان ' + 'خرید' if percentage < 0.20 else 'فروش'
        text += f'{names[i]}: {coins[i] / 10:,.0f} ' + 'تومان' + f'\n{coins_bubble[i] / 10:+,.0f} ' + 'یا' + f' {percentage:.2%} ' + 'حباب' + f' : {status}\n\n'

    for i in range(len(names_other)):
        text += f'{names_other[i]}: {coins_other[i] / 10:,.0f} ' + 'تومان' + '\n'

    return text.strip()

def getMonetary():
    names = ['دلار 🇺🇸', 'یورو 🇪🇺', 'درهم امارات 🇦🇪', 'پوند 🇬🇧', 'لیر 🇹🇷', 'یوان 🇨🇳', 'دینار عراق 🇮🇶', 'لیر سوریه 🇸🇾', 'ریال عربستان 🇸🇦', 'بات تایلند 🇹🇭', 'روبل روسیه 🇷🇺', 'منات ترکمنستان 🇹🇲', 'منات آذربایجان 🇦🇿', 'درام ارمنستان 🇦🇲', 'سوم ازبکستان 🇺🇿', 'سامانی تاجیکستان 🇹🇯']
    text = ''

    coin_mass = 8.13598
    dollar_real_price = coins[1] * 1000 / 900
    dollar_real_price /= gold_oz_real * coin_mass / troy_oz

    for i in range(len(names)):
        text += f'{names[i]}: {monetaries[i] / 10:,.0f} ' + 'تومان'
        if i == 0:
            text += ' (قیمت واقعی: ' + f'{dollar_real_price / 10:,.0f} ' + 'تومان)'
        text += '\n'

    return text.strip()


def message():
    setVariables()

    gold = getGold()
    coin = getCoin()
    stock_market = getStock()
    monetary = getMonetary()

    text = '🗓 تاریخ:' + f'\n📅 {persian_date} {timezone.tehran_datetime("%X")}\n\n\n'
    text += '🥇 طلا:' + f'\n{gold}\n\n\n'
    text += '🪙 سکه:' + f'\n{coin}\n\n\n'
    text += '💰 صندوق های طلا:' + f'\n{stock_market}\n\n\n'
    text += '💵 ارز:' + '\n' + monetary
    return text
