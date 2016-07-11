from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from stock_market.scrapers.investopedia import historic_quotes,option_chain
from stock_market.analysis.historic_quote_analysis import analyze
from stock_market.analysis.options_analysis import analyze_options

import sqlite3
import json

import dbprops

@require_http_methods(['POST'])
@csrf_exempt
def quick_analysis(request):
    query_params=json.loads(request.body.decode('utf-8'))
    stock = query_params['symbol'].lower()
    analysis = {}
    analysis['historic_quotes']=analyze(historic_quotes(stock))
    try:
        analysis['options_analysis']=analyze_options(option_chain(stock))
    except:
        analysis['option_analysis']="No options data available to analyze"
    return JsonResponse(analysis)


@require_http_methods(['POST'])
@csrf_exempt
def find_near_target_entry(request):
    results = []
    query_params=json.loads(request.body.decode('utf-8'))
    results_list = []
    with(sqlite3.connect('stockdata.db')) as connection:
        connection.row_factory = sqlite3.Row
        cur = connection.cursor()
        cur.execute(dbprops.sqlite3_find_near_target_entry, (float(query_params['profit']),float(query_params['percent'])))
        
        for r in cur.fetchall():
            results.append(r)
        print(results)
        for stock in results:
            result = {}
            for field in stock.keys():
                if field.lower() in ('symbol', 'date', 'target_entry_price','target_exit_price'):
                    result[field]=stock[field]
            results_list.append(result)
    return JsonResponse(results_list,safe=False)


    
