import numpy as np
import pandas as pd

class Game():

    history = pd.DataFrame(columns=['Price', 'Action', 'Trade', 'Cash($)', 'Holding(BTC)', 'Capital($)', 'Capped'])

    def __init__(self, data, predictor, **kwargs):

        self.data = data
        self.predictor = predictor
        self.bitcoin = kwargs.get('bitcoin', 1)
        self.cash = kwargs.get('cash', 200)


    def play(self):

        bitcoin_ = self.bitcoin
        cash_ = self.cash


        for d in np.array(self.data):

            info = {}

            prediction = self.predictor.predict(d)

            spent_cash = d[0] * prediction[0] * prediction[1] * -1
            sold_btc = prediction[0]*prediction[1]
            

            if spent_cash + cash_ < 0:

                info.update({'Capped':f"{(abs(spent_cash-cash_))}$"})

                bitcoin_ += cash_/d[0]
                cash_ = 0
            
            elif sold_btc + bitcoin_ < 0:

                info.update({'Capped':f"{(abs(sold_btc-bitcoin_))}BTC"})

                cash_ += bitcoin_ * d[0]
                bitcoin_ = 0 

            else:
                cash_ += spent_cash 
                bitcoin_ += prediction[0]*prediction[1]
                info.update({'Capped': 0})


            info.update({'Price':d[0], 'Action':prediction[0], 'Trade':prediction[1], 'Cash($)':cash_, 'Holding(BTC)':bitcoin_, 'Capital($)':(cash_ + d[0]*bitcoin_)})
            self.history = self.history.append(info, ignore_index=True)

        return self.history



    def multi_play(self, n=5):

        histories = []
        for i in range(5):

            histories.append(self.play())
        
        self.histories = histories

        return histories

        


class Predictor():

    
    def __init__(self, **kwargs):
        self.preceding = kwargs.get('preceding', 0)
        self.history = []


    def get_past(self):

        if len(self.history) >= self.preceding:

            return self.history[-self.preceding:]

        else:
            return False


    def predict(self, data):

        pasts = self.get_past()
        self.history.append(data)

        if pasts:
            return self.predict_engine(pasts, data)

        else:
            return (0,0)

        

    def predict_engine(self, pasts, data):
        

        """

        arg1:

        sell: -1
        hold: 0
        buy: 1

        arg2:

        percent traded

        """


        return (1, 0.25)