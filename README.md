# poker-flop-analyzer

This will take any card starting hand in hold;em poker and calculate the possible hands it can hit on the flop and the gives the percentage chance of hitting them.


```python
starting_hand = HoleCards([Card(VALUES.ACE, SUITS.SPADES), Card(VALUES.SEVEN, SUITS.HEARTS)])

print(analyse(starting_hand))

```
returns:  
{'full house or quads': 0.10204081632653061,  
'trips': 1.5714285714285714,  
'two pair': 4.040816326530612,  
'top pair': 15.918367346938776,  
'middle pair': 7.346938775510204,  
'bottom pair': 3.673469387755102,  
'missed': 67.34693877551021}  
  
or for a pocket pair:
```python
starting_hand = PocketPair([Card(VALUES.SEVEN, SUITS.SPADES), Card(VALUES.SEVEN, SUITS.HEARTS)])

print(analyse(starting_hand))

```

returns:  
{'full house or quads': 1.2244897959183674,  
'trips': 10.775510204081632,  
'two pair': 16.163265306122447,  
'overpair': 3.2653061224489797,  
'pair with one overcard': 22.857142857142858,  
'pair with two overcards': 34.285714285714285,  
'underpair': 11.428571428571429}  
