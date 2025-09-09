import cv2
import easyocr


def read_text(reader, frame):
    '''
    Uses cv2 to read all of the text on the ticket
    and sends all of the text to be parsed by a TicketHolder object
    '''
    results = reader.readtext(frame)
    possible_text = []
    for (bbox, text, prob) in results:
        (top_left, top_right, bottom_right, bottom_left) = bbox
        
        if prob > 0.6:
            possible_text.append(text)
            cv2.rectangle(frame, 
                      (int(top_left[0]), int(top_left[1])), 
                      (int(bottom_right[0]), int(bottom_right[1])), 
                      (0, 255, 0), 2)
            cv2.putText(frame, text, (
                        int(top_left[0]), int(top_left[1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
   
    return possible_text