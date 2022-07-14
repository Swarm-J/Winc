## Report
The first two problems I ran into was the use of spaces in positional arguments and using multiple
positional arguments without getting the error 'Error: Too few arguments'. I tackled both these problems
at the same time by using a list of strings. The list of commands could then be used by the parameter
choices of the ```add_argument()``` method. Each one of these strings represents a basic command that the user
needs to choose one of to start and build up a command. 
The program only knows one optional argument, but with the use of the parameter ```'metavar'``` the user will
see seven different commands. 
A smaller point of notice is the use of ```add_mutually_exclusive_group()```. This takes care
of preventing the user from combining certain optional arguments. This is an easy way to make it clear
for the user what is and what is not allowed. An error message will be prompted when a certain combination
is not allowed.



The third problem I ran into was that some functions needed to return values and print these values at
the same time. My solution to the above problem was ```creating two functions```. One that handles the printing
and one that generates the needed values. The function that handles the printing gets called by the user, 
which then calls the function that generates the needed values. So when the user enters the report-revenue
or report-costs command the function get_revenue/get_costs is called. Both functions wil check which argument
regarding time is being entered. Then the function that actually calculates the reveneu/costs is called with
the time based argument (i.e. revenue(yesterday)).

One other thing of notice when working with timedelta objects and the days attribute is the rounding. For
example 2022-06-25 15:30:12.917806 will be rounded up as 2022-06-26. This will give (un)expected results 
when using the condition 'if datetime.datetime.now() - datetime.datetime.strpstrptime('2022-06-26, "%Y-%m-%d") == 0:'
if it's already passed 12:00 and assuming now is 2022-06-25. 
The ```replace method``` solved this issue because it can set values of a datetime object. Regarding the above example
it would look like this: datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)