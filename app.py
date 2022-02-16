import os
import sys

root= os.path.dirname(__file__)
sys.path.append(root+"/pyimagesearch")


from pyimagesearch.anpr import PyImageSearchANPR
from imutils import paths
import argparse
import imutils
import cv2
from flask import Flask, render_template,request, send_from_directory
from werkzeug.utils import secure_filename


def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text ] ).strip()

# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--input", required=True, help="path to input directory of images")
# ap.add_argument("-c", "--clear-border", type=int, default=-1, help="whether or to clear border pixels before OCR'ng")
# ap.add_argument("-p", "--psm", type=int, default=7, help="default PSM mode for OCRing license plates")
# ap.add_argument("-d", "--debug", type=int, default=-1, help="whether or not to show additional visualizations")
# args=vars(ap.parse_args())

# initialize our ANPR class
anpr = PyImageSearchANPR(3,5)
# imagePaths = sorted(list(paths.list_images(args["input"])))
# loop over all image paths in the input directory


UPLOAD_FOLDER = root+"/uploads"

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/predict", methods=['POST','GET'])
def predict():
    if request.method  == 'POST':
        file=request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # perform ocr
            image=cv2.imread(app.config['UPLOAD_FOLDER']+"\\"+filename)
            image=imutils.resize(image, width=600)
            (lpText, lpCnt) = anpr.find_and_ocr(image )
            if lpText is not None and lpCnt is not None:
                return render_template('result.html',prediction_text=lpText)
            else:
                return render_template('result.html',prediction_text="Could not identify")
        return render_template('result.html', prediction_text="file received but not cvd")


    