import json
import os
import time as t
from dataclasses import asdict
from datetime import datetime
from typing import List

import requests
from requests.exceptions import (
    ConnectionError,
    ConnectTimeout,
    HTTPError,
    ReadTimeout,
    RequestException,
    Timeout,
)

from model import HttpData, HttpLog, HttpTarget

WEB_HOOK_URL = "https://hooks.slack.com/services/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"


def http_status(url: str):
    try:
        r = requests.get(url)
    except ConnectionError:
        return "ConnectionError"
    except ConnectTimeout:
        return "ConnectTimeout"
    except HTTPError:
        return "HTTPError"
    except ReadTimeout:
        return "ReadTimeout"
    except Timeout:
        return "Timeout"
    except RequestException:
        return "RequestException"
    else:
        return r.status_code


def monitoring(log: HttpLog):
    count = 1
    while True:

        with open(f"./logs/{log.datetime}_data.json", "w") as f:

            targets = [
                HttpTarget(url="https://group-manager.nutfes.net"),
                HttpTarget(url="https://finansu.nutfes.net"),
                HttpTarget(url="https://slackbot.nutfes.net"),
                HttpTarget(url="https://seeds.nutfes.net"),
                HttpTarget(url="https://account.nutfes.net"),
            ]

            http_data = HttpData(
                count=count,
                datetime=datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
                targets=targets,
            )

            for i, target in enumerate(targets):
                status = http_status(target.url)
                http_data.targets[i].status = status

                if status == 530:
                    requests.post(
                        WEB_HOOK_URL,
                        data=json.dumps(
                            {
                                "text": f"Cloudflare 1033 Error \n url: {http_data.targets[i].url}",  # 通知内容
                                "username": "Cloudflare",  # ユーザー名
                                "icon_emoji": ":computer:",  # アイコン
                                "link_names": 1,  # 名前をリンク化
                            }
                        ),
                    )

            print(
                f"({http_data.count}) {' '.join([f'{target.url} [{target.status}]' for target in http_data.targets])}"
            )

            log.data.append(http_data)
            log_d = asdict(log)
            json.dump(log_d, f, indent=2, separators=(",", ": "))
        count += 1
        t.sleep(30)


if __name__ == "__main__":
    log = HttpLog(
        datetime=datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
        data=[],
    )
    os.makedirs("./logs", exist_ok=True)
    monitoring(log)
