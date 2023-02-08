#print all Tom Hank movies
from pprint import pprint
import boto3
from boto3.dynamodb.conditions import Key


def scan_movies(year_range, display_movies, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('Movies')

    #scan and get the first page of results
    response = table.scan(FilterExpression=Key('year').lt(year_range));
    data = response['Items']
    display_movies(data)

    #continue while there are more pages of results
    while 'LastEvaluatedKey' in response:
        response = table.scan(FilterExpression=Key('year').lt(year_range), ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
        display_movies(data)

    return data

if __name__ == '__main__':
    def print_movies(movies):
        for movie in movies:
            if ('actors' in movie['info'].keys()): #not all info dictionaries had an 'actors' key 
                actorList = movie['info']['actors'] #extracting actors list from info dictionary
                count = actorList.count('Tom Hanks') #counts number of instances of Tom Hanks

                if count > 0: #if Tom Hanks is one of the actors, movie is printed
                    print(f"\n{movie['year']} : {movie['title']}")

    query_range = 2023 #scanned in the same way as OpExTask3
    print(f"Printing Tom Hanks Movies")
    scan_movies(query_range, print_movies)