import controlflow as cf
import json

classifier = cf.Agent(
    name="Classifier",
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
        """,
)

@cf.flow
def classify_calendar_event(event_json: str):
  event = json.loads(event_json)

  is_spam = cf.Task(
    "Classify the following calendar event to determine if it is submitted by a spammer",
    result_type=bool,
    context=dict(event=event),
    agents=[classifier],
  )

  print(is_spam)


