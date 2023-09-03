import psycopg2
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    key_serializer=str.encode,
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

topic_name = "hello_world"

try:
    connection = psycopg2.connect(
        user="postgres",
        password="12345",
        host="127.0.0.1",
        port="5432",
        database="sql-practice",
    )

    cursor = connection.cursor()
    postgreSQL_select_Query = """
    SELECT customer_id, order_id, order_date, order_amount 
    FROM public.customer_orders
    ORDER BY customer_id, order_date
    """

    cursor.execute(postgreSQL_select_Query)
    # print("Selecting rows from mobile table using cursor.fetchall")
    mobile_records = cursor.fetchall()

    data = []
    customer_data = {}
    order_data = []
    curr_customer = mobile_records[0][0]

    for row in mobile_records:
        # print(row[0], row[1], row[2], row[3])
        if row[0] == curr_customer:
            customer_data["customer_id"] = row[0]
            order_data.append(
                {
                    "order_id": row[1],
                    "order_date": row[2].strftime("%Y-%m-%d"),
                    "order_amount": row[3],
                }
            )
        else:
            customer_data["orders"] = order_data
            producer.send(topic_name, key="ping", value=customer_data)

            order_data = []
            customer_data = {}
            curr_customer = row[0]
            customer_data["customer_id"] = row[0]
            order_data.append(
                {
                    "order_id": row[1],
                    "order_date": row[2].strftime("%Y-%m-%d"),
                    "order_amount": row[3],
                }
            )

except Exception as e:
    print("Error: ", e)

finally:
    producer.close()
