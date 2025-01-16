import logging
import random
import time
from datetime import datetime

import psycopg2
import simplejson as json
from confluent_kafka import Consumer, KafkaError, SerializingProducer

from main import delivery_report

logging.basicConfig(level=logging.INFO)

# Kafka configuration
conf = {'bootstrap.servers': 'localhost:9092'}
consumer = Consumer(conf | {'group.id': 'voting-group', 'auto.offset.reset': 'earliest', 'enable.auto.commit': False})
producer = SerializingProducer(conf)

# Database connection
with psycopg2.connect("host=localhost dbname=voting user=postgres password=postgres") as conn:
    with conn.cursor() as cur:
        # Fetch candidates
        cur.execute("SELECT row_to_json(t) FROM (SELECT * FROM candidates) t;")
        candidates = [candidate[0] for candidate in cur.fetchall()]
        if not candidates:
            raise Exception("No candidates found in the database")

        logging.info(f"Candidates: {candidates}")

        # Subscribe to voters_topic
        consumer.subscribe(['voters_topic'])

        try:
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                elif msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logging.error(msg.error())
                        break

                # Process voter message
                voter = json.loads(msg.value().decode('utf-8'))
                chosen_candidate = random.choice(candidates)
                vote = voter | chosen_candidate | {
                    "voting_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    "vote": 1
                }

                try:
                    logging.info(f"User {vote['voter_id']} is voting for candidate: {vote['candidate_id']}")
                    cur.execute("""
                        INSERT INTO votes (voter_id, candidate_id, voting_time)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (voter_id, candidate_id) DO NOTHING;
                    """, (vote['voter_id'], vote['candidate_id'], vote['voting_time']))
                    conn.commit()

                    producer.produce(
                        'votes_topic',
                        key=vote["voter_id"],
                        value=json.dumps(vote),
                        on_delivery=delivery_report
                    )
                    producer.poll(0)
                except Exception as e:
                    logging.error(f"Error processing vote: {e}")
                    conn.rollback()
                    continue
                time.sleep(0.2)
        finally:
            consumer.close()
            producer.flush()
