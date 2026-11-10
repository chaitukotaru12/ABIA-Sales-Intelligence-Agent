
import json
from ollama import chat


class SalesAnalysisPlanner:
    """
    Uses Qwen to convert business questions
    into structured sales analysis plans.
    """

    ALLOWED_TOOLS = [
        "get_overview",
        "revenue_by_product",
        "revenue_by_region",
        "monthly_revenue",
        "get_data_quality"
    ]

    def __init__(self, model="qwen3:4b"):
        self.model = model

    def create_plan(self, question):

        system_prompt = """
        You are an expert Sales Intelligence Planning Agent.

        Your task is to understand a user's sales question
        and create a structured analysis plan.

        Available tools:
        - get_overview
        - revenue_by_product
        - revenue_by_region
        - monthly_revenue
        - get_data_quality

        Rules:
        1. Select only tools from the available list.
        2. Select only tools relevant to the question.
        3. Never invent numerical results.
        4. Do not calculate revenue yourself.
        5. Return valid JSON only.

        Required JSON structure:
        {
            "objective": "Short description",
            "tools": ["tool_name"],
            "steps": ["step 1", "step 2"]
        }
        """

        response = chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            think=False,
            format="json",
            options={
                "temperature": 0,
                "num_predict": 700
            }
        )

        response_text = response.message.content

        print("\n===== DEBUG: QWEN RESPONSE =====")
        print("Content:", repr(response_text))
        print(
            "Thinking field present:",
            bool(getattr(response.message, "thinking", None))
        )

        try:
            plan = json.loads(response_text)
        except json.JSONDecodeError as error:
            raise ValueError(
                "Qwen returned invalid JSON."
            ) from error

        self.validate_plan(plan)

        return plan

    def validate_plan(self, plan):

        if not isinstance(plan, dict):
            raise ValueError("Plan must be a JSON object.")

        if not isinstance(plan.get("objective"), str):
            raise ValueError("Invalid objective.")

        tools = plan.get("tools")

        if not isinstance(tools, list) or not tools:
            raise ValueError("Plan must contain at least one tool.")

        invalid_tools = [
            tool for tool in tools
            if tool not in self.ALLOWED_TOOLS
        ]

        if invalid_tools:
            raise ValueError(
                f"Unauthorized tools requested: {invalid_tools}"
            )

        steps = plan.get("steps")

        if not isinstance(steps, list) or not steps:
            raise ValueError("Plan must contain analysis steps.")

        if not all(isinstance(step, str) for step in steps):
            raise ValueError("Every analysis step must be text.")
