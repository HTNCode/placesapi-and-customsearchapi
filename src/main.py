from dotenv import load_dotenv
from googleapiclient.discovery import build
import googlemaps
import glob
import os
# import json
import time
import logging
from datetime import timedelta, timezone, datetime
import csv

logger = logging.getLogger(__name__)
logging.basicConfig(filename=f"./logs/{timezone(timedelta(hours=+9), 'Asia/Tokyo')}.log", encoding='utf-8', level=logging.DEBUG)
load_dotenv()

# 環境変数読み込み
GOOGLE__API_KEY=os.environ["GOOGLE__API_KEY"]
CUSTOM_SEARCH_CX=os.environ["CUSTOM_SEARCH_CX"]
# 検索結果のリスト
custom_search_results = []
google_map_search_results = []

def main():
    # TODO: サンプルなので実際に使う場合は検索対象のテキストのリストを渡すようにしてください。また、必要なloggingの出力を追加してください。
    queries:[] = ["焼肉"]
    custom_search_api(queries)
    google_map_search(queries)

def custom_search_api(queries):
    service = build(
        "customsearch", "v1", developerKey=GOOGLE__API_KEY
    )
    for query in queries:
        res = (
            service.cse()
            .list(
                q=query,
                cx=CUSTOM_SEARCH_CX,
            )
            .execute()
        )
        # 住所で検索して店名を拾うとかにした方がよいかも
        # print(json.dumps(res, ensure_ascii=False, indent=4))
        # TODO: ここにjsonで返ってきた後の店名のみを拾う処理を追加し、appendでリストに追加すればOK
        custom_search_results.append(res)
        time.sleep(1) # 1秒待機

    return custom_search_results

def google_map_search(queries):
    gmaps = googlemaps.Client(key=GOOGLE__API_KEY)
    # テキスト情報で検索
    for query in queries:
        res = gmaps.places(
            query,
            language="ja",
            region="jp" # 検索対象地域
        )

        detailed_results = []

         # 各場所の詳細情報を取得
        for place in res.get("results", []):
            try:
                # place_idを使用して詳細情報を取得
                place_details = gmaps.place(
                    place["place_id"],
                    language="ja",
                    fields=[
                        "name",
                        "nationalPhoneNumber",
                        "formattedAddress",
                        "shortFormattedAddress",
                        "businessStatus",
                        "formattedAddress",
                    ]
                )["result"]

                 # 必要な情報を整形
                detailed_place = {
                    "name": place.get("name"),
                    "nationalPhoneNumber": place_details.get("nationalPhoneNumber", "なし"),
                    "formattedAddress": place_details.get("formattedAddress", "なし"),
                    "shortFormattedAddress": place.get("shortFormattedAddress", "なし"),
                    "businessStatus": place_details.get("businessStatus", "なし"),
                    "formattedAddress": place_details.get("formattedAddress", "なし")
                }
                detailed_results.append(detailed_place)

            except Exception as e:
                detailed_results.append("検索結果が得られませんでした")
                continue
        time.sleep(1) # 1秒待機
    return google_map_search_results


def export_sample():
    # TODO:ここにexportディレクトリにファイル出力する処理を書く
    sample_list = [["A", "B"], ["C", "D", "E"]]
    with open(f"./export/export_{datetime.now().strftime('%Y%m%d%H%M')}.csv", mode="a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(sample_list)

def import_sample():
    # TODO:ここにcsvディレクトリに設置したファイルをインポートする処理を書く
    for x in glob.glob('*.jpg'):
        print(x)


if __name__ == "__main__":
    main()
