trading_demo
===========

a simple demo project based on tornado

To test apis, simply:

.. code-block:: bash

    curl 'http://127.0.0.1:8989/balance?userid=${userid}'

.. code-block:: bash

    curl -XPOST -d 'userid=${userid}&tradingamount=${trading_amount}' 'http://127.0.0.1:8989/trading/record'

