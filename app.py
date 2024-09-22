from flask import Flask, render_template, request, redirect, url_for, session, make_response
import os
import json
import markdown
from discord_utils import get_discord_login_url, get_token, get_user_info
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

tokens = {}

allowed_characters = "abcdefghijklmnopqrstuvqxyz._01234567890"

default_profile = {
  'username': 'Loading',
  'avatar': '/static/resources/images/temp_profile.jpg',
  'onboarded': False,
  'about': '',
  'socials': {}
}

betauser_ids = []

def get_userid_from_token(token):
  if token not in tokens:
    return None
  return tokens[token]

@app.route('/')
def index():
  token = request.cookies.get('token')
  user_id = get_userid_from_token(token)
  if user_id is None:
    return render_template('index.html', user_info=default_profile)
  with open('users.json', 'r') as f:
    users = json.load(f)
  user_info = users.get(user_id)
  if user_info:
    if not user_info['onboarded']:
      return render_template('onboarding.html', user_info=user_info)
    return render_template('dashboard.html', user_info=user_info)
  else:
    return render_template('index.html', user_info=default_profile)
  
@app.route('/discord')
def discord():
  return redirect("https://discord.gg/aYN59wQrYn")

@app.route('/about')
def about():
  token = request.cookies.get('token')
  user_id = get_userid_from_token(token)
  if user_id is None:
    user_info = default_profile
  else:
    with open('users.json', 'r') as f:
      users = json.load(f)
    user_info = users.get(user_id)
  return render_template('about.html', user_info=user_info)

@app.route('/explore')
def explore():
  token = request.cookies.get('token')
  user_id = get_userid_from_token(token)
  if user_id is None:
    return redirect('/help/nice-try')
  else:
    with open('users.json', 'r') as f:
      users = json.load(f)
    user_info = users.get(user_id)
  return render_template('explore.html', user_info=user_info)

@app.route('/token-login')
def token_login():
  token = request.args.get('token')
  user_id = request.args.get('user')
  if user_id not in betauser_ids:
    return redirect('/help/nice-try')
  if token not in tokens:
    return redirect('/help/nice-try')
  # make sure the token is valid
  if user_id != tokens[token]:
    return redirect('/help/nice-try')
  response = make_response(redirect('/'))
  response.set_cookie('token', token)
  return response

@app.route('/login')
def login():
  return redirect(get_discord_login_url())

@app.route('/callback')
def callback():
  code = request.args.get('code')
  token_info = get_token(code)
  print(token_info)
  session['discord_token'] = token_info['access_token']
  user_info = get_user_info(session['discord_token'])
  
  # Write to users.csv
  user_id = user_info['id']
  username = user_info['username']
  avatar = user_info['avatar']

  if user_id not in betauser_ids:
    return redirect('/help/nice-try')

  print(f'User {username} ({user_id}) logged in.')
  print(f'Avatar: {avatar}')

  with open('users.json', 'r') as f:
    users = json.load(f)

  if user_id in users:
    # user already exists, generate a new token
    token = ''
    while token == '' or token in tokens:
      token = os.urandom(24).hex()
    tokens[token] = user_id
    new_response = make_response(redirect('/'))
    new_response.set_cookie('token', token, max_age=604800)
    # save to tokens.json
    with open('tokens.json', 'w') as f:
      json.dump(tokens, f, indent=2)
    return new_response
  else:
    # set up the user in users.json
    # see if the user has a discord profile picture
    if user_info['avatar'] is not None:
      avatar = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar}.png'
      print(f'Avatar: {avatar}')
    else:
      avatar = '/static/resources/images/temp_profile.jpg'
      print(f'Avatar: {avatar}')
    users[user_id] = {
      'username': username,
      'avatar': avatar,
      'onboarded': False,
      'about': '',
      'socials': {}
    }
    with open('users.json', 'w') as f:
      json.dump(users, f, indent=2)
      print(f'User {username} ({user_id}) added to users.json')

  session['user_info'] = user_info
  # generate a new token for the user
  token = ''
  while token == '' or token in tokens:
    token = os.urandom(24).hex()
  tokens[token] = user_id
  new_response = make_response(redirect('/'))
  # expire the token in 1 week
  new_response.set_cookie('token', token, max_age=604800)
  # save to tokens.json
  with open('tokens.json', 'w') as f:
    json.dump(tokens, f, indent=2)
  return new_response

@app.route('/logout')
def logout():
  # clear the token
  token = request.cookies.get('token')
  if token in tokens:
    del tokens[token]
    with open('tokens.json', 'w') as f:
      json.dump(tokens, f, indent=2)
  # clear the session
  session.clear()
  # remove the cookie
  response = make_response(redirect('/'))
  response.set_cookie('token', '', expires=0)
  return response

@app.route('/help')
def help():
  # grab help center json file
  with open('help-center.json', 'r') as f:
    help_center = json.load(f)
    items = []
    for category in help_center:
      for item in help_center[category]['items']:
        item['category'] = help_center[category]['name']
        item['category_description'] = help_center[category]['description']
        items.append(item)
  token = request.cookies.get('token')
  user_id = get_userid_from_token(token)
  if user_id is None:
    user_info = default_profile
  else:
    with open('users.json', 'r') as f:
      users = json.load(f)
    user_info = users.get(user_id)
  return render_template('list.html', title='Help Center', items=items, user_info=user_info)

