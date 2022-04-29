import os
import json
from datetime import datetime
from flask import make_response, request
from flask_restful import Resource
from trans_util import get_translation, load_t5_model


class IndicTranslator(Resource):
    def __init__(self):
        self.response_data = {
            "status": "fail",
            "message": "Invalid payload."
        }

        self.logfile = 'service.log'

    def post(self):
        is_parse = request.is_json
        if not is_parse:
            self.response_data["message"] = "Request error!"
            response = json.dumps(self.response_data, indent=2)
            return make_response(response, 200)

        content = request.get_json()
        try:
            lang = content["lang"]
            text = content["text"]
        except Exception as error:
            self.response_data["message"] = repr(error)
            response = json.dumps(self.response_data, indent=2)
            return make_response(response, 200)

        # translate text
        with open(self.logfile, 'a') as f:
            # logging
            cur_time = datetime.now().strftime("%m-%d-%Y  %H:%M:%S")
            f.write("========  {}  ========\n".format(cur_time))
            f.write("Language: {}\n".format(lang))
            f.write("Source text:\n{}\n".format(text))

            try:
                result_text, score = get_translation(text, lang)
                
                f.write("Output text:\n\t{}\n".format(result_text))
                f.write("Bleu Score:\t{}\n".format(score))

                self.response_data["status"] = "success"
                self.response_data["message"] = "score: {}\ntext:\n{}".format(
                    score, result_text)
                response = json.dumps(self.response_data, indent=2)

            except Exception as error:
                f.write("Output text:\n\t{}\n".format(repr(error)))

                self.response_data["message"] = repr(error)
                response = json.dumps(self.response_data, indent=2)


            f.write("****************************************\n\n")

        return make_response(response, 200)
