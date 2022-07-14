# Imports
import argparse
from supermarket import *

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.
def main():

    # create parser object
    parser = argparse.ArgumentParser(description='Supermarket inventory tracker', epilog='For more detailed usage check the guide.')
    group = parser.add_mutually_exclusive_group()
    basic_commands = ['buy', 'sell', 'report-inventory', 'report-profit', 'report-costs', 'report-revenue', 'time']
    
    # parser arguments
    
    # positional
    parser.add_argument('basic_command', choices=basic_commands, metavar='buy, sell, report-inventory, report-profit, report-costs or report-revenue, time', 
                        help='basic commands to operate the program')

    # optional
    parser.add_argument('-p','--price', nargs=1, type=float, help='used to set a price for a specific product')
    parser.add_argument('-a','--amount', nargs=1, type=int, help='used to set the amount for a specific product')
    parser.add_argument('--product-name', help='used to specify the product')
    parser.add_argument('--expiration-date', nargs=1, help='used to set the date when a specified product is overdue')
    parser.add_argument('--save-data', action='store_true', help='saves the data to a csv-file. Is applicable buy history, sold history and inventory')


    group.add_argument('-n','--now', action='store_true', help='combined with report-inventory this returns a report regarding stock and expired products')
    group.add_argument('-d' ,'--date', help='returns value(s) of a specific moment in time. Can be a day, month or year')
    group.add_argument('-t', '--today', action='store_true', help='combined with i.e. report-profit it returns values regarding the current day')
    group.add_argument('-y', '--yesterday', action='store_true', help='combined with i.e. report-profit it returns values regarding yesterday')
    group.add_argument('--advance-time', type=int, help='forwards time with the specified amount of day(s)')
    group.add_argument('--current-date', action='store_true', help='returns the date that is internally used by the program')
    group.add_argument('-r', '--reset', action='store_true', help='resets the date in use to current date outside of program')
    group.add_argument('-g', '--graph', action='store_true', help='returns a graph of the current year regarding revenue, costs or profit')

    # Storing userinput in a variable
    args = parser.parse_args()
    
    # calling functions depending on type of basic command
    if args.basic_command == 'buy':
        buy(args)
    elif args.basic_command == 'sell':
        sell(args)
    elif args.basic_command == 'report-inventory':
        report_inventory(args)
    elif args.basic_command == 'report-profit':
        report_profit(args)
    elif args.basic_command == 'report-costs':
        report_costs(args)
    elif args.basic_command == 'report-revenue':
        report_revenue(args)
    elif args.basic_command == 'time':
        advance_time(args)


if __name__ == "__main__":
    main()
