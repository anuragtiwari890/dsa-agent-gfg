import requests
from bs4 import BeautifulSoup

url = "https://www.geeksforgeeks.org/problems/subarray-with-given-sum-1587115621/1"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

soup = BeautifulSoup(response.content, 'html.parser')

print(soup.prettify())