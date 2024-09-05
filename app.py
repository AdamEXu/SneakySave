from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
import markdown
from discord_utils import get_discord_login_url, get_token, get_user_info

app = Flask(__name__)

@app.route('/')
def index():
  user_info = session.get('user_info')
  if user_info:
    if user_info['onboarding-state'] != -1:
      return redirect('/onboarding')
    return render_template('dashboard.html', user_info=user_info)
  else:
    return render_template('index.html')

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
  discriminator = user_info['discriminator']
  avatar = user_info['avatar']
  
  # check if user exists in users.json
  with open('users.json', 'r') as f:
    users = json.load(f)
  if user_id not in users:
    users[user_id] = {
      'username': username,
      'discriminator': discriminator,
      'avatar': avatar,
      'onboarding-state': 0,
      'about': '',
      'socials': {}
    }
    with open('users.json', 'w') as f:
      json.dump(users, f, indent=2)
  
  session['user_info'] = user_info
  return redirect('/')

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')

@app.route('/explore')
def explore():
  return render_template('explore.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/onboarding')
def onboarding():
  return render_template('onboarding.html')

@app.route('/help/<string:page>')
def help(page):
  # get markdown file from "help-guides" folder
  if not os.path.exists(f'help-guides/{page}.md'):
    return redirect('/404')
  with open(f'help-guides/{page}.md', 'r') as f:
    content = f.read()
  # convert markdown to html
  html_content = markdown.markdown(content)
  # custom markdown tag: [video:https://youtube.com/embed/etc] -> <iframe src="https://youtube.com/embed/etc"></iframe>
  html_content = html_content.replace('[video:', '<iframe src="').replace(']', '"></iframe>')
  return render_template('help.html', content=html_content)

# API Endpoints
@app.route('/api/get-user-onboarding-state')
def get_user_onboarding_state():
  user_id = session.get('user_info')['id']
  with open('users.json', 'r') as f:
    users = json.load(f)
  return users[user_id]['onboarding-state']

@app.route('/api/update-user-onboarding-state', methods=['POST'])
def update_user_onboarding_state():
  user_id = session.get('user_info')['id']
  with open('users.json', 'r') as f:
    users = json.load(f)
  users[user_id]['onboarding-state'] = request.json['onboarding-state']
  with open('users.json', 'w') as f:
    json.dump(users, f, indent=2)
  return 'ok'

@app.route('/api/get-user-info')
def get_user_info_api():
  user_info = session.get('user_info')
  return user_info

@app.route('/api/get-users')
def get_users():
  with open('users.json', 'r') as f:
    users = json.load(f)
  return users

@app.route('/api/get-public-saves')
def get_public_saves():
  user_id = request.args.get('user_id')
  with open('saves.json', 'r') as f:
    saves = json.load(f)
  user_saves = []
  for save in saves:
    if save['user_id'] == user_id and save['public']:
      user_saves.append(save)
  return user_saves


@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

if __name__ == '__main__':
  if os.environ.get('DEBUG') == 'TRUE':
    app.run(host='0.0.0.0', port=8080, debug=True)
  else:
    app.run(host='0.0.0.0', port=80)