@app.route('/help/<string:page>')
def help_page(page):
  # get markdown file from "help-guides" folder
  if not os.path.exists(f'help-guides/{page}.md'):
    return redirect('/404')
  with open(f'help-guides/{page}.md', 'r') as f:
    content = f.read()
  # convert markdown to html
  html_content = markdown.markdown(content)
  # custom markdown tag: [video:https://youtube.com/embed/etc] -> <iframe src="https://youtube.com/embed/etc"></iframe>
  html_content = html_content.replace('<--video:', '<iframe src="').replace('-->', '"></iframe>')
  token = request.cookies.get('token')
  user_id = get_userid_from_token(token)
  if user_id is None:
    user_info = default_profile
  else:
    with open('users.json', 'r') as f:
      users = json.load(f)
    user_info = users.get(user_id)
  return render_template('help.html', content=html_content, user_info=user_info)

# API Endpoints
@app.route('/api/<string:api_dir>')
def api(api_dir, methods=['GET', 'POST']):
  if request.method == 'GET':
    return redirect('/404')
  token = request.json.get('token')
  user_id = get_userid_from_token(token)
  if user_id is None:
    return {'error': 'Invalid token'}, 401
  get_json = request.json
  if api_dir == 'get':
    if get_json.get('user_id') is None:
      return {'error': 'Missing user_id'}, 400
    elif get_json.get('user_id') != user_id:
      return {'error': 'Unauthorized. You should use get_public instead.'}, 401
    with open('users.json', 'r') as f:
      users = json.load(f)
    return users[user_id]
  elif api_dir == 'get_public':
    if get_json.get('user_id') is None:
      return {'error': 'Missing user_id'}, 400
    with open('users.json', 'r') as f:
      users = json.load(f)
    the_user = users.get(get_json['user_id'])
    public_data = {
      'username': the_user['username'],
      'avatar': the_user['avatar'],
      'about': the_user['about'],
      'socials': the_user['socials']
    }
    return public_data
  elif api_dir == 'update':
    if get_json.get('user_id') is None:
      return {'error': 'Missing user_id'}, 400
    elif get_json.get('user_id') != user_id:
      return {'error': 'Unauthorized'}, 401
    with open('users.json', 'r') as f:
      users = json.load(f)
    user_info = users[user_id]
    user_info['about'] = get_json.get('about', user_info['about'])
    user_info['socials'] = get_json.get('socials', user_info['socials'])
    with open('users.json', 'w') as f:
      json.dump(users, f, indent=2)
    return {'success': True}
  else:
    return {'error': 'Invalid API endpoint'}, 404

@app.route('/api/check_username')
def check_username():
  username = request.args.get('username')
  if len(username) < 3:
    return {'success': False, 'error': 'Username must be at least 3 characters long'}
  for character in username:
    if character not in allowed_characters:
      return {'success': False, 'error': 'Username can only contain letters, numbers, and underscores'}
  with open('users.json', 'r') as f:
    users = json.load(f)
  for user_id in users:
    if users[user_id]['username'] == username and users[user_id]['onboarded']:
      return {'success': False, 'error': 'Username already taken'}
  return {'success': True}

# @app.route('/api/alias')
# def alias():
#   url = request.args.get('url')
#   # find username matching the url
#   with open('users.json', 'r') as f:
#     users = json.load(f)
#     for user_id in users:
#       if users[user_id]['username'] == url:
#         result = {
#           "success": True,
#           "url": f"save/{user_id}"
#         }
#         return result
#   return {"success": False}

@app.route('/redirect/<string:url>')
def alias(url):
  with open('users.json', 'r') as f:
    users = json.load(f)
    for user_id in users:
      if users[user_id]['username'] == url:
        return redirect(f'/save/{user_id}')
  for file in os.listdir('help-guides'):
    if file.split('.')[0] == url:
      return redirect(f'/help/{url}')
  for file in os.listdir('blogs'):
    if file.split('.')[0] == url:
      return redirect(f'/blog/{url}')
  return redirect(f'/{url}')

@app.errorhandler(404)
def page_not_found(e):
  token = request.cookies.get('token')
  user_id = get_userid_from_token(token)
  if user_id is None:
    user_info = default_profile
  else:
    with open('users.json', 'r') as f:
      users = json.load(f)
    user_info = users.get(user_id)
  return render_template('404.html', user_info=user_info, page=request.path), 404

if __name__ == '__main__':
  # Load tokens from tokens.json
  if os.path.exists('tokens.json'):
    with open('tokens.json', 'r') as f:
      tokens = json.load(f)
  # Load betauser_ids from betausers.txt (one user_id per line)
  if os.path.exists('betausers.txt'):
    with open('betausers.txt', 'r') as f:
      betauser_ids = f.read().splitlines()
  if os.environ.get('DEBUG') == 'TRUE':
    app.run(host='0.0.0.0', port=8080, debug=True)
  else:
    app.run(host='0.0.0.0', port=80)