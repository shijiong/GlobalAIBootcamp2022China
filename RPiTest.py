'''
Microsoft Cognitive Services and Azure IotHub Quickstart for Raspberry Pi 4. 
Uses local and remote images in each example.
Prerequisites:
    - Install the Computer Vision SDK:
      pip install --upgrade azure-cognitiveservices-vision-computervision
    - Install the Azure IoTHub device SDK
      pip install azure-iot-device --user
    - Install the Azure Blob Storage SDK
      pip install azure-storage-blob
    - Install Webcamera lib fswebcam
      sudo apt-get install fswebcam
    - Install PIL:
      pip install --upgrade pillow
      All the local images and remote images are downloaded from https://github.com/Azure-Samples/cognitive-services-sample-data-files/tree/master/ComputerVision/Images

Run the entire file to demonstrate the following examples:
    - Describe Image - local
    - Describe Image - remote
    - Describe Image - camera
    - Detect Faces - local
    - Detect Faces - remote
    - Detect Faces - camera
References:
    - SDK: https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-vision-computervision/azure.cognitiveservices.vision.computervision?view=azure-python
    - Documentaion: https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/index
    - API: https://westus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-2/operations/5d986960601faab4bf452005
'''
# <snippet_imports_and_vars>
# <snippet_imports>
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure.storage.blob import ContentSettings, BlobClient
from azure.iot.device import Message
from azure.iot.device.aio import IoTHubDeviceClient

from array import array
import os
from PIL import Image
import sys
import time
from PIL import ImageDraw
import matplotlib.pyplot as plt
import asyncio
import threading
# </snippet_imports>
'''
Authenticate
Authenticates your credentials and creates a client.
'''
# <snippet_vars>
subscription_key = "c89efbf9c5bb45cab362d300eab052a8"
endpoint = "https://globalaicomputervisiondemo.cognitiveservices.azure.com/"
# </snippet_vars>
# </snippet_imports_and_vars>

# <snippet_client>
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
# </snippet_client>

#Bolb Storage
conn_str="DefaultEndpointsProtocol=https;AccountName=myiotservicestorage;AccountKey=jVkqfT8DXIWCQQ3vFipe1mWdRtwutaz1zBR5BEeZorc2U9tt5t3aR4EA5NXQMfRDSLl2vloZGQ+jK+R+KTKUTg==;BlobEndpoint=https://myiotservicestorage.blob.core.windows.net/;QueueEndpoint=https://myiotservicestorage.queue.core.windows.net/;TableEndpoint=https://myiotservicestorage.table.core.windows.net/;FileEndpoint=https://myiotservicestorage.file.core.windows.net/;"
container_name="raspberrypic"
blob_name="face_detect"
# Azure IotHub
CONNECTION_STRING = "HostName=MyIoTHubSample.azure-devices.net;DeviceId=MyRPi;SharedAccessKey=i598CK6++eTEyGf2zSo0zZvsKU8UMxiMjVtftlKJyR4="
# Create instance of the device client
iothub_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
PAYLOAD = '{{"No. of faces": {face_num}}}'
'''
END - Authenticate
'''

'''
Quickstart variables
These variables are shared by several examples
'''
# Images used for the examples: Describe an image, Categorize an image, Tag an image, 
# Detect faces, Detect adult or racy content, Detect the color scheme, 
# Detect domain-specific content, Detect image types, Detect objects
images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "images")
# <snippet_remoteimage>
remote_image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"
# </snippet_remoteimage>
'''
END - Quickstart variables
'''

