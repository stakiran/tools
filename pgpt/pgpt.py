import argparse
import openai
import os
import concurrent.futures


openai.api_key = os.environ["OPENAI_API_KEY"]
client = openai.OpenAI()

# 事前定義するモデル一覧
MODELS = [
    "gpt-4o",
    "gpt-4.1",
    "gpt-5",
    "gpt-5.1",
    "gpt-5.2",
    "o1", 
    "o3-mini",
    "o4-mini",
    #"o1-pro", #  This model is only supported in v1/responses and not in v1/chat/completions
]

def read_prompt(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def request_to_model(model_name, prompt, timeout=130):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {'role': 'user', 'content': prompt},
            ],
            timeout=timeout
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR in {model_name}]: {str(e)}"

def save_response(base_filename, model_name, content):
    name, ext = os.path.splitext(base_filename)
    out_filename = f"{name}-{model_name}.md"
    with open(out_filename, "w", encoding="utf-8") as f:
        f.write(content)
        f.write('\n')  # ファイル末尾に空行を追加
    print(f"Saved: {out_filename}")

def main():
    parser = argparse.ArgumentParser(description="Prompt multi LLMs and save responses.")
    parser.add_argument("-i", "--input", required=True, help="Input markdown file as prompt.")
    args = parser.parse_args()

    prompt = read_prompt(args.input)

    # 並列で各モデルにリクエスト
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_model = {
            executor.submit(request_to_model, model, prompt): model
            for model in MODELS
        }
        for future in concurrent.futures.as_completed(future_to_model):
            model = future_to_model[future]
            content = future.result()
            save_response(args.input, model, content)

if __name__ == "__main__":
    main()
