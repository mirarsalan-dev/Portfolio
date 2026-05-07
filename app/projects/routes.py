import os
from flask import Blueprint, render_template
import requests

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/')
def showcase():
    github_username = "mirarsalan2006-ship-it" 
    url = f"https://api.github.com/users/mirarsalan2006-ship-it/repos"
    
    # Securely load the token from your .env file
    github_token = os.getenv('GITHUB_TOKEN')
    
    # Prepare the headers. If the token exists, attach it. 
    # If not (like during initial setup), it falls back to an empty dictionary.
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    try:
        params = {'sort': 'updated', 'direction': 'desc'}
        
        # Pass the headers directly into the request
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status() 
        
        repos = response.json()
        repos = [repo for repo in repos if not repo['fork']]
        
    except requests.RequestException as e:
        print(f"Error fetching GitHub repos: {e}")
        repos = [] 

    return render_template('projects.html', projects=repos)