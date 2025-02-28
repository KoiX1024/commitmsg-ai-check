import subprocess
import json
import sys

SYSTEM_PROMPT = """您是一个资深代码审查员。请对比以下代码变更和提交信息，检查是否匹配：

代码变更：
<code>
    {code_diff}
</code>

提交信息：
<msg>
    {commit_msg}
</msg>


"""
SYSTEM_PROMPT_OUT = """
请用以下的格式返回，保证结果正确可解析：
{
  "match": boolean,
  "mismatch_reasons": [str],
  "suggested_message": str
}
"""
AI_BASE_URL = "ai.base.url"
AI_MODEL = "ai.model"
AI_API_KEY = "ai.api.key"


def get_code_diff():
    """
    获取提交的文件改动
    """
    diff_cmd = ["git", "diff", "--cached", "--unified=0", "--"]
    result = subprocess.run(diff_cmd, capture_output=True, text=True)
    return result.stdout


def get_commit_message(commit_msg_file):
    """
    获取提交的msg
    """
    with open(commit_msg_file, "r") as f:
        msg = f.read()
    return msg


def get_all_git_configs():
    """
    获取所有 Git 配置项的值。

    :return: 返回所有配置项的字典
    """
    try:
        # 获取所有的 Git 配置项
        result = subprocess.run(
            ["git", "config", "--list"], capture_output=True, text=True, check=True
        )
        # 解析配置项，按行分割并存储到字典中
        config_dict = {}
        for line in result.stdout.strip().split("\n"):
            key, value = line.split("=", 1)
            config_dict[key] = value
        return config_dict
    except subprocess.CalledProcessError:
        return {}


def analyze_with_ai(diff, msg):
    """
    使用AI分析提交和msg是否匹配
    """
    git_configs = get_all_git_configs()
    base_url = git_configs[AI_BASE_URL]
    model = git_configs[AI_MODEL]
    api_key = git_configs[AI_API_KEY]
    from openai import OpenAI

    client = OpenAI(base_url=base_url, api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(code_diff=diff, commit_msg=msg)
                + SYSTEM_PROMPT_OUT,
            }
        ],
        temperature=0.0,
    )
    return json.loads(response.choices[0].message.content)


def main() -> int:
    args = sys.argv
    commit_msg_file = args[1]

    diff = get_code_diff()
    msg_info = get_commit_message(commit_msg_file)
    analysis = analyze_with_ai(diff, msg_info)

    if analysis["match"]:
        return 0
    else:
        print("Mismatch detected:")
        for reason in analysis["mismatch_reasons"]:
            print(f" - {reason}")
        print(f"\nSuggested message: {analysis['suggested_message']}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
