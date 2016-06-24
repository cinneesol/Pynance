from statistics import mean, pstdev
from investopedia import option_chain

def get_calls(options, month):
    calls_for_month = []
    for option in options['calls']:
        if option['month'] == month:
            calls_for_month.append(option)
    return calls_for_month

def get_puts(options,month):
    puts_for_month = []
    for option in options['puts']:
        if option['month'] == month:
            puts_for_month.append(option)
    return puts_for_month

def calculate_weighted_call_price(calls):
    total_open_interest = sum([int(x['openInterest'].replace(',','')) for x in calls])
    weighted_sum = 0
    for call in calls:
        cost = float(call['strikePrice'])+float(call['ask'])
        weighted_sum += int(call['openInterest'].replace(',',''))*cost
    
    if total_open_interest>0:
        return weighted_sum/total_open_interest
    else:
        return 0

def calculate_weighted_put_price(puts):
    total_open_interest = sum([int(x['openInterest'].replace(',','')) for x in puts])
    weighted_sum = 0
    for put in puts:
        cost = float(put['strikePrice'])+float(put['ask'])
        weighted_sum += int(put['openInterest'].replace(',',''))*cost
    if total_open_interest>0:
        return weighted_sum/total_open_interest
    else:
        return 0
    
def analyze_options(options):
    analysis = {'date':options['date'],'symbol':options['calls'][0]['symbol']}
    option_months = [x['month'] for x in options['calls']]
    month_analysis = {}
    for month in option_months:
        calls = get_calls(options, month)
        puts = get_puts(options, month)
        weighted_effective_call_price = calculate_weighted_call_price(calls)
        weighted_effective_put_price = calculate_weighted_put_price(puts)
        month_analysis[month] = {
                                 'weighted_effective_call_price':weighted_effective_call_price,
                                 'weighted_effective_put_price':weighted_effective_put_price
                                 }
    analysis['month_analysis']=month_analysis
    return analysis
