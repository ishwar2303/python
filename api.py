import requests
import json

def getReviews(pageNumber, pageSize):
    url = 'https://graphidotbackenddotnetapi.azurewebsites.net/api/CustomerReview/Fetch/'
    url += str(pageNumber) + '/'
    url += str(pageSize)
    res = requests.get(url)
    return res.json()

def printData():
    print('Fetching Reviews...')
    reviews = getReviews(1, 3)
    print(json.dumps(reviews, indent=2))
    print('Reviews Fetched Successfully')

printData()


