import cv2

def cartoonize_video(input_file_path, output_file_path):
    # 비디오 파일 열기
    cap = cv2.VideoCapture(input_file_path)

    # 비디오 코덱 및 프레임 정보 가져오기
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 비디오 출력 설정
    out = cv2.VideoWriter(output_file_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # 만화적인 효과를 적용하기 위한 전처리
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

        # 비디오에 만화적인 효과 적용
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)

        # 출력 프레임 저장
        out.write(cartoon)

        # 화면에 출력
        cv2.imshow('Cartoonized Video', cartoon)
        
        # 'q' 키를 누르거나 창을 닫으면 비디오 종료
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Cartoonized Video', cv2.WND_PROP_VISIBLE) < 1:
            break

    # 자원 해제
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    input_file_path = input("비디오 파일 경로를 입력하세요: ")
    output_file_path = 'cartoonized_output_video.mp4'  # 출력 비디오 파일명
    cartoonize_video(input_file_path, output_file_path)