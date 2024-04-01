from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a silly goober who enjoys eating onions."},
        {"role": "user", "content": "What is the tastiest food?"}
    ]
)
print("Q: What is the tastiest food?")
print("A:" + completion.choices[0].message.content)