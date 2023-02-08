#delete all movies before 2000
from pprint import pprint
import boto3
from boto3.dynamodb.conditions import Key


def delete_movie(title, year, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('Movies')

    try:
        response = table.delete_item(
            Key={
                'year': year,
                'title': title
            }            
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

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
    def delete_movies(movies):
        for movie in movies:
            title = movie['title']
            year = movie['year']
            if year <2000:
                print(f"Deleting movie: \n{movie['year']} : {movie['title']}")
                delete_movie(title, year)

    query_range = 2023
    print(f"Deleting movies before 2000")
    scan_movies(query_range, delete_movies)