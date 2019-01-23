Simple classifier which use a lot of odd preprocessing.
Just an attemp to understand classifiers using simple example.

It splits all reviews to positive "+1" (raiting 5 or 4) and negative "-1" (raiting 1 or 2),
raiting 3 is neutral and not used. And tries to predict wether review would be "+1" or "-1".
It works a lot of time due odd preprocessing using only csvreader and os package.
