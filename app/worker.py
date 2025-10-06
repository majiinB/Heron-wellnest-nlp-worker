def start_worker():
    from google.cloud import pubsub_v1
    from app.services.nlp_service import NLPService
    from app.config.env_config import env
    import json

    PROJECT_ID = "heron-wellnest"
    SUBSCRIPTION_ID = "journal-topic-sub"
    id_to_label = {
        0: "Anxiety",
        1: "Normal",
        2: "Depression",
        3: "Suicidal",
        4: "Stress"
    }

    nlp_service = NLPService(model_path=env.MODEL_PATH, id_to_label=id_to_label)
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    def callback(message):
        try:
            # Decode and parse the message payload
            data = message.data.decode("utf-8")
            payload = json.loads(data)  # convert JSON string to dict

            # Extract journal content
            content = payload.get("content", "")
            print(f"Received: {payload}")
            print(f"Received content: {content}")

            # Run your NLP analysis
            preds = nlp_service.analyze_text([content])
            print(f"Prediction: {preds}")

            # Acknowledge message after successful processing
            message.ack()

        except Exception as e:
            print(f"Worker error: {e}")
            message.nack()  # optional — retries the message

    print(f"Listening on {subscription_path}")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    with subscriber:
        try:
            streaming_pull_future.result()
        except Exception as e:
            print(f"Worker error: {e}")
            streaming_pull_future.cancel()