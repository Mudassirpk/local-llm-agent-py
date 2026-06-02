from dria_agent import tool
from dria_agent import ToolCallingAgent
import json


products_file = "products.json"
with open(products_file, "r") as f:
    dummy_products = json.load(f)

user_question = "are there any white color wireless headphones available?"

@tool
def list_products():
    """
    Lists available products.

    :return: A list of product objects.
    """

    # Local product catalog loaded from products.json.
    return dummy_products


agent = ToolCallingAgent(
    tools=[list_products],
    backend="ollama", # model provider
    mode="performant", # mode presets, and ultra_light maps to driaforall/tiny-agent-a:0.5b
)

execution = agent.run(
    user_question,
    print_results=False, # we will print results in a custom way below
)

tool_name = "list_products"
result_key = execution.results.get(tool_name)
tool_result = execution.data.get(result_key) if result_key is not None else None

products = tool_result if isinstance(tool_result, list) else dummy_products
cheapest_product = min(products, key=lambda p: p.get("price", float("inf"))) if products else None

print(f"Execution details: {{{tool_name!r}: {cheapest_product}}}")

# getting llm response for tool result
rewrite_prompt = (
    "You are a helpful assistant. "
    "Answer in one short sentence. "
    f"The user asked {user_question}. "
    f"The required data is: {cheapest_product}. "
)

if hasattr(agent.agent, "instruct"):
    print('Returning llm response')
    human_answer = agent.agent.instruct(rewrite_prompt).strip()
else:
    print('Returning fallback response')
    # Deterministic fallback when current backend does not support instruct mode.
    if cheapest_product:
        human_answer = (
            f"The cheapest product is {cheapest_product['name']} "
            f"({cheapest_product['id']}) at ${cheapest_product['price']:.2f}."
        )
    else:
        human_answer = "No products are currently available."

print(f"Products: {human_answer}")
