import os
from typing import Optional

import requests


def search_restaurants(
    keyword: Optional[str] = None,
    private_room: int = 0,
    free_drink: int = 0,
    start: int = 1,
    count: int = 3,
    response_format: str = 'json'
) -> str:
    """
    ホットペッパーグルメAPIを利用して飲食店を検索します。

    :param keyword: (Optional[str]) 飲食店を検索するためのキーワード。店名、住所、駅名、お店ジャンルなどを指定できます。例: "大阪駅 和食"
    :param private_room: (int) 個室ありの店舗で絞り込むかを指定します。0: 絞り込まない（デフォルト）, 1: 個室ありの店舗のみを検索。
    :param free_drink: (int) 飲み放題ありの店舗で絞り込むかを指定します。0: 絞り込まない（デフォルト）, 1: 飲み放題ありの店舗のみを検索。
    :param start: (int) 検索結果の開始位置を指定します。デフォルトは1。
    :param count: (int) 取得する結果数を指定します。デフォルトは3件。
    :param response_format: (str) APIレスポンスの形式を指定します。デフォルトは'json'。

    :return: APIレスポンスを指定形式（デフォルトはJSON）で返します。
    :rtype: str
    """
    base_url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
    api_key = os.getenv("HOTPEPPER_API_KEY")
    params = {
        "key": api_key,
        "format": response_format,
        "start": start,
        "count": count,
        "free_drink": free_drink,
        "private_room": private_room,
    }

    if keyword:
        params["keyword"] = keyword

    response = requests.get(base_url, params=params)

    if response_format == 'json':
        return response.json()
    else:
        return response.text
