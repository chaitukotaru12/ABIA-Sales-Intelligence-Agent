
from ollama import chat


def ask_qwen(question):

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a business intelligence analyst. "
                    "Answer in complete sentences. "
                    "Give three clear points. "
                    "Avoid unnecessary explanations."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        options={
            "num_predict": 700,
            "temperature": 0.2
        }
    )

    return response.message.content


if __name__ == "__main__":

    question = (
        "Explain three possible reasons for declining sales. "
        "Give one short explanation for each reason."
    )

    answer = ask_qwen(question)

    print("\nQWEN RESPONSE:\n")
    print(answer)
    print("\n--- END OF RESPONSE ---")
