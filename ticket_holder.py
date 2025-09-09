from openpyxl import Workbook, load_workbook
import cv2


class TicketHolder:
    '''
    Processes and stores the information that is found on the ticket
    Stores the tickets first initial, last name, and phone number on a string
    Also stores the workbook/microsoft edge file path to then add all 
    necesarry information to the file.
    '''
    def __init__(self, workbook_path):
        '''
        Initializes a new TicketHolder object
        Takes the path of the workbook to store the information
        '''
        self.first_initial = ""
        self.last_name = ""
        self.phone_number = ""
        self.workbooth_path = workbook_path
        self.wb = load_workbook(workbook_path)
        self.ws = self.wb.active

    def process_text(self, possible_text):
        '''
        Takes all of the text on the scanned ticket
        and tries parsing through it to find the necesarry
        information
        '''
        for text in possible_text:
            if "customer:" in text.lower() or "customer" in text.lower():
                try:
                    name = text[9: len(text)]
                    name = name.strip()
                    self.first_initial = name[0]
                    self.last_name = name[name.index(" ") + 1: len(text)]
                except:
                    pass
            # Since I know it's not their name I can put it in lower case
            # Makes conditional statements cleaner
            text = text.lower()
            if "mobile:" in text or "mobile" in text or "home:" in text or "home" in text or "work" in text or "work:" in text:
                self.phone_number = ""
                for char in text:
                    if ord(char) - 48 >= 0 and ord(char) - 48 <= 9:
                        self.phone_number += str(char)
         
    def place_info(self, frame):
        '''
        Places the found information onto the frame/video
        Allowing the user to see what information has been scanned
        '''
        cv2.putText(frame, self.last_name, (40, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, self.first_initial, (1500, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, self.phone_number, (750, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
 
    def add_to_worksheet(self):
        '''
        Adds all information to the worksheet into respective columns
        '''
        if self.first_initial != "" and self.last_name != "" and self.phone_number != "":
            self.ws.append([self.phone_number, self.first_initial, self.last_name])
            self.first_initial = ""
            self.last_name = ""
            self.phone_number = ""
            self.wb.save(self.workbooth_path)