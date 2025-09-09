import easyocr
import cv2
import frame_proc
from ticket_holder import TicketHolder


def line(frame):
    height, width, _ = frame.shape
    center_y = height // 2
    cv2.line(frame, (0, center_y), (width, center_y), (0, 0, 0), 2)


def main():
    reader = easyocr.Reader(["en"], gpu=True)

    cap = cv2.VideoCapture(0)
    # 1 means that auto focus is enabled
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600) 
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 896)  
    #C:\Users\User\Downloads\Book-1_Sheet1_.xlsx
    ticket = TicketHolder("C:/Users/User/Downloads/Book-1_Sheet1_.xlsx")
    while True:

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        ret, frame = cap.read()

        if not ret:
            break

        if cv2.waitKey(1) & 0xFF == ord("g"):
            possible_text = frame_proc.read_text(reader, frame)
            ticket.process_text(possible_text)

        ticket.place_info(frame)
        line(frame)
        cv2.imshow("Image", frame)
        
        if cv2.waitKey(1) & 0xFF == ord(" "):
            ticket.add_to_worksheet()
     
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
