import json
import boto3
import random
import time

# --- CONFIGURATION ---
# We force the region to eu-central-1 so the email always works
s3_client = boto3.client('s3', region_name='eu-central-1')
sns_client = boto3.client('sns', region_name='eu-central-1')

BUCKET_NAME = 'sales-data-imran-123' 
# I put your correct ARN here for you:
TOPIC_ARN = 'arn:aws:sns:eu-central-1:376505902429:high-value-sales-topic'

def lambda_handler(event, context):
    # 1. Generate REAL Random Data
    products = ['Laptop', 'Phone', 'Mouse', 'Monitor', 'Keyboard']
    product = random.choice(products)
    
    # --- REAL MODE: Random price between $50 and $500 ---
    price = round(random.uniform(50, 500), 2) 
    
    quantity = random.randint(1, 5)
    
    sale_data = {
        'order_id': random.randint(10000, 99999),
        'product': product,
        'price': price,
        'quantity': quantity,
        'timestamp': time.time()
    }
    
    file_name = f"sales_{int(time.time())}.json"
    
    # 2. Save to S3 (Always do this)
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=json.dumps(sale_data)
    )
    print(f"Saved {file_name} to S3.")

    # 3. CHECK FOR HIGH VALUE (The Filter)
    # The Alarm only rings if price is MORE than $400
    if price > 400:
        print(f"🔥 ALERT! High value sale detected: ${price}")
        
        sns_client.publish(
            TopicArn=TOPIC_ARN,
            Message=f"Hello Imran!\n\nWe just sold a {product} for ${price}!\n\nOrder ID: {sale_data['order_id']}",
            Subject="High Value Sale Alert"
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"High Value Sale Processed: ${price}")
        }

    return {
        'statusCode': 200,
        'body': json.dumps("Normal sale processed.")
    }