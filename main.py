import controlflow as cf
from prefect import get_run_logger
import json
# from langchain_openai import ChatOpenAI

classifier = cf.Agent(
    name="Classifier",
    # model=ChatOpenAI(model_name="gpt-3.5-turbo"),
    description="An AI agent that classifies Google Calendar events to identify spam",
    instructions="""
        Your goal should be to classify Google Calendar events to identify if
        they were created by a spammer or not. Be strict in your assessments.

        only classify the event as spam if it is very likely to be spam based on these examples:

        ```
        SPAM EXAMPLES:

        description: 3109889710
        description: Cowbell
        description: asdf
        ```

        ```
        LEGIT EXAMPLES:

        description: Orchestration
        description: Im a data engineer
        ```
        """,
)

@cf.flow
def classify_calendar_event(event_json: str):
  logger = get_run_logger()
  logger.info(f"Classifying event: {event_json}")
  # Event JSON schema: {"description": str, "created_date": str, "event_name": str, "invitee_email": str, "event_id": str}
  event = json.loads(event_json)

  is_spam = cf.Task(
    "Classify the following calendar event to determine if it is submitted by a spammer",
    result_type=bool,
    context=dict(event=event),
    agents=[classifier],
  )

  logger.info(f"Is spam: {is_spam}")

if __name__ == "__main__":
  classify_calendar_event.serve(
    name="classify-calendar-event",
  )
