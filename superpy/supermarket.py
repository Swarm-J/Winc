import csv
import datetime
from os.path import exists as file_exists
from rich import print
from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt

class Supermarket():

    def __init__(self, name):
        
        self.name = name

    def graph(self, file):
        year = datetime.date.today().year
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        values = [0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0]

        if file == 'bought.csv':
            with open(file, 'r', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    check_month = row[2][5:7]
                    for m in months:
                        if check_month == m:
                            values[int(check_month) - 1] += float(row[6])

            plt.suptitle(f'Costs {year}')
            plt.ylabel('costs')
            plt.xlabel('months')
        elif file == 'sold.csv':
            with open(file, 'r', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    check_month = row[2][5:7]
                    for m in months:
                        if check_month == m:
                            values[int(check_month) - 1] += float(row[5])

            plt.suptitle(f'Revenue {year}')
            plt.ylabel('revenue')
            plt.xlabel('months')
        elif file == 'profit':
            for i, m in enumerate(months):
                year_month = str(year) + '-' + m
                r = self.revenue(year_month)
                c = self.costs(year_month)
                p = r - c
                values[i] += round(p, 2)

            plt.suptitle(f'Profit {year}')
            plt.ylabel('profit')
            plt.xlabel('months')

        plt.bar(months, values)
        self.addlabels(months, values)
        plt.show()

    @staticmethod
    def addlabels(x,y):
        for i in range(len(x)):
            plt.text(i, y[i], y[i], horizontalalignment='center')

    def advance_time(self, args):
        with open('time.txt', 'r', newline='') as readtime:
            if args.current_date:
                t = readtime.readline()
                d = t[:t.find(' ')]
                print(f'Date currently in use: {d}')
            elif args.reset:
                now = datetime.datetime.now()
                str_now = datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S.%f")
                with open('time.txt', 'w', newline='') as writetime:
                    writetime.write(str_now)
                    print(f'Date reset to realtime: {str_now[:str_now.find(" ")]}')
            else:
                advance_value = args.advance_time
                if advance_value <= 0:
                    print('Rewinding time is not allowed!')
                else:
                    new_date = None
                    t = readtime.readline()
                    t = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
                    new_date = t + datetime.timedelta(days=advance_value)
                    
                    with open('time.txt', 'w', newline='') as writetime:
                        str_t = datetime.datetime.strftime(new_date, "%Y-%m-%d %H:%M:%S.%f")
                        writetime.write(str_t)
                    
                    print(f'Advanced current date with {advance_value} days. Date currently in use is: {str_t[:str_t.find(" ")]}')
            
    @staticmethod
    def get_date():
        with open('time.txt', 'r') as time:
            t = time.readline()
            d = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')
            d = d.replace(hour=0, minute=0, second=0, microsecond=0)
            return d
        
    @staticmethod
    def create_id(file):
        ids = []
        next_id = 0
        with open(file, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for count, line in enumerate(csvreader):
                ids.append(count)    
                next_id = max(ids) + 1
        
        return next_id

    @staticmethod
    def check_stock(product):
        current_date = datetime.datetime.now()
        
        with open('inventory.csv', 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if product in row:
                        expiration_date = datetime.datetime.strptime(row[3], "%Y-%m-%d")
                        dif_date = (expiration_date - current_date).days
                        if dif_date < 0:
                            row[1] = '0'
                            return row
                        else:
                            return row

    def get_bought_id(self, product):
        bought_id = None
        now = self.get_date()
        
        # check buy history
        with open('bought.csv', 'r', newline='') as bought:
            boughtreader = csv.reader(bought)
            
            for row in boughtreader:
                if product in row:
                    expiration_date = datetime.datetime.strptime(row[5], "%Y-%m-%d")
                    dif_date = (expiration_date - now).days
                    if dif_date > 0:
                        bought_id = int(row[0])
                        
        return bought_id

    def sell(self, args):
        try:
            if args.save_data:
                self.save_data('sell_data', args.date)
            else:
            
                amount_for_sale = float(self.check_stock(args.product_name)[1])
                amount = args.amount[0]

                if amount <= amount_for_sale:
                    id = self.create_id('sold.csv')
                    bought_id = self.get_bought_id(args.product_name)
                    sell_date = datetime.date.today()
                    sell_price = args.price[0]
                    total_revenue = amount * sell_price

                    with open('sold.csv', 'a', newline='') as sold:
                        soldwriter = csv.writer(sold)
                        soldwriter.writerow([id, bought_id, sell_date, int(amount), sell_price, total_revenue])
                    
                    lines = []
                    with open('inventory.csv', 'r', newline='') as inventory:
                        inventoryreader = csv.reader(inventory)
                        for row in inventoryreader:
                            if args.product_name in row:
                                row[1] = int(amount_for_sale - amount)
                                lines.append(row)
                            else:
                                lines.append(row)
                    with open('inventory.csv', 'w', newline='') as inventory:
                        inventorywriter = csv.writer(inventory)
                        inventorywriter.writerows(lines)            
                    print(f'Successfully sold {int(amount)} {args.product_name} for a total of {total_revenue}')
                elif amount_for_sale == '0':
                    print('ERROR: Not enough product(s) in stock and/or Expiration date reached.')
                else:
                    print('ERROR: Product not in stock')
        except TypeError:
            print('That is not a valid command. Check the guide for help.')
        
    def buy(self, args):

        try:
            id = self.create_id('bought.csv')
            product_name = args.product_name
            buy_date = datetime.date.today()
            amount = args.amount[0]
            buy_price = args.price[0]
            expiration_date = args.expiration_date[0]
            total_costs = amount * buy_price
            now = self.get_date()

            # check if expiration is after current date
            if (datetime.datetime.strptime(expiration_date, "%Y-%m-%d") - now).days > 0:
                new_product = True
                with open('inventory.csv', 'r', newline='') as inventory:
                    inventoryreader = csv.reader(inventory)
                    for row in inventoryreader:
                        if product_name in row:
                            new_product = False

                if new_product:
                    with open('inventory.csv', 'a', newline='') as inventory:
                        inventorywriter = csv.writer(inventory)
                        inventorywriter.writerow([product_name, int(amount), buy_price, expiration_date])
                                
                else: 
                    lines = []

                    with open('inventory.csv', 'r', newline='') as inventory:
                        inventoryreader = csv.reader(inventory)
                        for row in inventoryreader:
                            if product_name in row:
                                row[1] = int(amount) + int(row[1])
                                row[2] = buy_price
                                row[3] = expiration_date

                                lines.append(row)
                            else:
                                lines.append(row)
                        with open('inventory.csv', 'w', newline='') as inventory:
                            inventorywriter = csv.writer(inventory)
                            inventorywriter.writerows(lines)
                    
                with open('bought.csv', 'a', newline='') as bought:
                    boughtwriter = csv.writer(bought)
                    boughtwriter.writerow([id, product_name, buy_date, int(amount), buy_price, expiration_date, total_costs])
            
                print(f'Successfully bought {int(amount)} {product_name}(s) for a total of {total_costs}')
            elif args.save_data:
                self.save_data('buy_data', args.date)
            else:
                print("Choose an expiration date that surpasses current date.")
        except TypeError:
            print('That is not a valid command. Check the guide for help.')

    @staticmethod
    def save_data(filename, date):
        timestamp = date
        if filename == 'sell_data':
            column_names = ['id', 'bought_id', 'sell_date', 'amount', 'sell_price', 'revenue']

            with open('sell_data.csv', 'w', newline='') as sell_data, open('sold.csv', 'r', newline='') as sold :
                sell_datawriter = csv.writer(sell_data)
                sell_datawriter.writerow(column_names)
                soldreader = csv.reader(sold)   # to skip the columnnames
                next(soldreader)
                
                if len(timestamp) == 4:
                    for row in soldreader:
                        if (datetime.datetime.strptime(row[2][:4], "%Y") - 
                            datetime.datetime.strptime(timestamp, "%Y")).days == 0:
                            sell_datawriter.writerow(row)
                elif len(timestamp) == 7:
                    for row in soldreader:
                        if (datetime.datetime.strptime(row[2][:7], "%Y-%m") - 
                            datetime.datetime.strptime(timestamp, "%Y-%m")).days == 0:
                            sell_datawriter.writerow(row)                     
                elif len(timestamp) == 10:
                    for row in soldreader:
                        if (datetime.datetime.strptime(row[2], "%Y-%m-%d") - 
                            datetime.datetime.strptime(timestamp, "%Y-%m-%d")).days == 0:
                            sell_datawriter.writerow(row)                                     
        elif filename == 'buy_data':
            column_names = ['id', 'product_name', 'buy_date', 'amount', 'buy_price', 'expiration_date', 'total_costs']

            with open('buy_data.csv', 'w', newline='') as buy_data, open('bought.csv', 'r', newline='') as bought:
                buy_datawriter = csv.writer(buy_data)
                buy_datawriter.writerow(column_names)
                boughtreader = csv.reader(bought)
                next(boughtreader)  # to skip the columnnames

                if len(timestamp) == 4:
                    for row in boughtreader:
                        if (datetime.datetime.strptime(row[2][:4], "%Y") - 
                            datetime.datetime.strptime(timestamp, "%Y")).days == 0:
                            buy_datawriter.writerow(row)
                elif len(timestamp) == 7:
                    for row in boughtreader:
                        if (datetime.datetime.strptime(row[2][:7], "%Y-%m") - 
                            datetime.datetime.strptime(timestamp, "%Y-%m")).days == 0:
                            buy_datawriter.writerow(row)
                elif len(timestamp) == 10:
                    for row in boughtreader:
                        if (datetime.datetime.strptime(row[2], "%Y-%m-%d") - 
                            datetime.datetime.strptime(timestamp, "%Y-%m-%d")).days == 0:
                            buy_datawriter.writerow(row)
                    
    def costs(self, args):
        total_costs = 0
        now = self.get_date()
        
        with open('bought.csv', 'r', newline='') as bought:
            boughtreader = csv.reader(bought)
            next(boughtreader)  # skip the columnnames row

            if args == 'today':
                for row in boughtreader:
                    if (datetime.datetime.strptime(row[2], "%Y-%m-%d") - now).days == 0:
                        total_costs += float(row[6])
            elif args == 'yesterday':
                for row in boughtreader:
                    if (datetime.datetime.strptime(row[2], "%Y-%m-%d") - now).days == -1:
                        total_costs += float(row[6])
            else:
                timestamp = args
                if len(timestamp) == 4:
                    for row in boughtreader:
                        if (datetime.datetime.strptime(row[2][:4], "%Y") - 
                            datetime.datetime.strptime(timestamp, "%Y")).days == 0:
                            total_costs += float(row[6])
                elif len(timestamp) == 7:
                    for row in boughtreader:
                        dt_obj = datetime.datetime.strptime(timestamp, "%Y-%m")
                        if (datetime.datetime.strptime(row[2][:7], "%Y-%m") - dt_obj).days == 0:
                            total_costs += float(row[6])
                elif len(timestamp) == 10:
                    for row in boughtreader:
                        if (datetime.datetime.strptime(row[2], "%Y-%m-%d") - 
                            datetime.datetime.strptime(timestamp, "%Y-%m-%d")).days == 0:
                            total_costs += float(row[6])
                    
        return round(total_costs, 2)

    def revenue(self, args):
        total_revenue = 0
        now = self.get_date()

        with open('sold.csv', 'r', newline='') as sold:
            soldreader = csv.reader(sold)
            next(soldreader)
            if args == 'today':
                for row in soldreader:
                    if (datetime.datetime.strptime(row[2], "%Y-%m-%d") - now).days == 0:
                        total_revenue += float(row[5])
            elif args == 'yesterday':
                for row in soldreader:
                    if (datetime.datetime.strptime(row[2], "%Y-%m-%d") - now).days == -1:
                        total_revenue += float(row[5]) 
            else:
                timestamp = args
                if len(timestamp) == 4:
                    for row in soldreader:
                        if (datetime.datetime.strptime(row[2][:4], "%Y") - 
                            datetime.datetime.strptime(timestamp, "%Y")).days == 0:
                            total_revenue += float(row[5])        
                elif len(timestamp) == 7:
                    for row in soldreader:
                        dt_obj = datetime.datetime.strptime(timestamp, "%Y-%m")
                        if (datetime.datetime.strptime(row[2][:7], "%Y-%m") - dt_obj).days == 0:
                            total_revenue += float(row[5])
                elif len(timestamp) == 10:
                    for row in soldreader:
                        if (datetime.datetime.strptime(row[2], "%Y-%m-%d") - 
                            datetime.datetime.strptime(timestamp, "%Y-%m-%d")).days == 0:
                            total_revenue += float(row[5])

            return round(total_revenue, 2)

    def report_revenue(self, args):

        if args.today:
            print(f"Today's revenue so far: {self.revenue('today')}")
        elif args.yesterday:
            print(f"Yesterday's revenue: {self.revenue('yesterday')}")
        elif args.date:
            if len(args.date) == 4:
                print(f"Revenue from {args.date}: {self.revenue(args.date)}")
            elif len(args.date) == 7:
                dt_obj = datetime.datetime.strptime(args.date, "%Y-%m")
                print(f"Revenue from {dt_obj.strftime('%B')}: {self.revenue(args.date)}")
            elif len(args.date) == 10:
                print(f"Revenue from {args.date}: {self.revenue(args.date)}")
            else:
                print('Use the format: year: 0000, month: 0000-00, day: 0000-00-00')
        elif args.graph:
            self.graph('sold.csv')
        else:
            print('Use one of the following commands: today, yesterday, or specific date')

    def report_costs(self, args):

        if args.today:
            print(f"Today's costs so far: {self.costs('today')}")
        elif args.yesterday:
            print(f"Yesterday's costs: {self.costs('yesterday')}")
        elif args.date:
            if len(args.date) == 4:
                print(f"Costs from {args.date}: {self.costs(args.date)}")
            elif len(args.date) == 7:
                dt_obj = datetime.datetime.strptime(args.date, "%Y-%m")
                print(f"Costs from {dt_obj.strftime('%B')}: {self.costs(args.date)}")
            elif len(args.date) == 10:
                print(f"Costs from {args.date}: {self.costs(args.date)}")
            else:
                print('Use the format: year: 0000, month: 0000-00, day: 0000-00-00')
        elif args.graph:
            self.graph('bought.csv')
        else:
            print('Use one of the following commands: today, yesterday, or specific date')
        
    def report_profit(self, args):
        profit = 0
        
        if args.today:
            r = self.revenue('today')
            c = self.costs('today')
            profit += (r - c)
            print(f"Today's profit: {profit}")
        elif args.yesterday:
            r = self.revenue('yesterday')
            c = self.costs('yesterday')
            profit += (r - c)
            print(f"Yesterday's profit: {profit}")
        elif args.date:
            r = self.revenue(args.date)
            c = self.costs(args.date)
            profit += (r - c)
            print(f"Profit regarding {args.date}: {profit}")
        elif args.graph:
            self.graph('profit')
        else:
            print('Use the format: year: 0000, month: 0000-00, day: 0000-00-00')

    def report_inventory(self, args):
        now = self.get_date()
        table = Table(title="Inventory")
        table.add_column("Released", justify="center", style="cyan")
        table.add_column("Version Number", justify="center", style="cyan")
        table.add_column("Description", justify="center", style="cyan")
        table.add_column("Released", justify="center", style="cyan")
        console = Console()

        with open('inventory.csv', 'r', newline='') as inventory:
            inventoryreader = csv.reader(inventory)
            next(inventoryreader)
            sort = sorted(inventoryreader, key=lambda x: x[0])


            if args.basic_command == 'report-inventory' and args.now:
                out_of_stock = []
                expired_stock = []
                close_to_expiration = []
                for row in sort:
                    table.add_row(row[0], row[1], row[2], row[3])
                    dif_time = (datetime.datetime.strptime(row[3], '%Y-%m-%d') - now).days
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
                    if (datetime.datetime.strptime(row[3], "%Y-%m-%d") - now).days == -1:
                        table.add_row(row[0], row[1], row[2], row[3])
                console.print(table)
            elif args.date:
                timestamp = args.date
                if len(timestamp) == 4:
                    for row in sort:
                        if (datetime.datetime.strptime(row[3][:4], "%Y") - 
                        datetime.datetime.strptime(timestamp, "%Y")).days == 0:
                            table.add_row(row[0], row[1], row[2], row[3])                                     
                elif len(timestamp) == 7:
                    for row in sort:
                        dt_obj = datetime.datetime.strptime(timestamp, "%Y-%m")
                        if (datetime.datetime.strptime(row[3][:7], "%Y-%m") - dt_obj).days == 0:
                            table.add_row(row[0], row[1], row[2], row[3])
                elif len(timestamp) == 10:
                    for row in sort:
                        if (datetime.datetime.strptime(row[3], "%Y-%m-%d") - 
                        datetime.datetime.strptime(timestamp, "%Y-%m-%d")).days == 0:
                            table.add_row(row[0], row[1], row[2], row[3])
                console.print(table)  
            else: 
                print('That is not a valid command. Please add options: now, yesterday or specific date')


    # create csv files with dummy data
    if not file_exists('bought.csv'):
        column_names = ['id', 'product_name', 'buy_date', 'amount', 'buy_price', 'expiration_date', 'total_costs']
        
        rows = [[1, 'apple', '2022-06-11', 10, 0.5, '2022-06-14', 5],
                [2, 'orange', '2022-06-13', 15, 0.7, '2022-06-17', 10.5],
                [3, 'steak', '2022-06-14', 5, 1.5, '2022-06-17', 7.5],
                [4, 'milk', '2022-06-14', 20, 1, '2022-06-16', 20], 
                [5, 'cookies', '2022-06-15', 15, 0.8, '2022-07-31', 12],
                [6, 'broccoli', '2022-06-15', 7, 0.6, '2022-06-17', 4.2],
                [7, 'toothpaste', '2022-06-16', 4, 0.4, '2022-09-12', 1.6],
                [8, 'water', '2022-06-19', 3, 0.3, '2022-06-25', 0.9]]
    
    
        with open('bought.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(column_names)
            csvwriter.writerows(rows)

    if not file_exists('sold.csv'):
        column_names = ['id', 'bought_id', 'sell_date', 'amount', 'sell_price', 'revenue']

        rows = [[1, 1, '2022-06-12', 10, 0.8, 8],
                [2, 5, '2022-06-15', 15, 1.2, 18],
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