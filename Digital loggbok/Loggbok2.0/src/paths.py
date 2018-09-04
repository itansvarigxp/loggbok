import os
_debug = True
# Allt som rör namn på filstrukturer är samlat här

# huvudmapp
os.chdir('..')
project_path  = os.getcwd()
# undermapp
src_path = project_path + "/src/"
res_path = project_path + "/res/"
reg_path = project_path + "/reg/"
stat_path = project_path + "/stat/"
#log_online_path = project_path + '/log/'
# Absolute paths for sharing

if _debug:
    log_online_path = project_path + '/debug/'
    mnt_loggbook_path = log_online_path
else:
    log_online_path = '/home/eXPerimentverkstaden/info/'
    mnt_loggbook_path = '/mnt/Digital Loggbok/'

print(mnt_loggbook_path)
# Absolut mapp
#webpage_resources_path = '/mnt/www/incheckade/'
webpage_resources_path = '/home/eXPerimentverkstaden/incheckade/'

# filnamn
file_name_bg = 'bg.gif'
file_name_logg_online = 'Loggbok_extern.xlsx'
file_name_member_register = 'Medlemsregister.xlsx'
file_name_new_member_register = 'Nyamedlemmar.xlsx'
# hela sökvägen
gui_bg = res_path + file_name_bg
xlsx_logg_online = log_online_path + file_name_logg_online
xlsx_member_register = mnt_loggbook_path + file_name_member_register
xlsx_new_members = mnt_loggbook_path + file_name_new_member_register

xlsx_statistics = mnt_loggbook_path + 'statistik/'

