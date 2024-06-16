from openai import OpenAI
import time
import os
import dotenv

dotenv.load_dotenv()

openai = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")


def interact_with_assistant(ass_id, prompt):
    # Retrieve the assistant
    assistant = openai.beta.assistants.retrieve(ass_id)

    # Create a new thread
    thread = openai.beta.threads.create()
    thread_id = thread.id

    # Create a message in the thread
    message = openai.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=prompt
    )

    # Initiate a run with the assistant
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ass_id,
    )
    run_id = run.id

    # Check the status until the run is complete
    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id,
        ).status

        if run_status == "completed":
            break

        time.sleep(2)

    # Retrieve the messages from the thread
    response = openai.beta.threads.messages.list(thread_id=thread_id)

    if response.data:
        return response.data[0].content[0].text.value
    else:
        return None


# Example usage
response_content = interact_with_assistant(
    assistant_id, "[topic]: make money with chatgpt"
)

if response_content:
    print(response_content)
