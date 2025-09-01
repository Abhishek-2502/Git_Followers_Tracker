from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

base_url = "https://api.github.com"

def get_github_followers(username):
    url = f"{base_url}/users/{username}/followers"
    params = {'per_page': 100, 'page': 1}
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set in environment!")
        return []
    headers = {'Authorization': f'token {token}'}

    followers_list = []

    while True:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            followers = response.json()
            if not followers:
                break
            followers_list.extend([follower['login'] for follower in followers])
            params['page'] += 1
        else:
            break

    return followers_list

def get_github_following(username):
    url = f"{base_url}/users/{username}/following"
    params = {'per_page': 100, 'page': 1}
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set in environment!")
        return []
    headers = {'Authorization': f'token {token}'}
    following_list = []

    while True:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            followings = response.json()
            if not followings:
                break
            following_list.extend([following['login'] for following in followings])
            params['page'] += 1
        else:
            break

    return following_list

@app.route('/', methods=['GET', 'POST'])
def index():
    token_warning = False
    if not os.getenv("GITHUB_TOKEN"):
        print("GITHUB_TOKEN not set in environment!")  # still logs on server
        token_warning = True

    if request.method == 'POST':
        username = request.form.get('username')
        followers = set(get_github_followers(username))
        following = set(get_github_following(username))

        # You Follow, they don't
        non_followers = following - followers

        # Mutual Followers
        both_followers = followers & following

        # they follow you, but you don’t
        not_following_back = followers - following

        return render_template('result.html', username=username, followers=followers, following=following,
                               non_followers=non_followers, both_followers=both_followers, 
                               not_following_back=not_following_back,
                               token_warning=token_warning)

    return render_template('index.html')


# # FOR LOCAL HOST TESTING
# if __name__ == '__main__':
#     app.run(debug=True)