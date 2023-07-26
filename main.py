#!/usr/bin/env python3

from data_processing import calculate_top_hitters
from tweet import tweet

def main():
    top_20_hitters = calculate_top_hitters()
    print(top_20_hitters)
    tweet(top_20_hitters)
    print('Done')

if __name__ == "__main__":
    main()