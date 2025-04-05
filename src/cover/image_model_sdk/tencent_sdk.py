# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import sys
import time
import base64
from datetime import datetime
import os
import requests
from src.config import TENCENT_SECRET_ID, TENCENT_SECRET_KEY

if sys.version_info[0] <= 2:
    from httplib import HTTPSConnection
else:
    from http.client import HTTPSConnection


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def post_request(action, payload):
    secret_id = TENCENT_SECRET_ID
    secret_key = TENCENT_SECRET_KEY
    token = ""
    service = "hunyuan"
    host = "hunyuan.tencentcloudapi.com"
    region = "ap-guangzhou"
    version = "2023-09-01"
    params = json.loads(payload)
    endpoint = "https://hunyuan.tencentcloudapi.com"
    algorithm = "TC3-HMAC-SHA256"
    timestamp = int(time.time())
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    # ************* step 1 canonical request *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (
        ct,
        host,
        action.lower(),
    )
    signed_headers = "content-type;host;x-tc-action"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (
        http_request_method
        + "\n"
        + canonical_uri
        + "\n"
        + canonical_querystring
        + "\n"
        + canonical_headers
        + "\n"
        + signed_headers
        + "\n"
        + hashed_request_payload
    )

    # ************* step 2 string to sign *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(
        canonical_request.encode("utf-8")
    ).hexdigest()
    string_to_sign = (
        algorithm
        + "\n"
        + str(timestamp)
        + "\n"
        + credential_scope
        + "\n"
        + hashed_canonical_request
    )

    # ************* step 3 calculate signature *************
    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(
        secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    # ************* step 4 build authorization *************
    authorization = (
        algorithm
        + " "
        + "Credential="
        + secret_id
        + "/"
        + credential_scope
        + ", "
        + "SignedHeaders="
        + signed_headers
        + ", "
        + "Signature="
        + signature
    )

    # ************* step 5 build and send request *************
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json; charset=utf-8",
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Timestamp": timestamp,
        "X-TC-Version": version,
    }
    if region:
        headers["X-TC-Region"] = region
    if token:
        headers["X-TC-Token"] = token

    try:
        req = HTTPSConnection(host)
        req.request("POST", "/", headers=headers, body=payload.encode("utf-8"))
        resp = req.getresponse()
        return resp.read()
    except Exception as err:
        print(err)


def hunyuan_generate_cover(your_file_path):
    submit_action = "SubmitHunyuanImageJob"
    with open(your_file_path, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode("utf-8")
    payload = f'{{"Prompt":"这是一个视频截图，请尝试根据该图生成对应的动漫类型的封面","Style":"riman","ContentImage":{{"ImageBase64":"data:image/png;base64,{data}"}}}}'
    submit_return = post_request(submit_action, payload).decode("utf-8")
    job_id = json.loads(submit_return)["Response"]["JobId"]
    query_action = "QueryHunyuanImageJob"
    payload = f'{{"JobId":"{job_id}"}}'
    max_retries = 30
    retries = 0
    while retries < max_retries:
        query_return = post_request(query_action, payload).decode("utf-8")
        if json.loads(query_return)["Response"]["JobStatusCode"] == "5":
            image_url = json.loads(query_return)["Response"]["ResultImage"][0]
            img_data = requests.get(image_url).content
            cover_name = time.strftime("%Y%m%d%H%M%S") + ".png"
            temp_cover_path = os.path.join(os.path.dirname(your_file_path), cover_name)
            with open(temp_cover_path, "wb") as handler:
                handler.write(img_data)
            os.remove(your_file_path)
            return temp_cover_path
        else:
            time.sleep(1)
            retries += 1
    return None


if __name__ == "__main__":
    print(hunyuan_generate_cover(""))
