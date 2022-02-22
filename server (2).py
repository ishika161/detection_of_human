from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/',methods = ['POST'])
def open():
    import boto3
    aws_mng_con=boto3.session.Session(profile_name='user1')
    s3 = aws_mng_con.client('s3')

    import cv2
    videoCaptureObject = cv2.VideoCapture(0)
    result = True
    while(result):
      ret,frame = videoCaptureObject.read()
      cv2.imwrite("NewPicture1.jpg",frame)
      s3.upload_file("NewPicture1.jpg","2311s","myPhoto1.jpg")
      cv2.waitKey(4)
      cv2.imwrite("NewPicture2.jpg",frame)
      s3.upload_file("NewPicture1.jpg","2311s","myPhoto2.jpg")
      cv2.waitKey(4)
      cv2.imwrite("NewPicture3.jpg",frame)
      s3.upload_file("NewPicture1.jpg","2311s","myPhoto3.jpg")
      cv2.waitKey(4)
      cv2.imwrite("NewPicture4.jpg",frame)
      s3.upload_file("NewPicture1.jpg","2311s","myPhoto4.jpg")
      result = False
    videoCaptureObject.release()
    cv2.destroyAllWindows()


    import boto3
    import pyttsx3
    k=["myPhoto1.jpg","myPhoto2.jpg","myPhoto3.jpg","myPhoto4.jpg"]
    for i in range(4):
        bucket = "2311s"
        key = k[i]
        rekognition = boto3.client("rekognition")
        s3=boto3.client("s3")
        response = rekognition.detect_labels(Image={
          "S3Object": {
            "Bucket": bucket,
            "Name": key,
          }
        },
        MaxLabels=3,
        MinConfidence=90,
      )
        for i in response['Labels'][:]:
            if((i['Name']=="Person" or i['Name']=="Head") and i['Confidence']> 90):
                print("Human Detected")
                engine = pyttsx3.init()
                engine.say("Alert! Human detected")
                engine.runAndWait()
               #added line
                return render_template('alert.html')

    return 'Working'

if __name__ == '__main__':
  app.run(debug=True)