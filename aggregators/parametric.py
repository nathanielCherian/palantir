

class ParametricAnalysis:

    def __init__(self, intervals, **kwargs):
        self.intervals = intervals
        self.out = kwargs.get('out', 1)

    def fit(self, X):

        X_intervals, y_intervals = [split_sequence(X, interval, self.out) for interval in self.intervals]


        for x_, y_ in zip(X_intervals, y_intervals):

            while x_:
                
                break



        def split_sequence(seq, n_steps_in, n_steps_out):
            """
            Splits the univariate time sequence
            """
            X, y = [], []
            
            for i in range(len(seq)):
                end = i + n_steps_in
                out_end = end + n_steps_out
                
                if out_end > len(seq):
                    break
                
                seq_x, seq_y = seq[i:end], seq[end:out_end]
                
                X.append(seq_x)
                y.append(seq_y)
            
            return np.array(X), np.array(y)