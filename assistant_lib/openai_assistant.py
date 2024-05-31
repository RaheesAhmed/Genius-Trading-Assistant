from openai import OpenAI
import time
import os
import dotenv

dotenv.load_dotenv()

openai = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")

assistant_id = os.getenv("OPENAI_ASSISTANT_ID")


def create_thread(ass_id, prompt):
    # Get Assitant
    assistant = openai.beta.assistants.retrieve(ass_id)

    # create a thread
    thread = openai.beta.threads.create()
    message = openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Analyze the BTC-USD cryptocurrency pair.",
    )

    # create a message
    message = openai.beta.threads.messages.create(
        thread_id=my_thread_id, role="user", content=prompt
    )

    # run
    run = openai.beta.threads.runs.create(
        thread_id=my_thread_id,
        assistant_id=ass_id,
    )

    return run.id, thread.id


def check_status(run_id, thread_id):
    run = openai.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
    return run.status


my_run_id, my_thread_id = create_thread(
    assistant_id, "[topic]: make money with chatgpt"
)


status = check_status(my_run_id, my_thread_id)

while status != "completed":
    status = check_status(my_run_id, my_thread_id)
    time.sleep(2)


response = openai.beta.threads.messages.list(thread_id=my_thread_id)


if response.data:
    print(response.data[0].content[0].text.value)