async def CognitiveServiceApp():
    '''
    Describe an Image - local
    This example describes the contents of an local image with the confidence score.
    '''
    print("===== Describe an Image - local =====")
    # Open local image file
    local_image_path = os.path.join (images_folder, "faces.jpg")
    local_image = open(local_image_path, "rb")

    # Call API
    description_result = computervision_client.describe_image_in_stream(local_image)

    # Get the captions (descriptions) from the response, with confidence level
    print("Description of local image: ")
    if (len(description_result.captions) == 0):
        print("No description detected.")
    else:
        for caption in description_result.captions:
            print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
    print()
    '''
    END - Describe an Image - local
    '''

    # <snippet_describe>
    '''
    Describe an Image - remote
    This example describes the contents of a remote image with the confidence score.
    '''
    print("===== Describe an image - remote =====")
    # Call API
    description_results = computervision_client.describe_image(remote_image_url )

    # Get the captions (descriptions) from the response, with confidence level
    print("Description of remote image: ")
    if (len(description_results.captions) == 0):
        print("No description detected.")
    else:
        for caption in description_results.captions:
            print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
    # </snippet_describe>
    print()
    '''
    END - Describe an Image - remote
    '''

    # <snippet_describe>
    '''
    Describe an Image - camera
    This example describes the contents of an image taken by USB camera with the confidence score.
    '''
    print("===== Describe an image - camera =====")
    # capture the image with USB webcamera
    a=os.system("fswebcam --no-banner -r 1280x720 capture.jpg")
    print(a)
    # Open local image file
    local_image = open("capture.jpg", "rb")

    # Call API
    description_result = computervision_client.describe_image_in_stream(local_image)

    # Get the captions (descriptions) from the response, with confidence level
    print("Description of local image: ")
    if (len(description_result.captions) == 0):
        print("No description detected.")
    else:
        for caption in description_result.captions:
            print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
    print()
    '''
    END - Describe an Image - camera
    '''

    '''
    Detect Faces - local
    This example detects faces in a local image, gets their gender and age, 
    and marks them with a bounding box.
    '''
    print("===== Detect Faces - local =====")
    # Open local image
    local_image = open(local_image_path, "rb")
    # Select visual features(s) you want
    local_image_features = ["faces"]
    # Call API with local image and features
    detect_faces_results_local = computervision_client.analyze_image_in_stream(local_image, local_image_features)

    # Print results with confidence score
    print("Faces in the local image: ")
    if (len(detect_faces_results_local.faces) == 0):
        print("No faces detected.")
    else:
        for face in detect_faces_results_local.faces:
            print("'{}' of age {} at location {}, {}, {}, {}".format(face.gender, face.age, \
            face.face_rectangle.left, face.face_rectangle.top, \
            face.face_rectangle.left + face.face_rectangle.width, \
            face.face_rectangle.top + face.face_rectangle.height))
    print()
    '''
    END - Detect Faces - local
    '''

    # <snippet_faces>
    '''
    Detect Faces - remote
    This example detects faces in a remote image, gets their gender and age, 
    and marks them with a bounding box.
    '''
    print("===== Detect Faces - remote =====")
    # Get an image with faces
    remote_image_url_faces = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/faces.jpg"
    # Select the visual feature(s) you want.
    remote_image_features = ["faces"]
    # Call the API with remote URL and features
    detect_faces_results_remote = computervision_client.analyze_image(remote_image_url_faces, remote_image_features)

    # Print the results with gender, age, and bounding box
    print("Faces in the remote image: ")
    if (len(detect_faces_results_remote.faces) == 0):
        print("No faces detected.")
    else:
        for face in detect_faces_results_remote.faces:
            print("'{}' of age {} at location {}, {}, {}, {}".format(face.gender, face.age, \
            face.face_rectangle.left, face.face_rectangle.top, \
            face.face_rectangle.left + face.face_rectangle.width, \
            face.face_rectangle.top + face.face_rectangle.height))
    # </snippet_faces>
    print()
    '''
    END - Detect Faces - remote
    '''

    '''
    Detect Faces - camera
    This example detects faces in a camera-captured image, gets their gender and age, 
    and marks them with a bounding box.
    '''
    # capture the image with USB webcamera
    a=os.system("fswebcam --no-banner -r 1280x720 face.jpg")
    print(a)
    # Open local image file
    local_image = open("face.jpg", "rb")
    print("===== Detect Faces - camera =====")
    # Select visual features(s) you want
    local_image_features = ["faces"]
    # Call API with local image and features
    detect_faces_results_local = computervision_client.analyze_image_in_stream(local_image, local_image_features)

    #data formating
    data = PAYLOAD.format(face_num=len(detect_faces_results_local.faces))
    message = Message(data)
    # Send a message to the IoT hub
    print(f"Sending message: {message}")
    await iothub_client.send_message(message)
    print("Message successfully sent")
    
    # Print results with confidence score
    print("Faces in the local image: ")
    if (len(detect_faces_results_local.faces) == 0):
        print("No faces detected.")
    else:
        for face in detect_faces_results_local.faces:
            print("'{}' of age {} at location {}, {}, {}, {}".format(face.gender, face.age, \
            face.face_rectangle.left, face.face_rectangle.top, \
            face.face_rectangle.left + face.face_rectangle.width, \
            face.face_rectangle.top + face.face_rectangle.height))
            im = Image.open("face.jpg")
            draw = ImageDraw.Draw(im)
            draw.rectangle([face.face_rectangle.left, face.face_rectangle.top, \
                            face.face_rectangle.left + face.face_rectangle.width,\
                            face.face_rectangle.top + face.face_rectangle.height],outline='red',width=5)
            im.save("detect.jpg")
    de=Image.open("detect.jpg")
    plt.figure("Result")
    plt.imshow(de)
    plt.show()
    print()
     
    # upload the image to Azure Blob Storage, Overwrite if it already exists!
    blob = BlobClient.from_connection_string(conn_str, container_name, blob_name)
    image_content_setting = ContentSettings(content_type='image/jpeg')
    with open("detect.jpg", "rb") as data:
        blob.upload_blob(data,overwrite=True,content_settings=image_content_setting)
        print("Upload completed")

    '''
    END - Detect Faces - camera
    '''
    
if __name__ == '__main__':
    asyncio.run(CognitiveServiceApp())