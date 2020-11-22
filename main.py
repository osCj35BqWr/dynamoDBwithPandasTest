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

    df = pd.json_normalize(data)
    df = df.astype({"value": float})

    df['MeasureDateTime'] = pd.to_datetime(df['MeasureDateTime'])

    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))

    plt.plot(df['MeasureDateTime'], df['value'])
    plt.show()