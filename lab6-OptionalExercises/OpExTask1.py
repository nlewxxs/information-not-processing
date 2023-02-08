#print the titles of all movies released in 1994
import boto3
from boto3.dynamodb.conditions import Key

def query_movies(year, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('Movies')
    response = table.query(
        KeyConditionExpression=Key('year').eq(year)
    )
    return response['Items']


if __name__ == '__main__':
    query_year = 1994
    print(f"Movies from {query_year}")
    movies = query_movies(query_year)
    print('Movies released in 1994: ')
    for movie in movies:
        print(movie['title'])