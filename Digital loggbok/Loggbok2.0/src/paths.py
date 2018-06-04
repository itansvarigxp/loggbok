import os

# Allt som rör namn på filstrukturer är samlat här

# huvudmapp
os.chdir('..')
project_path  = os.getcwd()
# undermapp
src_path = project_path + "/src/"
res_path = project_path + "/res/"
reg_path = project_path + "/reg/"
stat_path = project_path + "/stat/"
log_online_path = project_path + '/log/'
# Absolut mapp
#webpage_resources_path = '/mnt/www/incheckade/'
webpage_resources_path = ''

# filnamn
file_name_bg = 'bg.gif'
file_name_logg_online = 'Loggbok_online.xlsx'
file_name_member_register = 'Medlemsregister.xlsx'
file_name_new_member_register = 'Nyamedlemmar.xlsx'
# hela sökvägen
gui_bg = res_path + file_name_bg
xlsx_logg_online = log_online_path + file_name_logg_online
xlsx_member_register = reg_path + file_name_member_register
xlsx_new_members = reg_path + file_name_new_member_register

xlsx_statistics = stat_path
