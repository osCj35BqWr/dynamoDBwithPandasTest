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

    # df = pd.json_normalize(data)
    df = pd.DataFrame(columns=["人数"])
    for data in response["Items"]:
        df.loc[data["MeasureDateTime"]] = data["value"]

    # data["value"]はDecimalで入っているが。
    # Decimalは直接表示できないので、floatに変換
    df = df.astype({"人数": float})
    # これをやると線がおかしくなる
    #df.index = pd.to_datetime(df.index)

    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(mdates.HourLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))

    plt.plot(df.index, df['人数'])
    plt.show()