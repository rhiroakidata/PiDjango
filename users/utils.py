def capture_image(nome, id):
    count = 1
    n_count = 30

    cam = cv2.VideoCapture(0 + cv2.CAP_V4L2)

    cv2.namedWindow("Diga X")

    face_locations = []
    process_this_frame = True

    while True:
        if count<=n_count:
            ret, frame = cam.read()


            imagemCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #imagemCinza = cv2.resize(imagemCinza, (0, 0), fx=0.25, fy=0.25)

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.125, fy=0.125)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left) in face_locations:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 8
                right *= 8
                bottom *= 8
                left *= 8

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Display the resulting image
            cv2.imshow('Diga X', frame)

            if not ret:
                break
            k = cv2.waitKey(1)

            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break

            elif k % 256 == 32:
                # SPACE pressed
                cv2.destroyAllWindows()
                timestamp = time.time()
                directory = os.getcwd()+'/dataset'

                directory2 = os.getcwd() + '/photos'

                img_name = f'{directory}/{nome}-{id}-{int(timestamp)}-{count}.jpg'
                img_name_1 = f'{directory2}/{nome}-{id}-{int(timestamp)}-{count}.jpg'

                face = imagemCinza[top:bottom, left: right]

                cv2.imwrite(img_name, frame)
                cv2.imwrite(img_name_1, cv2.resize(face,(80,60)))

                #print("{} written!".format(img_name))
                count += 1
        else:
            break

    cam.release()


    cv2.destroyAllWindows()