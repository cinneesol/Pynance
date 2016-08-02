from statistics import mean, pstdev

def analyze(historic_quotes, floating_shares):
    """returns a dict of statistics about the historic quotes for the symbol
       returns None if a None object is passed or there are not at least 
       30 entries for historic quotes
    """
    if historic_quotes is None or len(historic_quotes) <=30:
        return None
    
    quotes = sorted(historic_quotes, key=lambda x: x['Date'], reverse=True)[:30]
    dips = [x['Open']-x['Low'] for x in quotes]
    jumps = [x['High']-x['Open'] for x in quotes]
    analysis= {}
    analysis['avg_day_high']= mean([x['High'] for x in quotes])
    analysis['avg_day_low'] = mean([x['Low'] for x in quotes])
    analysis['day_high_std_dev'] = pstdev([x['High'] for x in quotes])
    analysis['day_high_slope']= quotes[0]['High']-quotes[29]['High']
    analysis['day_low_std_dev'] = pstdev([x['Low'] for x in quotes])
    analysis['day_low_slope']=quotes[0]['Low']-quotes[29]['Low']
    analysis['close_slope']=quotes[0]['Close']-quotes[29]['Close']
    analysis['avg_close'] = mean([x['Close'] for x in quotes])
    analysis['close_std_dev'] = pstdev([x['Close'] for x in quotes])
    analysis['avg_dip'] = mean(dips)
    analysis['avg_jump'] = mean(jumps)
    analysis['dip_std_dev'] = pstdev(dips,analysis['avg_dip'])
    analysis['jump_std_dev'] = pstdev(jumps, analysis['avg_jump'])
    analysis['avg_volume'] = mean([x['Volume'] for x in quotes])
    weighted_close_sum=0.0
    volume_sum=0
    for q in quotes:
        weighted_close_sum += (q['Close']*q['Volume'])
        volume_sum+= q['Volume']
    analysis['volume_weighted_avg_close']= (weighted_close_sum/volume_sum)
    most_recent = quotes[0]
    analysis['target_entry_price'] = most_recent['Close'] - (analysis['avg_dip']-analysis['dip_std_dev'])
    analysis['target_exit_price'] = most_recent['Close'] + (analysis['avg_jump']-analysis['jump_std_dev'])
    analysis['Symbol']=most_recent['Symbol']
    analysis['Date']= most_recent['Date']
    analysis['last_quote'] = most_recent
    
    try:
        if floating_shares is not None and floating_shares['float'] != "N/A" \
        and floating_shares['outstanding'] != "N/A":
            analysis['floating_shares_ratio']=int(floating_shares['float'])/int(floating_shares['outstanding']) * 100;
        else:
            analysis['floating_shares_ratio']="N/A"
    except Exception as e:
        print("historicquoteanalysis::analyze exception:: "+str(e))
        analysis['floating_shares_ratio']="N/A"
    return analysis
