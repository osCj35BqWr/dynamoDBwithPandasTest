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

    df = pd.json_normalize(response["Items"])


    df.MeasureDateTime = pd.to_datetime(df.MeasureDateTime)
    # data["value"]はDecimalで入っているが。
    # Decimalは直接表示できないので、floatに変換
    df = df.astype({"value": float})

    # 日付でソートする。戻り値を受け取らないとソートされないので注意
    df = df.sort_values(by='MeasureDateTime')

    fig, ax = plt.subplots()

    # x軸の目盛りは1時間ごとにする
    ax.xaxis.set_major_locator(mdates.HourLocator())
    # x軸の目盛りの表示形式を設定する
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))

    plt.plot(df.MeasureDateTime, df.value)
    plt.show()