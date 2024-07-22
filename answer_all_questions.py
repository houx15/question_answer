import pandas as pd
import requests

API = "http://ec2-52-80-220-114.cn-north-1.compute.amazonaws.com.cn/v1/workflows/run"
HEADERS = {
    "Authorization": "Bearer app-kJD6P96dfjDkpIUPzhAvwr3w",
}


def run_workflow(question_text: str, question_answer: str):
    """
    returns:
    {
        "original_answer": "",
        "original_result": "",
        "fixed_answer": ""
    }
    """
    data = {
        "inputs": {"question_text": question_text, "question_answer": question_answer},
        "response_mode": "blocking",
        "user": "houyuxin@xizhi-ai.com",
    }

    r = requests.post(API, headers=HEADERS, json=data)

    r.raise_for_status()
    result = r.json()
    return result["data"]["outputs"]


def run_all_questions(repeat_times: int = 5):
    dataset = pd.read_csv(
        "high-school-405-240722.csv", usecols=["题干文本", "答案文本"]
    )
    for i in range(repeat_times):
        # 跑n轮，取总结果
        result = {
            "index": [],
            "question_text": [],
            "question_answer": [],
            "original_answer": [],
            "original_result": [],
            "fixed_answer": [],
        }
        for index, row in dataset.iterrows():
            result["index"].append(index)
            result["question_text"].append(row["题干文本"])
            result["question_answer"].append(row["答案文本"])
            # try:
            llm_result = run_workflow(row["题干文本"], row["答案文本"])
            original_result_text = llm_result["original_result"]
            original_result = "FALSE"
            if original_result_text.startswith("是"):
                original_result = "TRUE"

            result["original_answer"].append(llm_result["original_answer"])
            result["original_result"].append(original_result)
            result["fixed_answer"].append(llm_result["fixed_answer"])
            # except:
            #     result["original_answer"].append(None)
            #     result["original_result"].append(None)
            #     result["fixed_answer"].append(None)
        run_result = pd.DataFrame(data=result)
        run_result.to_csv(f"result-{i}.csv", index=False)


if __name__ == "__main__":
    run_all_questions()
