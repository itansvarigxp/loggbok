
from datetime import datetime
import excel_handler as XlsxHandler

# Klass som innehåller allt som behövs för att logga medlemmar
class Member(object):
    # Klassvariabler som delas med alla objekt av typen Member
    # Incheckade medlemmar
    checked_in_members = {}
    checked_in_styret = {}
    # Aktivt medlemsregister
    member_register = {}

    # Konstruktor
    def __init__(self, key_card, name, board_member = False, latest_activity = None):
        self.key_card = key_card
        self.name = name
        self.board_member = board_member
        self.checkin_time = None
        self.latest_activity = latest_activity
        Member.member_register[key_card] = self

    # Sätter incheckningstiden och incheckningsdatum
    def setCheckInTime(self, time_object):
        self.checkin_time = time_object
        

    # Checkar in en medlem i klassvariabeln
    def checkIn(member):
        member.setCheckInTime(datetime.now())
        member.setLatestActivity()
        if (member.board_member):
            Member.checked_in_styret[member.key_card] = member
        else:
            Member.checked_in_members[member.key_card] = member

    # Returnerar namnet på en objektet som kallar funktionen
    def getName(self):
        return self.name

    # Returnerar om objektet är en styrelsemedlem eller ej
    def getBoardmember(self):
        return self.board_member

    # Returnerar tiden som objektet checkade in
    def getCheckedInTime(self):
        return self.checkin_time.strftime("%H:%M:%S")

    # Returnerar datumet som objektet checkade in
    def getCheckinDate(self):
        return self.checkin_time.strftime("%Y-%m-%d")

    def getCheckInTimeObject(self):
        return self.checkin_time

    def getKeyCardNumber(self):
        return self.key_card

    def getLatestActivity(self):
        return self.latest_activity

    def setLatestActivity(self):
        self.latest_activity = datetime.now().strftime("%Y-%m-%d")

    # Används vid byte av nyckelkort
    def changeKeyCard(self, new_key_card):
        del Member.member_register[self.key_card]
        self.key_card = new_key_card
        Member.member_register[self.key_card] = self

    # Clearar klassvariablerna checked_in_members och checked_in_styret
    def clearCheckedIn():
        Member.checked_in_members = {}
        Member.checked_in_styret = {}

    # Gör om en lång lista av incheckade namn till en lista av strings
    # med incheckade namn. Splittar listan efter split_at rader.
    # Returnerar en lista av strings med split at antal rader
    def toListStr(member_dict, split_at):
        list_of_names_tmp = []
        list_of_names = []
        for member in member_dict:
           list_of_names_tmp.append(member_dict[member].getName())
        nbr_of_elems = len(list_of_names_tmp) // split_at
        for idx in range(0, nbr_of_elems+1):
            list_of_names.append('\n'.join(list_of_names_tmp[idx*split_at:((idx+1)*split_at)]))
        return list_of_names

    # Gör om incheckade medlemmar till en lista av strings
    def checkedInMembersToStr(split_at):
        return Member.toListStr(Member.checked_in_members, split_at-1)

    # Gör om incheckade styret till en lista av strings
    def checkedInStyretToStr(split_at):
        return Member.toListStr(Member.checked_in_styret, split_at-1)

    # Checkar ut en medlem om den är incheckad och returnerar dess namn
    # om medlemmen inte finns i incheckade så returnerar den None
    def checkOut(key_card):
        if key_card in Member.checked_in_members:
            member = Member.checked_in_members[key_card]
            del Member.checked_in_members[key_card]
        elif key_card in Member.checked_in_styret:
            member = Member.checked_in_styret[key_card]
            del Member.checked_in_styret[key_card]
        else:
            return None
        return member

    def nbrCheckedInMembersNow():
        return len(Member.checked_in_members)

    def nbrCheckedInStyretNow():
        return len(Member.checked_in_styret)

    def nbrCheckedInNow():
        return (Member.nbrCheckedInStyretNow() + Member.nbrCheckedInMembersNow())

