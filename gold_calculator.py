def sell(gold_weight: float, gold_price_per_gram: float) -> str:
    text = ''
    gold_price = gold_weight * gold_price_per_gram
    sell_price = gold_price * 740 / 750
    text += '🏋️‍♂️ وزن: ' + f'{gold_weight:.3f} ' + 'گرم' + '\n'
    text += '🥇 هر گرم طلا 750: ' + f'{gold_price_per_gram:,.0f} ' + 'تومان' + '\n'
    text += '\n'
    text += '✨ ارزش خالص طلا 750: ' + f'{gold_price:,.0f} ' + 'تومان' + '\n'
    text += '👨‍💼 قیمت فروش طلا 740: ' + f'{sell_price:,.0f} ' + 'تومان' + '\n'
    return text


def buy_secondhand(gold_weight: float, gold_price_per_gram: float, buy_price: float) -> str:
    text = ''
    gold_price = gold_weight * gold_price_per_gram
    profit_amount = buy_price - gold_price
    profit_percent = profit_amount / gold_price

    text += '🏋️‍♂️ وزن: ' + f'{gold_weight:.3f} ' + 'گرم' + '\n'
    text += '🥇 هر گرم طلا 750: ' + f'{gold_price_per_gram:,.0f} ' + 'تومان' + '\n'
    text += '👨‍💼 قیمت خرید: ' + f'{buy_price:,.0f} ' + 'تومان' + '\n'
    text += '\n'
    text += '🤑 سود فروشنده: ' + f'{profit_percent:.2%} ' + 'یا ' + f'{profit_amount:,.0f} ' + 'تومان' + '\n'
    text += '✨ ارزش خالص طلا: ' + f'{gold_price:,.0f} ' + 'تومان' + '\n'
    text += '\n'
    text += '💰 رنج قیمت فروش(حداقل, حداکثر):' + '\n'
    text += f'{gold_price:,.0f} - {buy_price:,.0f} ' + 'تومان'

    return text


def buy(gold_weight: float, gold_price_per_gram: float, fee_percent: float, buy_price: float) -> str:
    text = ''
    gold_price = gold_weight * gold_price_per_gram
    fee_percent /= 100
    gold_price_without_profit = gold_price * (1 + fee_percent)
    fee_amount = gold_price_without_profit - gold_price
    profit_amount = buy_price - gold_price_without_profit
    profit_percent = profit_amount / gold_price_without_profit

    text += '🏋️‍♂️ وزن: ' + f'{gold_weight:.3f} ' + 'گرم' + '\n'
    text += '🥇 هر گرم طلا 750: ' + f'{gold_price_per_gram:,.0f} ' + 'تومان' + '\n'
    text += '🛠 اجرت: ' + f'{fee_percent:.2%} ' + 'یا ' + f'{fee_amount:,.0f} ' + 'تومان' + '\n'
    text += '👨‍💼 قیمت خرید: ' + f'{buy_price:,.0f} ' + 'تومان' + '\n'
    text += '\n'
    text += '🤑 سود فروشنده: ' + f'{profit_percent:.2%} ' + 'یا ' + f'{profit_amount:,.0f} ' + 'تومان' + '\n'
    text += '✨ ارزش خالص طلا: ' + f'{gold_price:,.0f} ' + 'تومان' + '\n'
    text += '\n'
    text += '💰 رنج قیمت فروش(حداقل, حداکثر):' + '\n'
    text += f'{gold_price_without_profit:,.0f} - {buy_price:,.0f} ' + 'تومان'

    return text
