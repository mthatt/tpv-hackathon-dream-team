import controlflow as cf
from prefect import get_run_logger
import json

classifier = cf.Agent(
    name="Classifier",
    description="An AI agent that classifies Google Calendar events to identify spam",
    instructions="""
        Your goal should be to classify Google Calendar events to identify if
        they were created by a spammer or not. Be strict in your assessments.

        ONLY consider the `description` and `invitee_email` fields when classifying the event. Disregard all other fields.

        Categorize the event as spam if:
        - `invitee_email` does not use a legitimate email domain
        - `description` is extremely vague and consists of only one word.
        - `description` doesn't provide any context about the purpose of the meeting or event.
        - `description` contains non-descriptive content that is similar to some of the spam examples provided:

        ```
        SPAM EXAMPLES:
        email: eli@scenset.comhi, description: i'm interested
        email: henry@climatepolicyradar.org, description: Are you hiring desparate for job
        email: parash.hallur@kyndryl.com, description: asdfiyb12
        email: johnny@boeing.com, description: saturday night meet me on the town
        ```

        Categorize the event as not spam if:
        - `invitee_email` uses a legitimate business email domain
        - `description` provides context about the purpose of the meeting or event
        - `description` contains references to Data Engineering, Data Science, Machine Learning, Helm, Kubernetes
        - `description` is descriptive that is similar to some of the legit examples provided:
        ```
        LEGIT EXAMPLES:

        email: kevin@elasti.ai, description: Data engineering team capacity is low
        email: tita.ristanto@span.io, description: Prefect demo
        email: jef@operto.com, description: troubleshoot data pipelines
        email: kiran.jayasheela@mercedes-benz.com, description: Is there a Helm chart to create a Prefect Kubernetes work pool?
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
