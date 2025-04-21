def dates_range(input_file):
    ranges = []
    ranges.append(input_file[-1][0])
    ranges.append(input_file[0][0])
    for date in range(len(ranges)):
        ranges[date] = ranges[date][-2:] + '/' + ranges[date][5:-3] + '/' + ranges[date][:4]

    return ranges


def find_capital(input_file):
    capital = 0
    stock_gain = 0
    first = True

    for stock in range(len(input_file)):
        #  boolean added to deal with date range change: skip initial Sell if new range starts with sell
        if input_file[stock][6] == 'Sell' and first:
            continue
        elif input_file[stock][6] == 'Buy' and stock_gain < float(input_file[stock][10].replace('.', '').replace(',', '.')):
            capital += -float(input_file[stock][10].replace('.', '').replace(',', '.')) - stock_gain
            stock_gain = 0
            first = False
        elif input_file[stock][6] == 'Sell':
            stock_gain += float(input_file[stock][10].replace('.', '').replace(',', '.'))
        elif input_file[stock][6] == 'Buy':
            stock_gain += float(input_file[stock][10].replace('.', '').replace(',', '.'))

    return round(capital, 2)


def find_closed_positions(input_file):
    stock_list = []
    total_balance = 0
    input_copy_buy = []

    #  appends all rows prior to first sale transaction found
    for line in input_file:
        input_copy_buy.append(line)

    for sell_row in range(0, len(input_file)):
        if input_file[sell_row][6] == 'Sell' and input_file[sell_row][5] == 'Security':
            stock = Stocks(input_file[sell_row][4][:21], 0, 0,
                           float(input_file[sell_row][10].replace('.', '').replace(',', '.')),
                           0, 0, float(input_file[sell_row][8].replace('.', '').replace(',', '.')))
            while stock.quantity_buy < stock.quantity_sell:
                #  check for buy transactions in rows preceding sale row
                for buy_row in input_copy_buy:
                    if buy_row[4] == input_file[sell_row][4] and buy_row[6] == 'Buy' and buy_row[5] == 'Security':
                        stock.money_out += float(buy_row[10].replace('.', '').replace(',', '.'))
                        stock.quantity_buy += float(buy_row[8].replace('.', '').replace(',', '.'))
                        input_copy_buy.remove(buy_row)
                        break
            stock.price_diff = round(stock.money_in + stock.money_out, 2)
            stock.percentage = round((stock.price_diff / -stock.money_out) * 100, 2)
            total_balance += stock.price_diff
            stock_list.append(stock)

    return stock_list, round(total_balance, 2)


def find_closed_positions_buyorientedtry(input_file):
    stock_list = []
    total_balance = 0

    for buy_row in range(0, len(input_file)):
        if input_file[buy_row][6] == 'Buy' and input_file[buy_row][5] == 'Security':
            stock = Stocks(input_file[buy_row][4][:21], 0, 0,
                           0, float(input_file[buy_row][10].replace('.', '').replace(',', '.')),
                           float(input_file[buy_row][8].replace('.', '').replace(',', '.')), 0)
            for match in range(buy_row + 1, len(input_file)):
                if input_file[match][4] == input_file[buy_row][4]:
                    if input_file[match][6] == 'Buy':
                        stock.money_out += float(input_file[match][10].replace('.', '').replace(',', '.'))
                        stock.quantity_buy += float(input_file[match][8].replace('.', '').replace(',', '.'))
                    elif input_file[match][6] == 'Sell':
                        stock.money_in += float(input_file[match][10].replace('.', '').replace(',', '.'))
                        stock.quantity_sell += float(input_file[match][8].replace('.', '').replace(',', '.'))
                        if stock.quantity_sell == stock.quantity_buy:
                            stock.price_diff = round(stock.money_in + stock.money_out, 2)
                            stock.percentage = round((stock.price_diff / -stock.money_out) * 100, 2)
                            total_balance += stock.price_diff
                            stock_list.append(stock)
                            break

    return stock_list, round(total_balance, 2)


class Stocks:
    def __init__(self, name, price_diff, percentage, money_in, money_out, quantity_buy, quantity_sell):
        self.name = name
        self.price_diff = price_diff
        self.percentage = percentage
        self.money_in = money_in
        self.money_out = money_out
        self.quantity_buy = quantity_buy
        self.quantity_sell = quantity_sell
