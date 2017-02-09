#!/usr/bin/env python
# coding=utf-8
import json
import falcon
import requests
import os

# **** LINE params **** #
REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', '')

# **** docomo params **** #
DOCOMO_API_KEY = os.environ.get('DOCOMO_API_KEY', '')

print('LINE_CHANNEL_ACCESS_TOKEN:' + LINE_CHANNEL_ACCESS_TOKEN)
print('DOCOMO_API_KEY:' + DOCOMO_API_KEY)

class Line(object):
    # docomo context
    contextId = ""
    # docomo appUserId
    appUserId = ""
    # docomo appUserId
    serverSendTime = ""

    # line response header
    header = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer {}'.format(LINE_CHANNEL_ACCESS_TOKEN)
    }

    # docomo dialogue api
    def call_dialogue(self, input, contextid):
        try:
            json_data = {'utt': input,
                         'context': contextid,
                         't': ('30')  # docomo baby style
                         }
            docomo_res = requests.post(
                'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY=' + DOCOMO_API_KEY,
                json.dumps(json_data),
                headers={'Content-Type': 'application/json'})
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_503,
                                   'Docomo API Error. ',
                                   'Could not invoke docomo api.')
        resjson = docomo_res.json()
        return resjson

    # docomo sentenceUnderstanding api
    def call_sentenceUnderstanding(self, input, contextid):
        try:
            json_data = {
                "projectKey": "OSU", # static
                "appInfo": {
                    "appName": "hoge_app", # no matter?
                    "appKey": "hoge_app01" # no matter?
                },
                "clientVer": "1.0.0", # static
                "dialogMode": "off", # static
                "language": "ja", # static
                "userId": "12 123456 123456 0", # no matter?
                "location": {
                    "lat": "139.766084", # no matter?
                    "lon": "35.681382" # no matter?
                },
                "userUtterance": {
                    "utteranceText": "これは、固定分の意図解釈を実施しています。" #input
                }
            }
            docomo_res = requests.post(
                'https://api.apigw.smt.docomo.ne.jp/sentenceUnderstanding/v1/task?APIKEY=' + DOCOMO_API_KEY,
                json.dumps(json_data),
                headers={'Content-Type': 'application/json'})
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_503,
                                   'Docomo API Error. ',
                                   'Could not invoke docomo api.')
        resjson = docomo_res.json()
        return resjson


    # docomo scenarioDialogue api
    def call_scenarioDialogueInit(self):
        try:
            json_data = {
                "botId": "APIBot" # static
            }
            docomo_res = requests.post(
                'https://api.apigw.smt.docomo.ne.jp/scenarioDialogue/v1/registration?APIKEY=' + DOCOMO_API_KEY,
                json.dumps(json_data),
                headers={'Content-Type': 'application/json'})
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_503,
                                   'Docomo API Error. ',
                                   'Could not invoke docomo api.')
        resjson = docomo_res.json()
        return resjson

    def call_scenarioDialogue(self, input, appUserId, serverSendTime):

        if (input == 'init'):
            initTalkingFlag = 'true'
            serverSendTime = '2017-02-08 17:48:00'
            initTopicId = "APITOPIC"
        else:
            initTalkingFlag = 'false'
            initTopicId = ""

        print('initTalkingFlag:' + initTalkingFlag)
        print('input:' + input)
        print('appUserId:' + appUserId)
        print('serverSendTime:' + serverSendTime)
        try:
            json_data = {
                "appUserId": appUserId,
                "botId": "APIBot", # static
                "voiceText": input,
                "initTalkingFlag": initTalkingFlag, # 1st:true / other:false
                "initTopicId": initTopicId, # 1st: must "APITOPIC"
                "appRecvTime": serverSendTime, # 1st:now / other:lasttime
                "appSendTime": serverSendTime # temp
            }
            docomo_res = requests.post(
                'https://api.apigw.smt.docomo.ne.jp/scenarioDialogue/v1/dialogue?APIKEY=' + DOCOMO_API_KEY,
                json.dumps(json_data),
                headers={'Content-Type': 'application/json'})
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_503,
                                   'Docomo API Error. ',
                                   'Could not invoke docomo api.')
        resjson = docomo_res.json()
        return resjson



    # def on_get(self, req, resp):
    #     msg = {
    #         "GET": "Line:Hello!"
    #     }
    #     resp.body = json.dumps(msg)

    def on_post(self, req, resp):

        # get body
        body = req.stream.read()
        # get json
        receive_params = json.loads(body.decode('utf-8'))


        print('receive_params: {}'.format(receive_params))

        # get events for loop
        for event in receive_params['events']:

            if event['type'] == 'message':

                # define
                user_input = event['message']['text']

                # switch

                # **** LINE template-message call **** #
                if user_input == 'template':

                    send_content = {
                        'replyToken': event['replyToken'],
                        "messages": [
                            {
                                'type': 'text',
                                'text': 'template-message called'
                            },
                            # Buttons
                            {
                                "type": "template",
                                "altText": "this is a confirm template",
                                "template": {
                                    "type": "buttons",
                                    "thumbnailImageUrl": "https://dimora.jp/pushimg/3/301693000238_h.jpg",
                                    "text": "沈黙見る？",
                                    "actions": [
                                        {
                                            "type": "message",
                                            "label": "Yes",
                                            "text": "yes"
                                        },
                                        {
                                            "type": "message",
                                            "label": "No",
                                            "text": "no"
                                        },
                                        {
                                            "type": "uri",
                                            "label": "詳細を",
                                            "uri": "https://ja.wikipedia.org/wiki/%E6%B2%88%E9%BB%99_-%E3%82%B5%E3%82%A4%E3%83%AC%E3%83%B3%E3%82%B9-"
                                         }
                                    ]
                                }
                            },
                            # Confirm
                            {
                                "type": "template",
                                "altText": "this is a confirm template",
                                "template": {
                                    "type": "confirm",
                                    "text": "Are you sure?",
                                    "actions": [
                                        {
                                            "type": "message",
                                            "label": "Yes",
                                            "text": "yes"
                                        },
                                        {
                                            "type": "message",
                                            "label": "No",
                                            "text": "no"
                                        }
                                    ]
                                }
                            },
                            # Carousel
                            {
                                "type": "template",
                                "altText": "おすすめレストラン",
                                "template": {
                                    "type": "carousel",
                                    "columns": [

                                        {
                                            "thumbnailImageUrl": "https://www.tis.co.jp/common/images/logo_tis.png",
                                            "title": "TIS株式会社",
                                            "text": "TIS、自律移動型ロボット開発ベンチャーのSEQSENSEへ出資",
                                            "actions": [

                                                {
                                                    "type": "uri",
                                                    "label": "詳細を見る",
                                                    "uri": "https://www.tis.co.jp"
                                                }
                                            ]
                                        },
                                        {
                                            "thumbnailImageUrl": "https://www.tis.co.jp/common/images/logo_tis.png",
                                            "title": "TIS新卒",
                                            "text": "2017.1.28　2018年度新卒採用サイトをリニューアルオープンしました！",
                                            "actions": [

                                                {
                                                    "type": "uri",
                                                    "label": "詳細を見る",
                                                    "uri": "http://www.tis.co.jp/recruit"
                                                }
                                            ]
                                        },
                                        {
                                            "thumbnailImageUrl": "https://www.tis.co.jp/common/images/logo_tis.png",
                                            "title": "TIS株式会社",
                                            "text": "TIS、自律移動型ロボット開発ベンチャーのSEQSENSEへ出資",
                                            "actions": [

                                                {
                                                    "type": "uri",
                                                    "label": "詳細を見る",
                                                    "uri": "https://www.tis.co.jp"
                                                }
                                            ]
                                        },
                                        {
                                            "thumbnailImageUrl": "https://www.tis.co.jp/common/images/logo_tis.png",
                                            "title": "TIS新卒",
                                            "text": "2017.1.28　2018年度新卒採用サイトをリニューアルオープンしました！",
                                            "actions": [

                                                {
                                                    "type": "uri",
                                                    "label": "詳細を見る",
                                                    "uri": "http://www.tis.co.jp/recruit"
                                                }
                                            ]
                                        },

                                    ]
                                }
                            }
                        ]
                    }

                else:

                    # **** docomo API call **** #

                    # **** sentenceUnderstanding **** #
                    if user_input == 'u':
                        resjson_sentenceUnderstanding = self.call_sentenceUnderstanding(user_input, self.contextId)
                        # overwrite sys_utt
                        sys_utt = json.dumps(resjson_sentenceUnderstanding, ensure_ascii=False)

                    # **** scenarioDialogue **** #
                    elif user_input == 's':
                        # init mode
                        print('call_scenarioDialogueInit')
                        resjson_scenarioDialogue = self.call_scenarioDialogueInit()
                        self.appUserId = resjson_scenarioDialogue['appUserId']

                        # overwrite sys_utt
                        sys_utt = 'シナリオモード開始。「init」とタイプしてね！'

                    elif self.appUserId != '':
                        # scenario mode
                        print('call_scenarioDialogue')
                        resjson_scenarioDialogue = self.call_scenarioDialogue(user_input,
                                                                              self.appUserId, self.serverSendTime)
                        print(json.dumps(resjson_scenarioDialogue, ensure_ascii=False))

                        # store docomo receivedtime
                        self.serverSendTime = resjson_scenarioDialogue['serverSendTime']
                        # overwrite sys_utt
                        # sys_utt = json.dumps(resjson_scenarioDialogue, ensure_ascii=False)
                        sys_utt = json.dumps(resjson_scenarioDialogue['systemText']['expression'], ensure_ascii=False)

                    # **** dialogue **** #
                    else:
                        resjson = self.call_dialogue(user_input, self.contextId)
                        sys_utt = resjson['utt']
                        self.contextId = resjson["context"]

                    # make response
                    send_content = {
                        'replyToken': event['replyToken'],
                        'messages': [
                            {
                                'type': 'text',
                                'text': sys_utt
                            }
                        ]
                    }
                # LINE response
                send_content = json.dumps(send_content)
                # logger.debug('send_content: {}'.format(send_content))

                res = requests.post(REPLY_ENDPOINT, data=send_content, headers=self.header)
                # logger.debug('res: {} {}'.format(res.status_code, res.reason))

                resp.body = json.dumps('OK')

