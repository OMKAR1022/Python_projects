import random
import time

def get_next_timestamp(current_timestamp):
    if current_timestamp[-3:] == '829':
        current_timestamp = str(int(current_timestamp) + 1).zfill(14)
    return current_timestamp

timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
while True:
    timestamp = get_next_timestamp(timestamp)
    number = random.randint(1, 9)
    result_type = random.choice(['big', 'small'])
    color = random.choice(['red', 'green', 'mix'])
    print(f"{timestamp}\t{number}\t{result_type}\t{color}")
    time.sleep(30)
