from tkinter import *
from threading import Thread
from time import sleep
from coin import Coin
from ftxdata import getftxdata

class MainApp(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.coin_list = self.get_coin_list()           # list of the coin tickers
        self.created_coins = {}                         # created widgets for the coin objects will be stored here for referencing
        self.clicked = ''                               # temporary variable to prevent creation of duplicate coin object when double clicking
        self.__initialize_widgets()
        
    # initialize the starting and permanent widgets
    def __initialize_widgets(self):
        # frame on the left side of the window which contains listbox, scrollbar, and button
        self.frame_left = Frame(self)
        self.frame_left.pack(side=LEFT, fill=Y)
        self.scrollbar = Scrollbar(self.frame_left, orient=VERTICAL, bg='gray40')
        self.listbox_coin_list = Listbox(self.frame_left, yscrollcommand=self.scrollbar.set, height=4, bg='gray15', fg='snow')
        self.scrollbar.config(command=self.listbox_coin_list.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox_coin_list.pack(side=TOP, fill=Y, expand=1)
        self.button_add_coin = Button(self.frame_left, text='ADD', command=lambda: Thread(target=self.create_coin).start(), bg='gray15', fg='snow')
        self.button_add_coin.pack(side=TOP,fill=BOTH)

        # insert the coin tickers from coin_list to listbox_coin_list widget
        for item in self.coin_list:
            self.listbox_coin_list.insert(END, item)

        # frame on the right side of the window which contains the labels; created widgets for the coin object will also be displayed here
        self.frame_right = Frame(self, bg='gray15')
        self.frame_right.pack(side=LEFT, fill=BOTH, expand=1)
        self.frame_label = Frame(self.frame_right, bg='gray15')
        self.frame_label.pack(side=TOP, fill=X)
        self.label_ticker = Label(self.frame_label, text='Ticker', bg='gray15', fg='snow', width=12, anchor=E)
        self.label_ticker.pack(side=LEFT, fill=X, expand=1)
        self.label_ticker = Label(self.frame_label, text='Price', bg='gray15', fg='snow', width=10, anchor=E)
        self.label_ticker.pack(side=LEFT, fill=X, expand=1)
        self.label_ticker = Label(self.frame_label, text='Daily Change', bg='gray15', fg='snow', width=17, anchor=E)
        self.label_ticker.pack(side=LEFT, fill=X, expand=1)        
        self.label_close = Label(self.frame_label, text='Close', bg='gray15', fg='snow', width=8, anchor=E, padx=10)
        self.label_close.pack(side=LEFT, fill=X, expand=1)

    # returns a list of coin tickers which is retrieved from ftx website
    def get_coin_list(self):
        coin_list = []
        ftxdata = getftxdata('https://ftx.com/api/futures')
        for item in ftxdata:
            if 'PERP' in item['name']:
                coin_list.append(item['name'])
        return coin_list
    
    # creates a coin object then call the function create_coin_widgets to create widgets for the coin objects
    def create_coin(self):
        i, = self.listbox_coin_list.curselection()
        ticker = self.coin_list[i]
        if ticker not in self.created_coins and ticker != self.clicked:
            self.clicked = ticker
            coin = Coin(ticker)
            print('Created coin ' + coin.get('ticker'))
            t = Thread(target=lambda: self.create_coin_widgets(coin))
            t.start()
            self.clicked = ''
        else:
            print(ticker + ' is already created')

    # creates widgets for the newly created coin objects and then calls the functions store_widget_data and update in separate threads
    def create_coin_widgets(self, coin):
        ticker = coin.get('ticker')
        price = coin.get('price')
        percent = coin.get('%')
        frame = Frame(self.frame_right, bg='gray15')
        frame.pack(side=TOP, fill=X)
        label_ticker = Label(frame, text=ticker, bg='gray15', fg='snow', width=12, anchor=E)
        label_ticker.pack(side=LEFT, fill=X, expand=1)
        label_price = Label(frame, text=price, bg='gray15', fg='snow', width=10, anchor=E)
        label_price.pack(side=LEFT, fill=X, expand=1)
        label_percent = Label(frame, text=percent, bg='gray15', fg='snow', width=17, anchor=E)
        label_percent.pack(side=LEFT, fill=X, expand=1)
        label_close = Label(frame, text='-', bd=1, bg='gray15', fg='snow', borderwidth=2, highlightcolor='snow', pady=0, relief=GROOVE, height=1, width=2)
        label_close.pack(side=LEFT, fill=X, expand=1, padx=(40,15))
        label_close.bind('<Button-1>', lambda e: self.destroy_coin_widget(ticker))
        print('Created widgets for ' + ticker)

        t1 = Thread(target=lambda: self.store_widget_data(ticker, frame, label_ticker, label_price, label_percent, label_close))
        t1.start()
        t2 = Thread(target=lambda: self.update(ticker))
        t2.start()

    # stores the widgets of the coin object to the dictionary of created_coins
    def store_widget_data(self, ticker, *args):
        self.created_coins[ticker] = []
        for widget in args:
            self.created_coins[ticker].append(widget)
        print('Stored widget data')

    # updates the price and percent every 1 second; the loop stops when the coin object is destroyed in the dictionary of created_coins
    def update(self, ticker):
        while ticker in self.created_coins:
            try:
                coin = Coin(ticker)
                self.created_coins[ticker][2].config(text=coin.get('price'))
                self.created_coins[ticker][3].config(text=coin.get('%'))
                sleep(1)
            except:
                pass
        print('Coin ' + ticker + ' is deleted')

    # destroys the widgets and deletes the coin object inside the dictionary of created_coins
    def destroy_coin_widget(self, ticker):
        for widget in self.created_coins[ticker]:
            widget.destroy()
        del self.created_coins[ticker]

root = Tk()
root.title('CRYPTO PERPETUAL FUTURES MARKET')
root.geometry("+1400+0")
MainApp(master=root)
root.mainloop()