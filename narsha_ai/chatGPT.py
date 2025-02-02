from flask import request, jsonify
from flask_restx import Resource, Api, Namespace

import openai
import os

ChatGPT = Namespace('ChatGPT')

@ChatGPT.route('/text')
class CommentMaker(Resource):
    def post(self):
        input = request.get_json()

        # request body 값
        post_content = input["post_content"]
        post_image = input["post_image"]

        # set api key
        openai.api_key = os.environ["FLASK_API_KEY"]

        # Call the chat GPT API
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 SNS 사용자이다. 조건에 맞게 문자를 댓글처럼 작성하라."},
                {"role": "system", "content": "문자는 두 문장 이내로 작성한다. 게시글 내용과 관련있는 내용으로 작성한다."},
                {"role": "user", "content": f"1. 게시글 내용: ${post_content} 2. 게시글 사진: ${post_image}"},
            ],
            temperature=0.8,
            max_tokens=2048
        )

        message_result = completion["choices"][0]["message"]["content"].encode("utf-8").decode()

        return jsonify({"result": message_result})