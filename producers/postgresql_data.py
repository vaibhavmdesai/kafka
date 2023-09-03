import psycopg2
import json

try:
    connection = psycopg2.connect(user="postgres",
                                  password="12345",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="sql-practice")

    cursor = connection.cursor()
    postgreSQL_select_Query = """
    SELECT customer_id, order_id, order_date, order_amount 
    FROM public.customer_orders
    ORDER BY customer_id, order_date
    """

    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from mobile table using cursor.fetchall")
    mobile_records = cursor.fetchall()

    data = []
    customer_data = {}
    order_data = []
    curr_customer = mobile_records[0][0]
    print(curr_customer)
    for row in mobile_records:
        print(row[0], row[1], row[2], row[3])
        if row[0] == curr_customer:
            customer_data["customer_id"] = row[0]
            order_data.append({
                "order_id": row[1],
                "order_date": row[2].strftime("%Y-%m-%d"),
                "order_amount": row[3]
            })
        else:
            # pass
            customer_data["orders"] = order_data
            data.append(customer_data)
            order_data = []
            customer_data = {}
            curr_customer = row[0]
            customer_data["customer_id"] = row[0]
            order_data.append({
                "order_id": row[1],
                "order_date": row[2].strftime("%Y-%m-%d"),
                "order_amount": row[3]
            })

    # print(data)
    with open('../data/output.json', 'w') as f:
        json.dump(data, f)

except Exception as e:
    print(e)
