import csv
import datetime
from os.path import exists as file_exists
from xmlrpc.client import Boolean
from kiwisolver import UnknownConstraint
from rich import print
from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt


def read_csv(file: str, skip: bool):
    """ Function to read data from csvfile. Arguments are
    a specified filename with csv extension and to ability to
    skip the first line the csv file. """
    rows = []
    with open(file, "r", newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        if skip:
            next(csvreader)
            for row in csvreader:
                rows.append(row)
        else:
            for row in csvreader:
                rows.append(row)

    return rows


def write_csv(file: str, writemethod: str, rows: bool, data):
    """ Function to write data to a csvfile. Arguments are the filename, 
    writemethod to specify append or write, rows to specify writerow() or writerows()
    and data to write to the file. """
    if writemethod == "w":
        with open(file, "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            if rows:
                csvwriter.writerows(data)
            else:
                csvwriter.writerow(data)
    elif writemethod == "a":
        with open(file, "a", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            if rows:
                csvwriter.writerows(data)
            else:
                csvwriter.writerow(data)


def graph(file):
    """ Function that plots a bar diagram regarding costs, revenue or profit for the current year.
    Argument is a specified filename or profit. """
    year = datetime.date.today().year
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    values = [0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0]  # default value for each month 
    try:
        for row in read_csv(file=file, skip=False):
            check_month = row[2][5:7]

            if file == 'bought.csv':
                fig = 'costs'       # give the graph file the correct name
                for m in months:
                    if check_month == m:
                        values[int(check_month) - 1] += float(row[6])   # adds value for each month that has a value
                plt.suptitle(f'Costs {year}')
                plt.ylabel('costs')
                plt.xlabel('months')
            elif file == 'sold.csv':
                fig = 'revenue'
                for m in months:
                    if check_month == m:
                        values[int(check_month) - 1] += float(row[5])
                plt.suptitle(f'Revenue {year}')
                plt.ylabel('revenue')
                plt.xlabel('months')
    except FileNotFoundError: # Profit has no file. Profit is calculated between revenue() and costs()
        # the csv extension is omitted since profit has no file. Revenue and costs function take care of calculating values.
        fig = 'profit'
        for i, m in enumerate(months):
            year_month = str(year) + '-' + m
            r = revenue(year_month)
            c = costs(year_month)
            p = r - c
            values[i] += round(p, 2)

        plt.suptitle(f'Profit {year}')
        plt.ylabel('profit')
        plt.xlabel('months')

    plt.bar(months, values)
    addlabels(months, values)
    plt.savefig(f'{fig}.png')


def addlabels(x,y): 
    """ function to add labels on top of the bars in the graph function. The 
    arguments consist of x-axis, y-axis. """
    for i in range(len(x)):
        plt.text(i, y[i], y[i], horizontalalignment='center')


def time_dif(x: str, y: str, timeperiod: str):
    """ Function to calculate the difference between datetime obects. Arguments are
    two datetime objects which are used for subtraction. Last argument is to specify
    the timeperiod. Return is a timedelta object. """

    if timeperiod == 'y':    # checks if date is year 
        result = (datetime.datetime.strptime(x, "%Y") - datetime.datetime.strptime(y, "%Y")).days
    elif timeperiod == 'y-m':  # checks if date is year - month
        result = (datetime.datetime.strptime(x, "%Y-%m") - 
                datetime.datetime.strptime(y, "%Y-%m")).days
    elif timeperiod == 'y-m-d': # checks if date is year - month - day
        result = (datetime.datetime.strptime(x, "%Y-%m-%d") - 
                datetime.datetime.strptime(y, "%Y-%m-%d")).days
    elif timeperiod == 'nd':   # no date
        result = (datetime.datetime.strptime(x, "%Y-%m-%d") - y).days
    else:
        print('Use the format: year: 0000, month: 0000-00, day: 0000-00-00')
    return result


def writetime(content):
    """ Function that writes datetime to a txt file. """
    with open('time.txt', 'w', newline='') as writetime:    
        writetime.write(content)


def advance_time(args):
    """ Function that advances time, resets time or returns current internal time.
    Arguments are take from the Argsparser. """
    with open('time.txt', 'r', newline='') as readtime:
        if args.current_date:
            t = readtime.readline()
            d = t[:t.find(' ')]
            print(f'Date currently in use: {d}')
        elif args.reset:
            now = datetime.datetime.now()
            str_now = datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S.%f")
            writetime(str_now)  # invokes writetime function to write to txt
            print(f'Date reset to realtime: {str_now[:str_now.find(" ")]}')
        else:
            advance_value = args.advance_time
            if advance_value <= 0:
                print('Rewinding time is not allowed!')
            else:
                t = readtime.readline()
                format_t = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
                new_date = format_t + datetime.timedelta(days=advance_value)
                str_t = datetime.datetime.strftime(new_date, "%Y-%m-%d %H:%M:%S.%f")
                writetime(str_t)
                print(f'Advanced current date with {advance_value} days. Date currently in use is: {str_t[:str_t.find(" ")]}')
        

def get_date():
    """ Returns current internal date in use from a txt file """
    with open('time.txt', 'r') as time:
        t = time.readline()
        d = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')
        d = d.replace(hour=0, minute=0, second=0, microsecond=0)
        return d


def create_id(file):
    """ creates the next row id in the specified file given as argument """
    ids = []
    next_id = 0
    for count, line in enumerate(read_csv(file=file, skip=False)):
        ids.append(count)    
        next_id = max(ids) + 1
    return next_id


def check_stock(product):
    """ Retrieves the product(argument) from inventory. Returns amount is 0
    if expiration date has been met. """
    current_date = get_date()
    unknown_product = True
    
    for row in read_csv(file="inventory.csv", skip=False):
        if product in row:
            unknown_product = False
            expiration_date = datetime.datetime.strptime(row[3], "%Y-%m-%d")
            dif_date = (expiration_date - current_date).days
            if dif_date < 0:    # product is expired
                return -1
            else:
                return row[1]
    else: 
        if unknown_product == True:     # Product is not known in current inventory
            return -1.5     # random made up number that can never be submitted by user


def get_bought_id(product):
    """ Retrieves the id for argument product from bought.csv """
    bought_id = None
    
    for row in read_csv(file='bought.csv', skip=False):
        if product in row:
            bought_id = int(row[0])
    return bought_id


def sell(args):
    """ Function to sell products and save sell history. The arguments are taken from the
    Argsparser. It takes the product name, amount and price from the user.
    It calls the create_id() function to get next id in the sold.csv file. It also calls
    get_bought_id() to retrieve the id from bought.csv. Furthermore check_stock() is called
    to check if the selling amount not surpasses the amount in stock.
    It saves the data if only save_data and date is given by user. Date can be 
    year, year - month, year - month - day. """
    try:
        if args.save_data:
            save_data('sell_data', args.date)
        else:
        
            amount_for_sale = float(check_stock(args.product_name))
            amount = args.amount[0]

            if amount <= amount_for_sale:
                id = create_id('sold.csv')
                bought_id = get_bought_id(args.product_name)
                sell_date = datetime.date.today()
                sell_price = args.price[0]
                total_revenue = amount * sell_price

                write_csv(file='sold.csv', writemethod='a', rows=False, data=[id, bought_id, sell_date, amount, sell_price, total_revenue])
                
                lines = []
                for row in read_csv('inventory.csv', skip=False):
                    if args.product_name in row:
                        row[1] = int(amount_for_sale - amount)
                        lines.append(row)
                    else:
                        lines.append(row)
                write_csv(file='inventory.csv', writemethod='w', rows=True, data=lines)     # Calls the write_csv function to write to file          
                print(f'Successfully sold {int(amount)} {args.product_name} for a total of {total_revenue}')
            elif amount_for_sale == -1:
                print(f'ERROR: Expiration date reached of {args.product_name}.')
            elif amount_for_sale == 0:
                print('ERROR: Product not in stock')
            elif amount_for_sale == -1.5:
                print('ERROR: Product has to bought first before being sold.')
            else:
                print(f'ERROR: Amount of {args.product_name} for sale is {int(amount_for_sale)}.')
    except TypeError:
        print('That is not a valid command. Check the guide for help.')


def buy(args):
    """ Function to buy products and save buy history. The arguments are taken from the
    Argsparser. It takes the product name, amount, price and expiration date from the user.
    It calls the create_id() function to get next id in the bought.csv file. 
    It saves the data if only save_data and date is given by user. Date can be 
    year, year - month, year - month - day """
    try:
        if args.save_data:
            save_data('buy_data', args.date)
        else:
            id = create_id('bought.csv')
            product_name = (args.product_name).lower()
            buy_date = datetime.date.today()
            amount = args.amount[0]
            buy_price = args.price[0]
            expiration_date = args.expiration_date[0]
            total_costs = float(amount) * buy_price
            now = get_date()    # retrieves current date in use
            if time_dif(expiration_date, now, 'nd') > 0:   # check if expiration is after current date
                new_product = True
                for row in read_csv('inventory.csv', skip=False):
                    if product_name in row:
                        new_product = False

                if new_product:
                    write_csv(file='inventory.csv', writemethod='a', rows=False, data=[product_name, int(amount), buy_price, expiration_date])
                else:       # product is already in inventory
                    lines = []

                    for row in read_csv(file='inventory.csv', skip=False):
                        if product_name in row:
                            row[1] = int(amount) + int(row[1])
                            row[2] = buy_price
                            row[3] = expiration_date

                            lines.append(row)
                        else:
                            lines.append(row)
                    write_csv(file='inventory.csv', writemethod='w', rows=True, data=lines)

                write_csv(file='bought.csv', writemethod='a', rows=False, data=[id, product_name, buy_date, int(amount), buy_price, expiration_date, total_costs])  
            
                print(f'Successfully bought {int(amount)} {product_name}(s) for a total of {total_costs}')
            else:
                print("Choose an expiration date that surpasses current date.")
    except TypeError:
        print('That is not a valid command. Check the guide for help.')


def save_data(filename, date):
    """ Function that can either save buy or sell data to a csv file. It takes two arguments.
    The first argument is the filename to specify the bought or sold. Second is argument is to
    specify the time by either year, year-month, or year-month-day. """
    timestamp = date
    if filename == 'sell_data':
        column_names = ['id', 'bought_id', 'sell_date', 'amount', 'sell_price', 'revenue']
        write_csv(file='sell_data.csv', writemethod='w', rows=False, data=column_names)
        for row in read_csv('sold.csv', skip=True):  # skip the columnnames
            
            # make sure to check for the correct dates
            if len(timestamp) == 4:     # checks if date is year (0000)     
                if time_dif(row[2][:4], timestamp, 'y') == 0:
                    write_csv(file='sell_data.csv', writemethod='a', rows=False, data=row)
            elif len(timestamp) == 7:   # checks if date is year - month (0000-00)
                if time_dif(row[2][:7], timestamp, 'y-m') == 0:
                    write_csv(file='sell_data.csv', writemethod='a', rows=False, data=row)                     
            elif len(timestamp) == 10:  # checks if date is year - month - day (0000-00-00)
                if time_dif(row[2], timestamp, 'y-m-d') == 0:
                    write_csv(file='sell_data.csv', writemethod='a', rows=False, data=row)
        else:
            print('Use the format: year: 0000, month: 0000-00, day: 0000-00-00')                                     
    elif filename == 'buy_data':
        column_names = ['id', 'product_name', 'buy_date', 'amount', 'buy_price', 'expiration_date', 'total_costs']
        write_csv(file='buy_data.csv', writemethod='w', rows=False, data=column_names)
        for row in read_csv('bought.csv', skip=True):  # skip the columnnames
            
            # make sure to check for the correct dates
            if len(timestamp) == 4:
                if time_dif(row[2][:4], timestamp, 'y') == 0:     
                    write_csv(file='buy_data.csv', writemethod='a', rows=False, data=row)
            elif len(timestamp) == 7:
                if time_dif(row[2][:7], timestamp, 'y-m') == 0:
                    write_csv(file='buy_data.csv', writemethod='a', rows=False, data=row)
            elif len(timestamp) == 10:
                if time_dif(row[2], timestamp, 'y-m-d') == 0:
                    write_csv(file='buy_data.csv', writemethod='a', rows=False, data=row)
        else:
            print('Use the format: year: 0000, month: 0000-00, day: 0000-00-00')


def costs(args):
    """ Function that returns the costs rounded by 2 from bought.csv in a single value 
    based on a time related argument. Arguments are taken from the Argsparser, given
    by report_costs(), and specifically look at the time related arguments. 
    Time related arguments can be now, yesterday or date. Date can be specified
    in year, year-month and year-month-day. """
    total_costs = 0
    now = get_date()
    
    for row in read_csv(file='bought.csv', skip=True):  # skip the first (columnnames) row

        if args == 'today':
            if time_dif(row[2], now, 'nd') == 0:
                total_costs += float(row[6])
        elif args == 'yesterday':
            if time_dif(row[2], now, 'nd') == -1:
                total_costs += float(row[6])
        else:
            timestamp = args
            if len(timestamp) == 4:     # checks if date is year (0000)
                if time_dif(row[2][:4], timestamp, 'y') == 0:
                    total_costs += float(row[6])
            elif len(timestamp) == 7:       # checks if date is year - month (0000-00)
                if time_dif(row[2][:7], timestamp, 'y-m') == 0:
                    total_costs += float(row[6])
            elif len(timestamp) == 10:      # checks if date is year - month - day (0000-00-00)
                if time_dif(row[2], timestamp, 'y-m-d') == 0:
                    total_costs += float(row[6])
            
    return round(total_costs, 2)


def revenue(args):
    """ Function that returns the revenue rounded by 2 from sold.csv in a single value 
    based on a time related argument. Arguments are taken from the Argsparser, given
    by report_revenue(), and specifically look at the time related arguments.
    Time related arguments can be now, yesterday or date. Date can be specified
    in year, year-month and year-month-day. """
    total_revenue = 0
    now = get_date()

    for row in read_csv('sold.csv', skip=True):

        if args == 'today':
            if time_dif(row[2], now, 'nd') == 0:
                total_revenue += float(row[5])
        elif args == 'yesterday':
            if time_dif(row[2], now, 'nd') == -1:
                total_revenue += float(row[5]) 
        else:
            timestamp = args
            if len(timestamp) == 4:         # checks if date is year (0000)
                if time_dif(row[2][:4], timestamp, 'y') == 0:
                    total_revenue += float(row[5])        
            elif len(timestamp) == 7:       # checks if date is year - month (0000-00)
                if time_dif(row[2][:7], timestamp, 'y-m') == 0:
                    total_revenue += float(row[5])
            elif len(timestamp) == 10:      # checks if date is year - month - day (0000-00-00)
                if time_dif(row[2], timestamp, 'y-m-d') == 0:
                    total_revenue += float(row[5])

    return round(total_revenue, 2)


def report_revenue(args):
    """ Function that prints the revenue in either a graph for the current year or just a single value
    based on a time related argument. Arguments are taken from the Argsparser and specifically
    look at the time related arguments. Time related arguments
    can be now, yesterday or date. Date can be split up in year, year-month and year-month-day. """
    if args.today:
        print(f"Today's revenue so far: {revenue('today')}")
    elif args.yesterday:
        print(f"Yesterday's revenue: {revenue('yesterday')}")
    elif args.date:
        if len(args.date) == 4:     # checks if date is year (0000)
            print(f"Revenue from {args.date}: {revenue(args.date)}")
        elif len(args.date) == 7:   # checks if date is year - month (0000-00)
            dt_obj = datetime.datetime.strptime(args.date, "%Y-%m")
            print(f"Revenue from {dt_obj.strftime('%B')}: {revenue(args.date)}")
        elif len(args.date) == 10:      # checks if date is year - month - day (0000-00-00)
            print(f"Revenue from {args.date}: {revenue(args.date)}")
        else:
            print('Use the format: year: 0000, month: 0000-00, day: 0000-00-00')
    elif args.graph:
        graph('sold.csv')
    else:
        print('Use one of the following commands: today, yesterday, specific date, graph')


def report_costs(args):
    """ Function that prints the costs in either a graph for the current year or just a single value
    based on a time related argument. Arguments are taken from the Argsparser and specifically
    look at the time related arguments. Time related arguments
    can be now, yesterday or date. Date can be split up in year, year-month and year-month-day. """
    if args.today:
        print(f"Today's costs so far: {costs('today')}")
    elif args.yesterday:
        print(f"Yesterday's costs: {costs('yesterday')}")
    elif args.date:
        if len(args.date) == 4:     # checks if date is year (0000)
            print(f"Costs from {args.date}: {costs(args.date)}")
        elif len(args.date) == 7:   # checks if date is year - month (0000-00)
            dt_obj = datetime.datetime.strptime(args.date, "%Y-%m")
            print(f"Costs from {dt_obj.strftime('%B')}: {costs(args.date)}")
        elif len(args.date) == 10:      # checks if date is year - month - day (0000-00-00)
            print(f"Costs from {args.date}: {costs(args.date)}")
        else:
            print('Use the format: year: 0000, month: 0000-00, day: 0000-00-00')
    elif args.graph:
        graph('bought.csv')
    else:
        print('Use one of the following commands: today, yesterday, specific date, or graph')


def report_profit(args):
    """ Function that prints the profit in either a graph for the current year or just a single value
    based on a time related argument. The function calls both costs() and revenue() to calculate profit.
    Arguments are taken from the Argsparser and specifically look at the time related arguments. 
    Time related arguments can be now, yesterday or date. 
    Date can be specified in year, year-month and year-month-day. """
    profit = 0
    
    if args.today:
        r = revenue('today')
        c = costs('today')
        profit += (r - c)
        print(f"Today's profit: {profit}")
    elif args.yesterday:
        r = revenue('yesterday')
        c = costs('yesterday')
        profit += (r - c)
        print(f"Yesterday's profit: {profit}")
    elif args.date:
        r = revenue(args.date)
        c = costs(args.date)
        profit += (r - c)
        print(f"Profit regarding {args.date}: {profit}")
    elif args.graph:
        graph('profit')
    else:
        print('Use the format: year: 0000, month: 0000-00, day: 0000-00-00')


def report_inventory(args):
    """ Function that prints the inventory in a table format. Arguments are taken from
    the Argsparser and specifically look at the time related arguments. Time related arguments
    can be now, yesterday or date. Date can be specified in year, year-month and year-month-day. """
    now = get_date()
    table = Table(title="Inventory")
    table.add_column("Product Name", justify="center", style="cyan")
    table.add_column("Amount", justify="center", style="cyan")
    table.add_column("Buy Price", justify="center", style="cyan")
    table.add_column("Expiration Date", justify="center", style="cyan")
    console = Console()

    with open('inventory.csv', 'r', newline='') as inventory:
        inventoryreader = csv.reader(inventory)
        next(inventoryreader)
        sort = sorted(inventoryreader, key=lambda x: x[0])
        
        if args.now:
            out_of_stock = []
            expired_stock = []
            close_to_expiration = []
            for row in sort:
                table.add_row(row[0], row[1], row[2], row[3])
                dif_time = time_dif(row[3], now, 'nd')
                # dif_time = (datetime.datetime.strptime(row[3], '%Y-%m-%d') - now).days
                if int(row[1]) == 0:
                    out_of_stock.append(row[0])
                elif dif_time <= 0:
                    expired_stock.append(row[0])
                elif dif_time == 1:
                    close_to_expiration.append(row[0])
            console.print(table)
            print(f'Products that are out of stock: {out_of_stock}', end='\n\n')
            print(f'Products that are expired: {expired_stock}', end='\n\n')
            print(f'Products that are close to expiration: {close_to_expiration}')
                    
        elif args.yesterday:
            for row in sort:
                if time_dif(row[3], now, 'nd') == -1:
                    table.add_row(row[0], row[1], row[2], row[3])
            console.print(table)
        elif args.date:
            timestamp = args.date
            for row in sort:
                if len(timestamp) == 4:     # checks if date is a year (0000)
                    if time_dif(row[3][:4], timestamp, 'y') == 0:
                        table.add_row(row[0], row[1], row[2], row[3])                                     
                elif len(timestamp) == 7:   # checks if date is year - month (0000-00)
                    if time_dif(row[3][:7], timestamp, 'y-m') == 0:
                        table.add_row(row[0], row[1], row[2], row[3])
                elif len(timestamp) == 10:  # checks if date is year - month - day (0000-00-00)
                    if time_dif(row[3], timestamp, 'y-m-d') == 0:
                        table.add_row(row[0], row[1], row[2], row[3])
            else:
                print('Use the format: year: 0000, month: 0000-00, day: 0000-00-00')
            console.print(table)  
        else: 
            print('That is not a valid command. Please add options: now, yesterday or specific date')


# create csv files with dummy data
if not file_exists('bought.csv'):
    column_names = ['id', 'product_name', 'buy_date', 'amount', 'buy_price', 'expiration_date', 'total_costs']
    
    rows = [[1, 'apple', '2022-06-11', 10, 0.5, '2022-06-14', 5.0],
            [2, 'orange', '2022-06-13', 15, 0.7, '2022-06-17', 10.5],
            [3, 'steak', '2022-06-14', 5, 1.5, '2022-06-17', 7.5],
            [4, 'milk', '2022-06-14', 20, 1.0, '2022-06-16', 20.0], 
            [5, 'cookies', '2022-06-15', 15, 0.8, '2022-07-31', 12.0],
            [6, 'broccoli', '2022-06-15', 7, 0.6, '2022-06-17', 4.2],
            [7, 'toothpaste', '2022-06-16', 4, 0.4, '2022-09-12', 1.6],
            [8, 'water', '2022-06-19', 3, 0.3, '2022-06-25', 0.9]]


    with open('bought.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names)
        csvwriter.writerows(rows)

if not file_exists('sold.csv'):
    column_names = ['id', 'bought_id', 'sell_date', 'amount', 'sell_price', 'revenue']

    rows = [[1, 1, '2022-06-12', 10, 0.8, 8.0],
            [2, 5, '2022-06-15', 15, 1.2, 18.0],
            [3, 8, '2022-06-15', 3, 0.5, 1.5]]
    
    with open('sold.csv', 'w', newline='') as csvfile:
        csvwriter= csv.writer(csvfile)
        csvwriter.writerow(column_names)
        csvwriter.writerows(rows)

if not file_exists('inventory.csv'):
    column_names = ['product_name', 'amount', 'buy_price', 'expiration_date']

    rows = [['apple', 0, 0.5, '2021-06-14'],
            ['orange', 15, 0.7, '2021-06-17'],
            ['steak', 5, 1.5, '2022-06-17'],
            ['milk', 20, 1, '2022-06-16'], 
            ['cookies', 0, 0.8, '2022-07-31'],
            ['broccoli', 7, 0.6, '2022-06-17'],
            ['toothpaste', 4, 0.4, '2022-09-12'],
            ['water', 0, 0.3, '2022-06-25']]
    
    with open('inventory.csv', 'w', newline='') as csvfile:
        csvwriter= csv.writer(csvfile)
        csvwriter.writerow(column_names)
        csvwriter.writerows(rows)

if not file_exists('time.txt'):
    now = datetime.datetime.now()
    str_now = datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S.%f")
    with open('time.txt', 'w', newline='') as writetime:
        writetime.write(str_now)
