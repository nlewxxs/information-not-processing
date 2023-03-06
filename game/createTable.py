import boto3

def create_player_scores_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
    table = dynamodb.create_table(
        TableName='PlayerScores',
        KeySchema=[
            {
                'AttributeName': 'serverIP',
                'KeyType': 'HASH' # Partition key
            },
            {
                'AttributeName': 'score',
                'KeyType': 'RANGE' # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'serverIP',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'score',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    
    return table

if __name__ == '__main__':
    player_scores_table = create_player_scores_table()
    print("Table status:", player_scores_table.table_status)