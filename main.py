from data_processing import calculate_top_hitters
from tweet import tweet
import heapq
import requests
import json

def main():
  top_20_hitters = calculate_top_hitters()
  tweet(top_20_hitters)
