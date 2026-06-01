from dria_agent import tool
from dria_agent import ToolCallingAgent
import time

@tool
def check_availability(day:str, start_time:str,end_time:str) -> bool:
    """
    Checks if a given time slot is available.

    :param day: The date in "YYYY-MM-DD" format.
    :param start_time: The start time of the desired slot (HH:MM format, 24-hour).
    :param end_time: The end time of the desired slot (HH:MM format, 24-hour).
    :return: True if the slot is available, otherwise False.
    """

    # Mock implementation
    if start_time == "12:00" and end_time == "13:00":
        return False
    return True

agent = ToolCallingAgent(
    tools=[check_availability],
    backend="ollama", # model provider
    mode="ultra_light", # mode presets, and ultra_light maps to driaforall/tiny-agent-a:0.5b
)

start_time = time.perf_counter()
execution = agent.run(
    "Is the meeting room available on 2024-06-30 from 10:00 to 11:00?",
    print_results=True,
)
elapsed_seconds = time.perf_counter() - start_time
print(f"Response time: {elapsed_seconds:.3f} seconds")

tool_name = "check_availability"
result_key = execution.results.get(tool_name)
tool_result = execution.data.get(result_key) if result_key is not None else None
print(f"Execution details: {{{tool_name!r}: {tool_result}}}")

if tool_result is not None:
    rewrite_prompt = (
        "You are a scheduling assistant. "
        "Convert the availability result into one short, human-readable sentence. "
        f"Availability is: {tool_result}. "
        "If true, say room is available in provided range. "
        "If false, say room is not available in provided range."
    )

    if hasattr(agent.agent, "instruct"):
        print('Returning llm response')
        human_answer = agent.agent.instruct(rewrite_prompt).strip()
    else:
        print('Returning fallback response')
        # Fallback when current backend does not support instruct mode.
        human_answer = (
            "Yes, the meeting room is available between the provided time range."
            if tool_result
            else "No, the meeting room is not available between the provided time range."
        )

    print(f"Human-readable result: {human_answer}")



