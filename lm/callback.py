import requests

API_ENDPOINT = 'https://ai-builder-server.xnfa.now.sh/api/progress'

def progress(model, progress, done):
    # data to be sent to api
    data = {'model': model,
            'progress': progress,
            'isDone': done }

    # sending post request and saving response as response object
    requests.post(url = API_ENDPOINT, data = data)