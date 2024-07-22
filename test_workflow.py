import requests


api = "http://ec2-52-80-220-114.cn-north-1.compute.amazonaws.com.cn/v1/workflows/run"

headers = {
    "Authorization": "Bearer app-zQkHQVFKRVrkOFxpML1D9FrG",
}

data = {
    "inputs": {
        "stem": "test",
    },
    "response_mode": "blocking",
    "user": "test",
}


if __name__ == "__main__":
    r = requests.post(
        api, headers=headers, json=data,
    )

    r.raise_for_status()

    data = r.json()
    print(data["data"]["outputs"]["text"])

