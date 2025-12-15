from openai import OpenAI

def same_or_not(name_1, name_2, decirb1, decirb2, category1, category2):
    client = OpenAI(api_key="sk-e274dfd9a2c74ba0a0287f14dbd77f2f", base_url="https://api.deepseek.com/v1")
    response = client.chat.completions.create(
    model   ="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个用于审核的AI助手，判断两个反馈是否可能为同一个反馈，只需要告诉我是或者否，不需要推理。注意，对同一个问题可能有不同的描述和分类，但如果它们的核心内容相同，则认为是同一个问题。"},
        {"role": "user", "content": f"请判断以下两个特征是否相同：\n1. 名称1: {name_1}\n2. 名称2: {name_2}\n3. 描述1: {decirb1}\n4. 描述2: {decirb2}\n5. 类别1: {category1}\n6. 类别2: {category2}\n请回答是或否。"},
    ],
    stream=False
)
    print(response)
    if response.choices[0].message.content.strip() == "是":
        return True
    else:
        return False
