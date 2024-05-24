import requests

def test_fpl_url():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()  # Assuming the content is JSON
    else:
        return {
            'statusCode': 400,
            'body': 'Failed'
        }
    
x = test_fpl_url()
print(x)