import json
import boto3
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import matplotlib.dates as mdates
import os

# 【AWS IAM関連情報】
#  IAMユーザーに割り当てたポリシー
#   AmazonDynamoDBFullAccess
#   AWSLambdaDynamoDBExecutionRole
#  profile名
#   環境編巣にAWS_DEFAULT_PROFILE, AWS_PROFILEとして定義した。
if __name__ == '__main__':

    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(os.environ['table_name'])
    response = table.scan()

    data = response["Items"]
    print(data)

    df = pd.json_normalize(data)
    df = df.astype({'value': float})

    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d%H%M%S'))

    df.plot(x='MeasureDateTime', y='value')
    plt.show()


