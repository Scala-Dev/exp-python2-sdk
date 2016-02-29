import time
import exp
from collections import OrderedDict

exp.runtime.start(enableEvents=False, host="https://api.exp.scala.com", consumerAppUuid="503bc281-3fc3-4f70-b22e-a7a9288e05eb", apiKey="28f2eebf745fb84b855d0619dc853351b9139e83cdd509f2968308be21a3bfeb2c232c58dc1ffbe7168a80151c83b3f9")

time.sleep(5)
while True:  
    data = exp.api.get_feed('2aea09ff-e014-4fc3-8e57-d374f577e05d').get_data()
    mydict = data['items']
    d_sorted = sorted(mydict, key=lambda d: d.get('raw', {}).get('closed_at'), reverse=True)
    for order in d_sorted[:4]:
        print 'order id ',order['id']
        print 'create date ',order['date']
        print 'closed date ',order['raw']['closed_at']
        print order['raw']['note']
        for item in order['raw']['line_items']:
            print item['name']
            print item['quantity']
            print item['product_id']
            print item['price']
    time.sleep(5)
exp.runtime.stop()