class LinePush(object):
    def on_post(self, req, resp):
        self.push_message()
        self.get_profile()

    def on_get(self, req, resp):
        self.push_message()
        self.get_profile()

    def push_message(self):

        try:
            json_data = {
                "to": "U69b93081ef731fdaf077813f65296ebc", # yamashita
                "messages":[
                    {
                        "type": "text",
                        "text": "Hello, world1"
                    },
                    {
                        "type": "text",
                        "text": "Hello, world2"
                    }
                ]
            }
            # NG. Why not? --> 'https://api.line.me/v2/bot/message/multicast',
            line_res = requests.post(
                'https://api.line.me/v2/bot/message/push',
                json.dumps(json_data),
                headers=Line.header
                         )
        except Exception:
            print('Exception:' + Exception)
            raise falcon.HTTPError(falcon.HTTP_503,
                                   'LINE API Error. ',
                                   'Could not invoke LINE api.')
        resjson = line_res.json()
        return resjson

    def get_profile(self):
        try:
            line_res = requests.get(
                'https://api.line.me/v2/bot/profile/' + "U69b93081ef731fdaf077813f65296ebc",
                headers=Line.header
            )
        except Exception:
            print('Exception:' + Exception)
            raise falcon.HTTPError(falcon.HTTP_503,
                                   'LINE API Error. ',
                                   'Could not invoke LINE api.')
        resjson = line_res.json()
        print(resjson)
        return resjson

app = falcon.API()
app.add_route("/line", Line())
app.add_route("/linepush", LinePush())
# app.add_route("/", HelloResource())
# app.add_route("/line/name", LineName())

if __name__ == "__main__":
    # HTTP
    from wsgiref import simple_server

    httpd = simple_server.make_server("0.0.0.0", 80, app)  # all ipadress free / port:80
    httpd.serve_forever()

    # HTTPS
    # httpd = simple_server.make_server("0.0.0.0", 443, app) # all ipadress free / port:443
    # httpd.socket = ssl.wrap_socket(httpd.socket, certfile='cert1.pem', keyfile='privkey1.pem',  server_side=True)
    # httpd.serve_forever()
