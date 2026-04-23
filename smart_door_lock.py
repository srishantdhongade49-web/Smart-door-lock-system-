import cv2
import time
import RFID
import servo_control
import lcd_display

def main():
    # Initialize face recognition
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    # Initialize RFID reader
    rfid_reader = RFID.Reader()

    # Initialize servo motor
    servo = servo_control.Servo()

    # Initialize LCD display
    lcd = lcd_display.LCD()

    while True:
        # Capture video from webcam
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Display the resulting frame
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Check RFID
            rfid_code = rfid_reader.scan()
            if rfid_code:
                lcd.display("Access Granted")
                servo.unlock()
                time.sleep(5)  # locked for 5 seconds
                servo.lock()
            else:
                lcd.display("Access Denied")

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()