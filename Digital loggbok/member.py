
import datetime, excel_handler

class Member(object):
    checked_in_members = {}
    checked_in_styret = {}
    member_register = {}
    """docstring for Member"""
    def __init__(self, key_card, name, board_member = False):
        self.key_card = key_card
        self.name = name
        self.board_member = board_member
        self.checkin_time = None
        self.checkin_date = None
        global member_register
        self.member_register[key_card] = self

    def setCheckInTime(self, time_object):
        self.checkin_time = time_object.strftime("%H:%M:%S")
        self.checkin_date = time_object.strftime("%Y-%m-%d")

    def checkIn(member):
        member.setCheckInTime(datetime.datetime.now())
        if (member.board_member):
            global checked_in_styret
            Member.checked_in_styret[member.key_card] = member
        else:
            global checked_in_members
            Member.checked_in_members[member.key_card] = member

    def getName(self):
        return self.name

    def getBoardmember(self):
        return self.board_member

    def getCheckedInTime(self):
        return self.checkin_time

    def getCheckinDate(self):
        return self.checkin_date

    def clearCheckedIn():
        global checked_in_members
        global checked_in_styret
        checked_in_members = {}
        checked_in_styret = {}

    def toListStr(member_dict, split_at):
        list_of_names_tmp = []
        list_of_names = []
        for member in member_dict:
           list_of_names_tmp.append(member_dict[member].getName())
        nbr_of_elems = len(list_of_names_tmp) // split_at
        for idx in range(0, nbr_of_elems+1):
            list_of_names.append('\n'.join(list_of_names_tmp[idx*split_at:((idx+1)*split_at)-1]))
        return list_of_names

    def checkedInMembersToStr(split_at):
        return Member.toListStr(Member.checked_in_members, split_at)

    def checkedInStyretToStr(split_at):
        return Member.toListStr(Member.checked_in_styret, split_at)

    def checkOut(key_card):
        global checked_in_members
        global checked_in_styret
        if key_card in Member.checked_in_members:
            member = Member.checked_in_members[key_card]
            del Member.checked_in_members[key_card]
        elif key_card in Member.checked_in_styret:
            member = Member.checked_in_styret[key_card]
            del Member.checked_in_styret[key_card]
        else:
            return None
        excel_handler.XlsxHandler.save_to_logg(member)
        return member.getName()

