import json

import requests
from django.shortcuts import render


# Create your views here.


def landing(request):
    return render(
        request,
        'marketapp/landing.html'
    )


def metaverse(request):
    return render(
        request,
        'marketapp/metaverse.html'
    )


def kakao(request):
    with open('private/token.txt', encoding='utf-8') as txtfile:
        for row in txtfile.readlines():
            token = row
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": "Bearer " + token
    }

    data = {
        "template_object": json.dumps({
            "object_type": "feed",
            "content": {
                "title": "π λΉκ³ μμν π μ μ€μ  κ²μ νμν©λλ€",
                "description": "μμΌλ‘ μμ£Ό λ§λμ!! λ λ°μ ν΄κ°κ² μ΅λλ€",
                "image_url": "https://postfiles.pstatic.net/MjAyMTEwMTNfNjQg/MDAxNjM0MDU4MTQzMjA5.yep2OdKvVyNw-Rrwl3tJSmVi3o5QFX3pOzOFRHj7R5Mg.-7elzcIyP1fFgZfeHW2e5TY8Iwa8O_2125liNTqbm_wg.PNG.polkmn249/2021-10-13-01-49-05.png?type=w966",
                "image_width": 640,
                "image_height": 640,
                "link": {
                    "web_url": "http://www.daum.net",
                    "mobile_web_url": "http://m.daum.net",
                    "android_execution_params": "contentId=100",
                    "ios_execution_params": "contentId=100"
                }
            },
            "buttons": [
                {
                    "title": "μΉμΌλ‘ μ΄λ",
                    "link": {
                        "web_url": "http://www.daum.net",
                        "mobile_web_url": "http://m.daum.net"
                    }}

            ]
        })
    }

    response = requests.post(url, headers=headers, data=data)

    return render(request, 'marketapp/landing.html')
