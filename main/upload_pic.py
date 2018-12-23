from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import os
import tempfile


@csrf_exempt
def upload_pic(request):
    return_message = dict()
    if request.method == 'POST':
        try:
            # Decode
            # ===============================
            encoded_json = request.body.decode('utf-8')
            json_body = json.loads(encoded_json)
            path = json_body['path']
            preprocessMethod = json_body['path']
            featureExtractionMethod = json_body['featureExtractionMethod']
            similarityCalculationMethod = json_body['similarityCalculationMethod']
            # ===============================

            # Compute
            # ===============================

            # Somehow get the answer

            # ===============================

            # Generate the json
            # ===============================
            # 0
            return_message['rawImage'] = 'FOO'  # the raw path
            # 1
            return_message['recallRatio'] = 'FOO'  # "92.5%" 查全率
            # 2
            return_message['precision'] = 'FOO'  # "87.5%" 查准率
            # 3
            features = dict()
            features['color'] = 'FOO'  # path of the generated image
            features['texture'] = 'FOO'  # path of the generated image
            features['shape'] = 'FOO'  # path of the generated image
            return_message['features'] = features

            # 4
            results = dict()
            # 4.1
            one = dict()
            one['similarity'] = 'FOO'
            one['path'] = 'FOO'
            one_features = dict()
            one_features['color'] = 'FOO'
            one_features['texture'] = 'FOO'
            one_features['shape'] = 'FOO'
            one['features'] = one_features
            # 4.2
            two = dict()
            two['similarity'] = 'FOO'
            two['path'] = 'FOO'
            two_features = dict()
            two_features['color'] = 'FOO'
            two_features['texture'] = 'FOO'
            two_features['shape'] = 'FOO'
            two['features'] = two_features
            # 4.3
            three = dict()
            three['similarity'] = 'FOO'
            three['path'] = 'FOO'
            three_features = dict()
            three_features['color'] = 'FOO'
            three_features['texture'] = 'FOO'
            three_features['shape'] = 'FOO'
            three['features'] = three_features
            # 4
            results['one'] = one
            results['two'] = two
            results['three'] = three
            return_message['results'] = results
            # ===============================

            # Write the result to file
            # ===============================
            temp_dir = tempfile.gettempdir() + '/SimpleCBIR_ResultTemp'

            # Try to make the temp folder
            try:
                os.mkdir(temp_dir)
            except Exception as x:
                print(str(x))

            # Try to write the json file
            try:
                busy = open(temp_dir + "/result.json.busy", 'w')
                result_json = open(temp_dir + '/result.json', 'w')
                json.dump(return_message, result_json)
                result_json.close()
                busy.close()
                import time
                time.sleep(5)
                os.remove(temp_dir + '/result.json.busy')

            # Make sure everything is closed and deleted if anything bad occurs.
            except Exception as x:
                try:
                    busy.close()
                except Exception as e:
                    print(str(e))
                    print("Busy Doesn't Exist.")
                try:
                    os.remove(temp_dir + '/result.json.busy')
                except Exception as e:
                    print(str(e))
                    print("Busy Doesn't Exist.")
                try:
                    result_json.close()
                except Exception as e:
                    print(str(e))
                    print("Result Doesn't Exist.")
                try:
                    os.remove(temp_dir + '/result.json')
                except Exception as e:
                    print(str(e))
                    print("Result Doesn't Exist.")

                # Raise the exception to the upper level.
                raise x
            # ===============================

        except Exception as e:
            return HttpResponseBadRequest(str(e))
    else:
        return HttpResponseBadRequest('Not a POST request.')

    # Return http status 200
    return HttpResponse()
