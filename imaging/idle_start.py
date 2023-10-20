def idle_start(cam, net):
    print("IDLE START")
    # Wait for bull detection
    counter = 0
    while True:
        img = cam.Capture()

        if img is None:
            continue

        detections = net.Detect(img)

        for detection in detections:
            if detection.ClassID == 1:  # Bull
                x = detection.Center[0]
                y = detection.Center[1]
                return x, y

# EOF
