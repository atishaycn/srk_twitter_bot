import openai
from loguru import logger
import os


def get_reply(text):

    with open('output_file_append.txt', 'r') as file:
        content = file.read()

    seen = set()
    unique_string = ""
    for line in content.split("\n"):
        # logger.info(line)
        if line in seen:
            # logger.info('already seen')
            continue
        seen.add(line)
        unique_string += line + "\n"

    openai.api_key = os.getenv("OPENAI_API_KEY")

    MODEL = "gpt-4"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Shahrukh Khan is said to be one the wittiest bollywood actors. \
                    Then look at all the conversations below he has had with fans on twitter. fans questions and tweets start with 'fan's tweet' and his replies are after 'srk's reply:'. Your job is to learn is his style, humor and reply to my questions as he would. when sending the output just give the text after 'srk's reply:'. "},
            {"role": "system", "content": unique_string},
            {"role": "assistant",
                "content": "What tweet do you need a reply to in SRK style?"},
            {"role": "user", "content":  text},
        ],
        temperature=0,
    )
    reply = response.choices[0].message['content']
    reply = reply.replace("@theatishay", "")
    reply = reply.replace("SRK's reply:", "")
    reply = reply.replace("srk's reply:", "")
    reply = reply.strip()
    logger.info(reply)
    return reply
