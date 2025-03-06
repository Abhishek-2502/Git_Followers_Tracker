from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_github_followers(username):
    url = f"https://api.github.com/users/{username}/followers"
    params = {'per_page': 100, 'page': 1}
    followers_list = []

    while True:
        response = requests.get(url, params=params)
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
    url = f"https://api.github.com/users/{username}/following"
    params = {'per_page': 100, 'page': 1}
    following_list = []

    while True:
        response = requests.get(url, params=params)
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
    if request.method == 'POST':
        username = request.form.get('username')
        followers = set(get_github_followers(username))
        following = set(get_github_following(username))

        non_followers = following - followers
        both_followers = followers & following

        return render_template('result.html', username=username, followers=followers, following=following,
                               non_followers=non_followers, both_followers=both_followers)

    return render_template('index.html')


# # FOR LOCAL HOST TESTING
# if __name__ == '__main__':
#     app.run(debug=True)