def get_difference(x2: float, x1: float):
    delta = x2 - x1
    # dic = dict(amount=delta,percent=delta / x1)
    dic = [delta, delta / x1]
    return dic


def sell(gold_weight: float, gold_price_per_gram: float) -> str:
    text = ''
    gold_price = gold_weight * gold_price_per_gram
    sell_price = gold_price * 740 / 750
    text += '🏋️‍♂️ وزن: ' + f'{gold_weight:.3f} ' + 'گرم' + '\n'
    text += '🥇 مظنه طلا 750: ' + f'{gold_price_per_gram:,.0f} ' + 'تومان' + '\n'
    text += '\n'
    text += '✨ ارزش طلا به 750:' + '\n'
    text += f'{gold_price:,.0f} ' + 'تومان' + '\n'
    text += '\n'
    text += '👨‍💼 قیمت فروش طلا به 740:' + '\n'
    text += f'{sell_price:,.0f} ' + 'تومان' + ' (⚠️ باید همین مقدار باشد!)'
    return text


def buy(gold_weight: float, gold_price_per_gram: float, fee_percent: float, gold_store_price: float) -> str:
    text = ''
    # fee = dict(amount=0.0, percent=fee_percent / 100)
    fee = [0.0, fee_percent / 100]

    gold_value = gold_weight * gold_price_per_gram
    gold_price_with_fee = gold_value * (1 + fee[1])
    # fee['amount'] = gold_price_with_fee - gold_value
    fee[0] = gold_price_with_fee - gold_value
    jeweler_profit = get_difference(gold_store_price, gold_value)
    store_profit = get_difference(gold_store_price, gold_price_with_fee)

    text += '🏋️‍♂️ وزن: ' + f'{gold_weight:.3f} ' + 'گرم' + '\n'
    text += '🥇 مظنه طلا 18: ' + f'{gold_price_per_gram:,.0f} ' + 'تومان' + '\n'
    # text += '🛠 اجرت: ' + f'{fee['percent']:.2%} ' + 'یا ' + f'{fee['amount']:,.0f} ' + 'تومان' + '\n'
    text += '🛠 اجرت: ' + f'{fee[1]:.2%} ' + 'یا ' + f'{fee[0]:,.0f} ' + 'تومان' + '\n'
    text += '👨‍💼 قیمت حجره دار: ' + f'{gold_store_price:,.0f} ' + 'تومان' + '\n'
    text += '\n'
    text += '🤑 سود حجره دار:' + '\n'
    # text += f'{store_profit['percent']:.2%} ' + 'یا ' + f'{store_profit['amount']:,.0f} ' + 'تومان' + ' (اگر حجره دار از زرگر بخرد)' + '\n'
    # text += f'{jeweler_profit['percent']:.2%} ' + 'یا ' + f'{jeweler_profit['amount']:,.0f} ' + 'تومان' + ' (اگر حجره دار زرگر باشد)' + '\n'
    text += f'{store_profit[1]:.2%} ' + 'یا ' + f'{store_profit[0]:,.0f} ' + 'تومان' + ' (اگر حجره دار از زرگر بخرد)' + '\n'
    text += f'{jeweler_profit[1]:.2%} ' + 'یا ' + f'{jeweler_profit[0]:,.0f} ' + 'تومان' + ' (اگر حجره دار زرگر باشد)' + '\n'
    text += '\n'
    text += '💰 دامنه قیمت طلا(بزرگ به کوچک):' + '\n'
    text += 'حجره دار - با اجرت - ارزش طلا' + '\n'
    text += f'{gold_store_price:,.0f} - {gold_price_with_fee:,.0f} - {gold_value:,.0f} ' + 'تومان' + '\n'
    text += 'تخفیف یادت نره!😧'

    return text


def buy_secondhand(gold_weight: float, gold_price_per_gram: float, gold_store_price: float) -> str:
    text = ''

    gold_value = gold_weight * gold_price_per_gram
    store_profit = get_difference(gold_store_price, gold_value)

    text += '🏋️‍♂️ وزن: ' + f'{gold_weight:.3f} ' + 'گرم' + '\n'
    text += '🥇 مظنه طلا 18: ' + f'{gold_price_per_gram:,.0f} ' + 'تومان' + '\n'
    text += '👨‍💼 قیمت حجره دار: ' + f'{gold_store_price:,.0f} ' + 'تومان' + '\n'
    text += '\n'
    text += '🤑 سود حجره دار:' + '\n'
    # text += f'{store_profit['percent']:.2%} ' + 'یا ' + f'{store_profit['amount']:,.0f} ' + 'تومان' + '\n'
    text += f'{store_profit[1]:.2%} ' + 'یا ' + f'{store_profit[0]:,.0f} ' + 'تومان' + '\n'
    text += '\n'
    text += '💰 دامنه قیمت طلا(بزرگ به کوچک):' + '\n'
    text += 'حجره دار - ارزش طلا' + '\n'
    text += f'{gold_store_price:,.0f} - {gold_value:,.0f} ' + 'تومان' + '\n'
    text += 'تخفیف یادت نره!😧'

    return text
