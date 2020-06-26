from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.VideoDAO import VideoDAO
from project.com.vo.VideoVO import VideoVO
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime
from flask import render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename

import cv2
import dlib
import imutils
import numpy as np
from imutils.video import FPS
from imutils.video import VideoStream

from project.com.controller.centroidtracker import CentroidTracker

compare = []
Dangerlist = []
Cautionlist = []
Safelist = []

UPLOAD_INPUTVIDEO_FOLDER = 'project/static/userResource/input/'
app.config['UPLOAD_INPUTVIDEO_FOLDER'] = UPLOAD_INPUTVIDEO_FOLDER

UPLOAD_OUTPUTVIDEO_FOLDER = 'project/static/userResource/output/'
app.config['UPLOAD_OUTPUTVIDEO_FOLDER'] = UPLOAD_OUTPUTVIDEO_FOLDER


@app.route( '/user/loadVideo', methods=['GET'] )
def userLoadVideo():
    try:
        if adminLoginSession() == 'user':
            return render_template( 'user/addVideo.html' )
        else:
            return adminLogoutSession()
    except Exception as ex:
        print( ex )


@app.route( '/user/insertVideo', methods=['POST'] )
def userInsertVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()
            videoDAO = VideoDAO()

            file = request.files['file']

            videoInputFileName = secure_filename( file.filename )
            videoInputFilePath = os.path.join( app.config['UPLOAD_INPUTVIDEO_FOLDER'] )

            file.save( os.path.join( videoInputFilePath, videoInputFileName ) )

            inputVideo = videoInputFilePath + videoInputFileName
            videoOutputFileName = videoInputFileName.replace( '.mp4', '.webm' )
            videoOutputFilePath = os.path.join( app.config['UPLOAD_OUTPUTVIDEO_FOLDER'] )

            outputVideo = videoOutputFilePath + videoOutputFileName

            confidence_default = 0.4
            skip_frames = 25

            s1 = 'project/static/userResource/modelDump/MobileNetSSD_deploy.prototxt'
            model = 'project/static/userResource/modelDump/MobileNetSSD_deploy.caffemodel'

            userName = session['session_loginUsername']

            print( "userName=", userName )

            # initialize the list of class labels MobileNet SSD was trained to
            # detect
            CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                       "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                       "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                       "sofa", "train", "tvmonitor"]

            # load our serialized model from disk
            print( "[INFO] loading model..." )
            net = cv2.dnn.readNetFromCaffe( s1, model )
            # print(">>>>>>>>>>>>>>>>>>>>>>>loding")

            # if a video path was not supplied, grab a reference to the webcam
            if not inputVideo:
                print( "[INFO] starting video stream..." )
                vs = VideoStream( src=0 ).start()
                time.sleep( 2.0 )

            # otherwise, grab a reference to the video file
            else:
                print( "[INFO] opening video file..." )
                vs = cv2.VideoCapture( inputVideo )

            # initialize the video writer (we'll instantiate later if need be)
            writer = None

            # initialize the frame dimensions (we'll set them as soon as we read
            # the first frame from the video)
            W = None
            H = None

            # instantiate our centroid tracker, then initialize a list to store
            # each of our dlib correlation trackers, followed by a dictionary to
            # map each unique object ID to a TrackableObject
            ct = CentroidTracker( maxDisappeared=40, maxDistance=50 )
            trackers = []
            trackableObjects = {}

            # initialize the total number of frames processed thus far, along
            # with the total number of objects that have moved either up or down
            totalFrames = 0
            miny = 0
            # start the frames per second throughput estimator
            fps = FPS().start()

            # loop over frames from the video stream
            while True:
                # grab the next frame and handle if we are reading from either
                # VideoCapture or VideoStream
                frame = vs.read()
                frame = frame[1] if (inputVideo != False) else frame

                # if we are viewing a video and we did not grab a frame then we
                # have reached the end of the video
                if inputVideo is not None and frame is None:
                    break

                # resize the frame to have a maximum width of 500 pixels (the
                # less data we have, the faster we can process it), then convert
                # the frame from BGR to RGB for dlib
                frame = imutils.resize( frame, width=500 )
                rgb = cv2.cvtColor( frame, cv2.COLOR_BGR2RGB )

                # if the frame dimensions are empty, set them
                if W is None or H is None:
                    (H, W) = frame.shape[:2]

                # if we are supposed to be writing a video to disk, initialize
                # the writer
                if outputVideo is not None and writer is None:
                    fourcc = cv2.VideoWriter_fourcc( *"VP80" )
                    writer = cv2.VideoWriter( outputVideo, fourcc, 30, (W, H), True )

                # initialize the current status along with our list of bounding
                # box rectangles returned by either (1) our object detector or
                # (2) the correlation trackers
                status = "Waiting"
                rects = []

                # check to see if we should run a more computationally expensive
                # object detection method to aid our tracker
                if totalFrames % skip_frames == 0:
                    # set the status and initialize our new set of object trackers
                    status = "Detecting"
                    trackers = []
                    print( "detectiong" )

                    # convert the frame to a blob and pass the blob through the
                    # network and obtain the detections
                    blob = cv2.dnn.blobFromImage( frame, 0.007843, (W, H), 127.5 )
                    net.setInput( blob )
                    detections = net.forward()

                    # loop over the detections
                    for i in np.arange( 0, detections.shape[2] ):
                        # extract the confidence (i.e., probability) associated
                        # with the prediction
                        confidence = detections[0, 0, i, 2]
                        # print("in detectioooon for loop")

                        # filter out weak detections by requiring a minimum
                        # confidence
                        if confidence > confidence_default:
                            # extract the index of the class label from the
                            # detections list
                            idx = int( detections[0, 0, i, 1] )

                            # if the class label is not a person, ignore it
                            if CLASSES[idx] != "person":
                                print( "detect person" )
                                continue

                            # compute the (x, y)-coordinates of the bounding box
                            # for the object
                            box = detections[0, 0, i, 3:7] * np.array( [W, H, W, H] )
                            (startX, startY, endX, endY) = box.astype( "int" )

                            # construct a dlib rectangle object from the bounding
                            # box coordinates and then start the dlib correlation
                            # tracker
                            tracker = dlib.correlation_tracker()

                            compare.append( (startX, startY) )
                            for i in compare:
                                if miny < i[1]:
                                    miny = i[1]
                            # add the tracker to our list of trackers so we can
                            # utilize it during skip frames
                            rect = dlib.rectangle( int( startX ), int( miny ), int( endX ), int( endY ) )
                            tracker.start_track( rgb, rect )
                            trackers.append( tracker )


                # otherwise, we should utilize our object *trackers* rather than
                # object *detectors* to obtain a higher frame processing throughput
                else:
                    miny = 0
                    # loop over the trackers
                    for tracker in trackers:
                        # set the status of our system to be 'tracking' rather
                        # than 'waiting' or 'detecting'
                        status = "Tracking"

                        # update the tracker and grab the updated position
                        tracker.update( rgb )
                        pos = tracker.get_position()

                        # unpack the position object
                        startX = int( pos.left() )
                        startY = int( pos.top() )
                        endX = int( pos.right() )
                        endY = int( pos.bottom() )

                        # add the bounding box coordinates to the rectangles list

                        compare.append( (startX, startY) )
                        for i in compare:
                            if miny < i[1]:
                                miny = i[1]

                        rects.append( (startX, miny, endX, endY) )

                        cv2.rectangle( frame, (startX, miny), (endX, endY), 2 )

                # draw a horizontal line in the center of the frame -- once an
                # object crosses this line we will determine whether they were
                # moving 'up' or 'down'
                cv2.line( frame, (int( W // 1.5 ), 0), (int( W // 1.5 ), H), (0, 255, 255), 2 )
                cv2.line( frame, (int( W // 2 ), 0), (int( W // 2 ), H), (255, 0, 0), 2 )
                cv2.line( frame, (0, int( H // 5 )), (W, int( H // 5 )), (255, 0, 255), 2 )
                # use the centroid tracker to associate the (1) old object
                # centroids with (2) the newly computed object centroids
                objects = ct.update( rects )
                caution = 0
                danger = 0
                safe = 0
                for i in rects:

                    if i[1] < H // 5:
                        continue

                    if W // 3 > i[0] > W // 3:
                        caution += 1
                        Cautionlist.append( caution )
                    elif i[0] > W // 3:
                        safe += 1
                        Safelist.append( safe )
                    elif i[0] < W // 3:
                        danger += 1
                        Dangerlist.append( danger )

                # loop over the tracked objects
                for (objectID, centroid) in objects.items():
                    # check to see if a trackable object exists for the current
                    # object ID
                    to = trackableObjects.get( objectID, None )

                    trackableObjects[objectID] = to

                    # draw both the ID of the object and the centroid of the
                    # object on the outputVideo frame
                    text = "ID {}".format( objectID )
                    if len( rects ) == 0:
                        continue

                    cv2.putText( frame, text, (rects[len( rects ) - 1][0] - 10, rects[len( rects ) - 1][1] - 10),
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2 )
                    cv2.circle( frame, (rects[len( rects ) - 1][0], rects[len( rects ) - 1][1]), 4, (0, 255, 0), -1 )

                # construct a tuple of information we will be displaying on the
                # frame
                info = [

                    ("Danger", danger),
                    ("Caution", caution),
                    ("Safe", safe),
                    ("Status", status),
                ]

                for (i, (k, v)) in enumerate( info ):
                    text = "{}: {}".format( k, v )
                    cv2.putText( frame, text, (10, H - ((i * 20) + 20)),
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2 )
                # check to see if we should write the frame to disk
                if writer is not None:
                    writer.write( frame )

                cv2.imshow( "Frame", frame )
                key = cv2.waitKey( 1 ) & 0xFF

                if key == ord( "q" ):
                    break

                totalFrames += 1

                fps.update()

                if len( Dangerlist ) == 2:
                    # song = AudioSegment.from_wav("1.wav")
                    # start = time.time()  # the variable that holds the starting time
                    # elapsed = 0  # the variable that holds the number of seconds elapsed.
                    # while elapsed < 10:  # while less than 30 seconds have elapsed
                    #     play(song)
                    #
                    #     elapsed = time.time() - start

                    message = "______DANGER_______Child has touch the grill."
                    fromaddr = "spotteractivity@gmail.com"
                    toaddr = userName
                    msg = MIMEMultipart()
                    msg['From'] = fromaddr
                    msg['To'] = toaddr
                    msg['Subject'] = "Child Security"
                    msg.attach( MIMEText( message, 'plain' ) )
                    server = smtplib.SMTP( 'smtp.gmail.com', 587 )
                    server.starttls()
                    server.login( fromaddr, "9925646618" )
                    text = msg.as_string()
                    server.sendmail( fromaddr, toaddr, text )
                    server.quit()

            print( "frame by camera", totalFrames )
            fps.stop()

            if writer is not None:
                writer.release()

            if not inputVideo:
                vs.stop()

            else:
                vs.release()

            cv2.destroyAllWindows()

            videoUploadDate = str( datetime.now().date() )
            videoUploadTime = datetime.now().strftime( '%H:%M:%S' )

            videoVO.videoUploadDate = videoUploadDate
            videoVO.videoUploadTime = videoUploadTime
            videoVO.videoInputFileName = videoInputFileName
            videoVO.videoInputFilePath = videoInputFilePath.replace( 'project', '..' )
            videoVO.videoOutputFileName = videoOutputFileName
            videoVO.videoOutputFilePath = videoOutputFilePath.replace( 'project', '..' )
            videoVO.video_LoginId = session['session_loginId']
            videoDAO.insertVideo( videoVO )

            return redirect( url_for( 'userViewVideo' ) )
        else:
            return adminLogoutSession()
    except Exception as ex:
        print( ex )


@app.route( '/user/viewVideo', methods=['GET'] )
def userViewVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()
            videoDAO = VideoDAO()

            videoVO.video_LoginId = session['session_loginId']
            videoVOList = videoDAO.viewVideo( videoVO )
            return render_template( 'user/viewVideo.html', videoVOList=videoVOList )
        else:
            return adminLogoutSession()
    except Exception as ex:
        print( ex )


@app.route( '/user/deleteVideo', methods=['GET'] )
def userDeleteVideo():
    try:
        if adminLoginSession() == 'user':
            videoVO = VideoVO()
            videoDAO = VideoDAO()
            videoId = request.args.get( 'videoId' )

            videoVO.videoId = videoId
            videoVOList = videoDAO.deleteVideo( videoVO )

            videoInputFileName = videoVOList.videoInputFileName
            videoInputFilePath = videoVOList.videoInputFilePath

            videoOutputFileName = videoVOList.videoOutputFileName
            videoOutputFilePath = videoVOList.videoOutputFilePath

            if videoInputFileName is not None:
                path = videoInputFilePath.replace( '..', 'project' ) + videoInputFileName
                os.remove( path )

            if videoOutputFileName is not None:
                path = videoOutputFilePath.replace( '..', 'project' ) + videoOutputFileName
                os.remove( path )

            return redirect( url_for( 'userViewVideo' ) )
        else:
            return adminLogoutSession()
    except Exception as ex:
        print( ex )


@app.route( '/admin/viewVideo', methods=['GET'] )
def adminViewVideo():
    try:
        if adminLoginSession() == 'admin':
            videoDAO = VideoDAO()

            videoVOList = videoDAO.adinViewVideo()
            print( 'videoVOList>>>', videoVOList )

            return render_template( 'admin/viewVideo.html', videoVOList=videoVOList )
        else:
            return adminLogoutSession()
    except Exception as ex:
        print( ex )
