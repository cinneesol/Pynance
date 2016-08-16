from Pynance.database import dbprops

import sqlite3
import csv


results = []
rows = ["symbol","date","avg_day_high","avg_day_low","avg_close"]

with sqlite3.connect(dbprops.sqlite_file) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(dbprops.sqlite3_find_bottoming_out_reversal);
    for r in cur.fetchall():
        res = {}
        for key in r.keys():
            res[key]=r[key]
        results.append(res)

    
with open('potential_reversals.csv','w') as csvFile:
    writer = csv.DictWriter(csvFile,fieldnames=rows)
    writer.writeheader()
    for x in results:
        writer.writerow(x)