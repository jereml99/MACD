# Importing the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def ema(Set, index, okresN) -> float:
    result = 0
    alfa = 2 / (okresN + 1)
    denominator = 0
    for i in range(0, okresN + 1):
        denominator += 1 * pow((1 - alfa), i)
    for i in range(0, okresN + 1):
        result += (Set[index - i]) * pow((1 - alfa), i)

    result /= denominator
    return float(result)


def buyAll(wallet, price) -> tuple[int, float, bool]:
    stockNum = int(wallet / price)
    wallet -= stockNum * price
    return stockNum, float(wallet),bool(stockNum)


def sellAll(wallet, price, stockNum) -> tuple[int, float,bool]:
    succes = stockNum
    wallet += stockNum * price
    stockNum = 0
    return stockNum, wallet, succes


# importing data
dataSet = pd.read_csv("Etsy_stock_5_year.csv")
X = dataSet.iloc[:, 0].values
Y = dataSet.iloc[:, 1].values


if isinstance(Y[0], str):
    for i in range(0, len(Y)):
        Y[i] = float(np.char.strip(Y[i], '$'))
Y = Y.tolist()
Y.reverse()
macdArray = []
signal = []
for index in range(26, len(Y)):
    macdArray.append(ema(Y, index, 12) - ema(Y, index, 26))
for index in range(9, len(macdArray)):
    signal.append(ema(macdArray, index, 9))
time = np.arange(26, len(macdArray) + 26)
time3 = np.arange(0, len(Y))
time2 = np.arange(35, len(signal) + 35)

# printig plots

enterWallet =float(1000)
wallet = enterWallet
walletArrey = []
buys_day = []
sells_day = []
buys_price = []
sells_price = []

StockNum = int(0)
print(f"Początkowa wartość portfela= {wallet}")
macdBiger = False
ifSignal = False
ifBuySele = False
lastValue= float()

#print("emaa  == ",ema(list(range(1, 27)),25,25))

for day in range(35, len(Y)):  # 35 becouse of specyficton of MACD
    if macdArray[day - 26] > signal[day - 35]:
        if (not (macdBiger)):  # Jeżeli wskażnik MACD był wczesniej mniejszy to znaczy że nastąpił moment przeciecia
            macdBiger = True
            newStock, wallet,ifBuySele = buyAll(wallet, Y[day])
            StockNum +=newStock
            if ifBuySele:
                lastValue = Y[day]
                buys_price.append(Y[day])
                buys_day.append(day)
    else:
        if (macdBiger):
            macdBiger = False
            if Y[day] >= lastValue*0.99: #pozwalamy na 1% straty na akcji
                StockNum, wallet,ifBuySele = sellAll(wallet, Y[day], StockNum)
                if ifBuySele:
                    sells_price.append(Y[day])
                    sells_day.append(day)
    walletArrey.append(wallet+StockNum*Y[day]) #łaczna wartosc portfela
#print(walletArrey)
print(f"Końcowa wartość portfela= {wallet+StockNum*Y[-1]:5.2f}")
print(f"Zwrot= {((wallet+StockNum*Y[-1])/enterWallet*100):5.2f}%")
print(f"Wartość portfela w przypadku kupienia na poczatku okresu i przedaniu na końcu= {(Y[-1]/Y[0]*enterWallet):5.2f}")
print(f"Zwrot= {Y[-1]/Y[0]*100:5.2f}%")
print(f"Liczba Wykonanych tranzakcji: {(len(buys_day) + len(sells_day))}")


fig, (ax1, ax2) = plt.subplots(2, 1)

fig.subplots_adjust(hspace=0.5)
ax1.plot(time, macdArray, label="MACD")
ax1.plot(time2, signal, label="SIGNAL")
ax1.set_xlabel("Time")
ax1.set_title("MACD,Signal")
ax1.legend()

ax2.plot(time3, Y, 'y', label="TXMD price")
ax2.plot(sells_day, sells_price, 'bo', label='sell')
ax2.plot(buys_day, buys_price, 'ro',label='buy')
ax2.set_xlabel("Time")
ax2.set_ylabel("Price")
ax2.set_title("Stock Price")
ax2.legend()

#ax3.plot(range(35,len(Y)),walletArrey)

plt.show()


