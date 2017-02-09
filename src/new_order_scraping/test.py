from auction_order import AuctionOrder
from storefarm_order import StorefarmOrder
from _11st_order import _11stOrder
from interpark_order import InterparkOrder

from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()

a = StorefarmOrder('id', 'password')
b = _11stOrder('id', 'password')
c = AuctionOrder('id', 'password')
d = InterparkOrder('id', 'password')

try:
    if a.logOn():
        print('login success')
        print(a.getNewOrderNum())
    else:
        print('login fail')

    if b.logOn():
        print('login success')
        print(b.getNewOrderNum())
    else:
        print('login fail')

    if c.logOn():
        print('login success')
        print(c.getNewOrderNum())
    else:
        print('login fail')

    if d.logOn():
        print('login success')
        print(d.getNewOrderNum())
    else:
        print('login fail')

finally:
    b.driverQuit()
    c.driverQuit()
    display.stop()
