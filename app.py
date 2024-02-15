import os
import re
from flask import Flask, request
from openai import OpenAI

app = Flask(__name__)

openai_client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

@app.route('/', methods=["GET"])
def hello_world():
    return '5atat Python Functions'

@app.route('/get-insta-products', methods=["GET"])
def get_insta_products():
    args = request.args
    insta_user = args.get("insta_user")

    if not insta_user:
        abort(400, 'insta_user is empty')

    return "insta user: " + insta_user
    
    # # Get instance
    # L = instaloader.Instaloader(
    #     quiet=True,
    #     download_pictures=False,
    #     download_videos=False,
    #     download_video_thumbnails=False,
    #     save_metadata=False,
    #     compress_json=False,
    #     post_metadata_txt_pattern=""
    # )

    # L.login("5atatapp", "comdem-0figka-caXdob")
    # print("Logged in as 5atatapp")

    # profile = instaloader.Profile.from_username(L.context, insta_user)

    # for post in profile.get_posts():
    # media = []
    # if post.mediacount > 1:
        
    #     sidecar_nodes = post.get_sidecar_nodes()
    #     for (node in sidecar_nodes):
    #         if not node.is_video:
            