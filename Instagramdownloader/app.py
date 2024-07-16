from flask import Flask, render_template, request, jsonify
import instaloader

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_media():
    profile_name = request.form['profile_name']
    
    # Create an instance of Instaloader
    L = instaloader.Instaloader()
    
    # Download only media from the target profile
    try:
        profile = instaloader.Profile.from_username(L.context, profile_name)
        for post in profile.get_posts():
            L.download_post(post, target=profile.username)
        return jsonify(success=True, message=f"Downloaded all media posts from {profile_name}")
    except instaloader.exceptions.ProfileNotExistsException:
        return jsonify(success=False, message=f"The profile {profile_name} does not exist.")
    except instaloader.exceptions.ConnectionException:
        return jsonify(success=False, message="Connection error occurred.")
    except Exception as e:
        return jsonify(success=False, message=f"An error occurred: {e}")

if __name__ == '__main__':
    app.run(debug=True)
