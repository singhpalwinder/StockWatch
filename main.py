import requests, os, asyncio
from notifications import Notification
from stockPrices import StockPrice
from time import sleep

# global variables for setup
TRACKING_COMPANIES = ["AAPL", "AMZN", "BRK.A"]
THRESHOLD = 180
SEND_NOTIFICATION = True
FLASH_CLOCK = True

def flash_clock():
    color_params = { 
        "default": {"r": 0, "g":0,"b":170},
        "flash": {"r": 0, "g":255,"b":0}
    }
    url = "http://matrix.lan/color"

    for i in range(0, 5):

        res = requests.get(url, params=color_params["flash"])

        sleep(1)

        res = requests.get(url, params=color_params["default"])

        sleep(1)
def send_notification(notificationTitle, notificationMessage):
    try:
        # class automatically loads variables from my .env
        noti = Notification()
        noti.send_textNotification(title=notificationTitle, message=notificationMessage)
        print("Successfuly sent Message notifications")
    except Exception as e:
        print(f'Issue sending Notification: {e}')
async def main():

    st = StockPrice()
    
    # tasks for asyncio
    tasks = []

    print("Current Stock Prices:\n")
    for company in TRACKING_COMPANIES:
        price = st.get_stockPrice(company)
        symbol = st.get_symbol(company)

        if not price:
            print(f"Unable to get price for: {company}")
        

        if float(price) < THRESHOLD:
            if SEND_NOTIFICATION and FLASH_CLOCK:
                tasks.append(asyncio.to_thread(flash_clock))
                tasks.append(asyncio.to_thread(send_notification,f"{symbol} Stock Update", f"{company} dipped below ${THRESHOLD}\nGreat time to buy it!"))
            elif FLASH_CLOCK:
                tasks.append(asyncio.to_thread(flash_clock))
            elif SEND_NOTIFICATION:
                tasks.append(asyncio.to_thread(send_notification,f"{symbol} Stock Update", f"{company} dipped below ${THRESHOLD}\nGreat time to buy it!"))

        # add 6 spaces after symbol and ensure price formatting to 2 decimal places
        print(f"\t\t{symbol:6s}: ${float(price):.2f}")

    
    await asyncio.gather(*tasks)
    
if __name__ == "__main__":
    asyncio.run(main())