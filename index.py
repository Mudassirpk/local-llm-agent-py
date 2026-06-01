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
    backend="ollama",
    mode="ultra_light",
)

start_time = time.perf_counter()
execution = agent.run(
    "Is the meeting room available on 2024-06-30 from 10:00 to 11:00?",
    print_results=True,
)
elapsed_seconds = time.perf_counter() - start_time
print(f"Response time: {elapsed_seconds:.3f} seconds")



