import os

token = "7931647653:AAFwoeZ_HnZLGFMy4Ncv_giCOrxZKAUvqgA"
chat_id = "820559840"

os.system(
    f'curl -X POST "https://api.telegram.org/bot {token}/sendMessage" -H "Content-Type: application/json" -d'
)
