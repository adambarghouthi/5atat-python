import os
import re
import json
from flask import Flask, jsonify, request
from openai import OpenAI

app = Flask(__name__)

openai_client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class Product:
    def __init__(self, name, description, price, sizes, colours, active, images):
        self.name = name
        self.description = description
        self.price = price
        self.sizes = sizes
        self.colours = colours
        self.active = active
        self.images = images

@app.route('/', methods=["GET"])
def hello_world():
    return jsonify({
        'status': 200,
        'message': 'Welcome to 5atat Python Functions'
    })

@app.route('/get-insta-products', methods=["GET"])
def get_insta_products():
    args = request.args
    insta_user = args.get("insta_user")

    if not insta_user:
        return jsonify({
            'status': 400,
            'message': 'insta_user cannot be empty.'
        })

    # Get instance
    L = instaloader.Instaloader(
        quiet=True,
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        save_metadata=False,
        compress_json=False,
        post_metadata_txt_pattern=""
    )

    L.login("5atatapp", "comdem-0figka-caXdob")
    print("Logged in as 5atatapp")

    profile = instaloader.Profile.from_username(L.context, insta_user)

    products = []
    count = 0

    for post in profile.get_posts():
        if post.is_video:
            continue

        media = []

        if post.mediacount > 1:
            sidecar_nodes = post.get_sidecar_nodes()
            for (node in sidecar_nodes):
                if not node.is_video:
                    media.append(node.url)
        else:
            media.append(post.url)

        caption = re.sub(r"[#|@]([a-zA-Z0-9-_.]+)", "", post.caption)
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are given a product description. You only have to extract the following: name, description, price, sizes, colours, and active. Just use what is given. Price is a number. Make it 0 if not found. Sizes and colours are empty arrays or arrays of strings. Active is a boolean. Make false if product is not available. Spell colours with 'ou' not 'o'. Output in a JSON object."},
                {"role": "user", "content": caption}
            ]
        )
        json_response = json.loads(response.choices[0].message.content)

        products.append(Product(
            name=json_response.name,
            description=json_response.description,
            price=json_response.price,
            sizes=json_response.sizes,
            colours=json_response.colours,
            active=json_response.active,
            images=media
        ))

        count += 1
    
    return jsonify({
        'status': 200,
        'products': products
    })

