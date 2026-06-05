from flask import Flask, request
from openai import OpenAI
import markdown
import os

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

@app.route("/")
def home():
    return """
<html>

<head>
<style>

body{
    max-width:900px;
    margin:40px auto;
    font-family:Arial;
}

textarea{
    width:100%;
    padding:10px;
}

button{
    padding:12px 20px;
    cursor:pointer;
}

</style>
</head>

<body>

<h1>Olin AI求职助手</h1>

<p>输入你的背景信息，获得职业建议</p >

<form method="post" action="/analyze">

<p>目标岗位：</p >

<select name="target">
<option>AI产品</option>
<option>AI运营</option>
<option>AI销售</option>
<option>跨境电商</option>
</select>
<br><br>

<p>功能：</p >

<select name="mode">
<option>职业规划</option>
<option>简历优化</option>
</select>
<br><br>

<textarea
name="resume"
rows="15"
placeholder="请输入年龄、学历、工作经历..."
></textarea>

<br><br>

<button type="submit">
开始AI分析
</button>

</form>

</body>
</html>
"""

@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.form["resume"]
    target = request.form["target"]
    mode = request.form["mode"]

    if mode == "职业规划":
        prompt = """你是一名深圳AI行业招聘顾问。

请根据用户背景输出：

1. 优势分析
2. 劣势分析
3. 推荐岗位
4. 30天行动计划
5. 面试准备建议

输出Markdown格式。"""

    else:
        prompt = """你是一名资深HR。

请优化用户简历：

1. 找出问题
2. 优化表达
3. 补充亮点
4. 输出优化版简历

输出Markdown格式。"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        temperature=0.3,
        max_tokens=800,
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": f"""目标岗位：{target}

用户背景：
{resume}

请根据所选功能给出结果。"""
            }
        ]
    )

    html_result = markdown.markdown(
        response.choices[0].message.content
    )

    return f"""
<html>
<head>
<style>
body {{
    max-width: 900px;
    margin: 40px auto;
    font-family: Arial;
    line-height: 1.8;
}}

.result {{
    background: #f5f5f5;
    padding: 20px;
    border-radius: 10px;
}}
</style>
</head>

<body>
<h1 style="color:#2563eb;">
分析结果
</h1>

<div class="result">
{html_result}
</div>

<br>
<a href=" ">重新分析</a >

</body>
</html>
"""

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
