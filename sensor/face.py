import face_recognition, cv2, threading, time, os

def detect_face(img):
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(img, (0, 0), fx=0.125, fy=0.125)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)

        return face_locations

def generate(cam):

    global outputFrame, lock

    lock = threading.Lock()

    process_this_frame = True

    while True:
        global frame
        frame = cam.read()

        face_locations = detect_face(frame)

        global top, right, bottom, left

        if face_locations:
            top, right, bottom, left = face_locations[0]

        # Display the results
        for (top, right, bottom, left) in face_locations:
            print(top, right, bottom, left)
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 8
            right *= 8
            bottom *= 8
            left *= 8

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
            if frame is None:
                continue
			# encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

    cam.release()

def capture_image(name, cpf):
        
        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # SPACE pressed
        timestamp = time.time()
        directory = os.getcwd()+'/media'

        img_name = f'{directory}/{name}-{cpf}-{int(timestamp)}.jpg'
        img_name_2 = f'{directory}/{name}-{cpf}-gray-{int(timestamp)}.jpg'

        face = grayImage[top:bottom, left: right]

        cv2.imwrite(img_name, frame)
        cv2.imwrite(img_name_2, cv2.resize(face,(80,60)))

        print("{} written!".format(img_name))