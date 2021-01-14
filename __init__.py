import os
from flask import Flask, render_template, redirect, url_for
from forms import UploadForm
from utils import *
import sudukoSolver
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
app = Flask(__name__)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route("/", methods=['GET', 'POST'])
def index():
    form = UploadForm()
    
    if form.validate_on_submit():
        pathImage = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/jj')
        
        heightImg = 450
        widthImg = 450
        model = intializePredectionModel()
        img = cv2.imread('uploads/jj')
        img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
        imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
        imgThreshold = preProcess(img)

        # #### 2. FIND ALL COUNTOURS
        imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3) # DRAW ALL DETECTED CONTOURS

        #### 3. FIND THE BIGGEST COUNTOUR AND USE IT AS SUDOKU
        biggest, maxArea = biggestContour(contours) # FIND THE BIGGEST CONTOUR
        print(biggest)
        if biggest.size != 0:
            biggest = reorder(biggest)
            print(biggest)
            cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25) # DRAW THE BIGGEST CONTOUR
            pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2) # GER
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
            imgDetectedDigits = imgBlank.copy()
            imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)

            #### 4. SPLIT THE IMAGE AND FIND EACH DIGIT AVAILABLE
            imgSolvedDigits = imgBlank.copy()
            boxes = splitBoxes(imgWarpColored)
            print(len(boxes))
            # cv2.imshow("Sample",boxes[65])
            numbers = getPredection(boxes, model)
            print(numbers)
            imgDetectedDigits = displayNumbers(imgDetectedDigits, numbers, color=(255, 0, 255))
            numbers = np.asarray(numbers)
            posArray = np.where(numbers > 0, 0, 1)
            print(posArray)


            #### 5. FIND SOLUTION OF THE BOARD
            board = np.array_split(numbers,9)
            
            sudukoSolver.solve(board)
            print("here",board)
            return render_template('sud.html', list=board)
            # except:
            #     print("No Sudoku Found")

        
            

            #     return redirect(url_for('index'))
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run()