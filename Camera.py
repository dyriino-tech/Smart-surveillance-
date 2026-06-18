import cv2
import datetime
import os

save_folder = "captures"
os.makedirs(save_folder, exist_ok=True)

cap = cv2.VideoCapture(0)
ret, prev = cap.read()
prev = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
prev = cv2.GaussianBlur(prev, (21, 21), 0)
counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    delta = cv2.absdiff(prev, gray)
    thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    motion = False
    for c in contours:
        if cv2.contourArea(c) < 500:
            continue
        motion = True
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    if motion:
        counter += 1
        if counter % 10 == 0:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = save_folder + "/capture_" + timestamp + ".jpg"
            result = cv2.imwrite(filename, frame)
            print("Saved: " + filename + " Result: " + str(result))
    else:
        counter = 0
    status = 'MOTION DETECTED - SAVING!' if motion else 'Monitoring...'
    color = (0, 0, 255) if motion else (0, 255, 0)
    cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow('Smart Surveillance', frame)
    prev = gray
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
