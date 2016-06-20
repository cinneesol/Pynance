from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

import sqlite3
import json

import dbprops

def get_database(request):
    rows = None
    with (sqlite3.connect('db.sqlite3')) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM sqlite_master')
        rows = cursor.fetchall()
    return JsonResponse(rows, safe=False)


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
