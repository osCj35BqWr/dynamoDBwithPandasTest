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

    #df = pd.json_normalize(data)
    df = pd.DataFrame(columns=["人数"])
    for data in response["Items"]:
        df.loc[data["MeasureDateTime"]] = data["value"]

    # data["value"]はDecimalで入っているが。
    # Decimalは直接表示できないので、floatに変換
    df = df.astype({"人数": float})

    # グラフの大きさを指定してプロット
    # df.plot(figsize=(15,8))
    df.plot()

    # y軸の幅を設定
    #plt.ylim(-10, 40)

    plt.grid()
    plt.show()
