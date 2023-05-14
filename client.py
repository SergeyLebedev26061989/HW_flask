import requests

# response = requests.get(
#     "http://127.0.0.1:5000/ad/1",
# )
# response = requests.post(
#     "http://127.0.0.1:5000/ad/",
#     json={
#         "title": "Объявление_1",
#         "description": "Продам кирпич",
#         "user": "mr.Bin",
#     },
# )
# response_3 = requests.patch(
#     "http://127.0.0.1:5000/ad/1", json={'description': 'Отдам бесплатно'}
# )
response = requests.get(
    "http://127.0.0.1:5000/ad/1",
)
print(response.json())
