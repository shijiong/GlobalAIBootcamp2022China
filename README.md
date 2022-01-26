# Global AI Bootcamp 2022 China
Demo project for Global AI Bootcamp 2022 China. Microsoft Cognitive Services and Azure IotHub Quickstart for Raspberry Pi 4.  
Uses local and remote images in each example.  
# Prerequisites:  
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

# Run the entire file to demonstrate the following examples:  
    - Describe Image - local  
    - Describe Image - remote  
    - Describe Image - camera  
    - Detect Faces - local  
    - Detect Faces - remote  
    - Detect Faces - camera  
    
# References:  
    - SDK: https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-vision-computervision/azure.cognitiveservices.vision.computervision?view=azure-python  
    - Documentaion: https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/index  
    - API: https://westus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-2/operations/5d986960601faab4bf452005  
