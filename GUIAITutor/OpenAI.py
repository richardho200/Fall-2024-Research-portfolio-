from openai import OpenAI

client = OpenAI(api_key="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")

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
