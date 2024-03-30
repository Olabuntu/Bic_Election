import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from streamlit import session_state
import time as t    
from streamlit_option_menu import option_menu
from gspread import Cell
import requests


st.set_page_config(page_title='BIOCHEMISTRY',
                    page_icon='🧬',
                    
                        initial_sidebar_state='auto')
       

def check_duplicate_vote(matric_no):
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_key('116wtaWh0Emg_XPIaZ7XQBfU4Bup5EkkF1_JWY3dU030')
    sheet = sh.worksheet('VOTE')
    cell = sheet.find(matric_no, in_column=1)
    if cell:
        return True
    else:
        return False
    

def check_user_login(username, password):

    valid_credentials = {'235052': '6953','235054': '4191','235033': '3382','237735': '5422','237734': '4781','237732': '2612','235024': '3644','235027': '2112','235057': '2858','235058': '9712','237731': '2517','235050': '4633','235032': '1457','235040': '8468','237729': '7617','237368': '3911','237371': '4496','235045': '6858','229139': '4419','235038': '1357','235042': '1937','238064': '2935','237736': '4658','237728': '5955','235041': '9821','235044': '2677','235047': '9826','235035': '1415','235043': '6812','235048': '2956','235037': '7881','237370': '7945','235022': '2725','238069': '8378','235060': '1977','235026': '1939','235036': '5446','235034': '3791','235023': '8818','235062': '3881','221934': '5651','238138': '6324','238248': '1372','237730': '6582','237981': '8568','235059': '2227','235020': '2369','237982': '7681','235028': '6296','235039': '9551','235051': '8558','235029': '2915','235021': '3624','235030': '9532','237369': '3612','237367': '4986','229101': '1836','229107': '6451','229111': '9583','229129': '1851','229156': '3176','229154': '1447','229163': '9856','229128': '6656','229089': '1212','229134': '4422','229149': '4622','229116': '9365','229091': '4997','232158': '8571','229162': '8883','229155': '1785','220023': '7121','229118': '4379','229143': '1851','229127': '2343','229148': '2173','229132': '3636','229137': '7167','229147': '4542','229094': '2884','229093': '2293','229141': '7737','229152': '8637','229150': '2911','230476': '9697','229126': '1659','229092': '3636','229138': '2574','229099': '2572','229131': '5792','229146': '6198','220630': '2545','220582': '5389','220608': '5477','220602': '4699','220601': '2248','220580': '3625','220583': '6478','220632': '7971','220592': '5741','220591': '7288','220620': '8856','220629': '2676','220604': '3182','220610': '9743','220622': '4135','220626': '8611','220618': '9765','220623': '8413','220576': '4581','220600': '4435','220650': '1188','220577': '4375','220649': '8577','220611': '8839','220624': '7186','220640': '3832','220634': '2978','220595': '7777','224039': '4211','223986': '2433','220612': '2287','220647': '8277','220578': '4445','220593': '7533','220587': '3314','220651': '1932','220590': '9853','220581': '7871','220615': '6927','220616': '3737','223728': '3536','220584': '4149','220625': '7825','220613': '1353','220631': '3199','220635': '5125','213088': '3152','213081': '3615','213056': '5844','213098': '3175','213080': '6142','213090': '8231','213087': '9683','213048': '2669','213060': '7651','213092': '1579','214499': '4719','213104': '6518','213082': '2825','213047': '4426','213055': '7232','214547': '8168','214485': '5181','213035': '1448','213099': '2692','213066': '1589','213106': '1153','213050': '5947','213574': '7315','213105': '7748','220607': '8132','213072': '7665','213084': '6154','213101': '6526','213039': '9513','213093': '3836','197747': '1956','213064': '4197','213069': '3273','213059': '7665','213070': '1554','213065': '2825','213095': '6689','213097': '7179','204902': '7457','213073': '7321','213049': '5418','213075': '9834','213107': '1821','213083': '5785','204906': '6121','213067': '3416','213063': '2562','204909': '6362','213038': '1676','213071': '6761','213077': '6214','213074': '1532'}
    # Define your own logic here
    return username in valid_credentials and valid_credentials[username] == password

def handle_login(role, check_user_login,check_duplicate_vote):
    # global username
    username = st.text_input(f"{role} User ID")
    password = st.text_input(f"{role} Password", type="password")
    if st.button(f'{role} Login'):
        if check_user_login(username, password):
            if check_duplicate_vote(username):
                st.error("You have already voted")
            else:
                st.session_state['logged_in_as'] = role
                st.session_state['logged_in_user'] = username
                st.experimental_rerun()
                return
        else:
            st.error("Incorrect username or password")
    

if 'logged_in_as' not in st.session_state:
    st.session_state['logged_in_as'] = None

def check_internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        pass
    return False

def get_next_empty_row(worksheet):
    last_row = worksheet.row_count
    worksheet.resize(rows=last_row + 1)  # Adds a row at the end
    next_empty_row = last_row + 1
    return next_empty_row  


def search_student_details(matric_no):
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_key('116wtaWh0Emg_XPIaZ7XQBfU4Bup5EkkF1_JWY3dU030')
    sheet = sh.worksheet('Accreditation_list')
    cell = sheet.find(matric_no, in_column=3)
    if cell:
        row_values = sheet.row_values(cell.row)
        student_name = row_values[0]
        level = row_values[3]
        return student_name, level
    else:
        return None, None

 
def success_page(name, LEVE):
    st.write('You have successfully voted')
    st.write(f'Name: {name}')
    st.write(f'Level: {LEVE}')
    st.image("voted.jpg", width=200)
    st.session_state['valid'] = True
    

     
     

def voting_page():
   
    st.markdown(f"<h1 style='text-align: center;'>NSBS 2024 ELECTION</h1>", unsafe_allow_html=True)

    st.markdown('---')
    st.markdown(f"<h1 style='text-align: center;'>PRESIDENT</h1>", unsafe_allow_html=True)
    user = st.session_state['logged_in_user']


    c1, c2 = st.columns(2)
    with c1:
            st.image('presido.jpg',caption="Adesokan Opeyemi Ayobami, A 300level Biochemistry Student" ,width=180)
    
    
    

    president = st.radio("Select Presidential candidate",['VOID','Adesokan Opeyemi Ayobami'])

    st.markdown('---')
    st.markdown(f"<h1 style='text-align: center;'>VICE PRESIDENT</h1>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
            st.image('vice.jpg',caption='OLADUNJOYE ESTHER TITILAYOMI, A 300L Student' ,width=180)
    # with c4:
    #             st.image('qowiyah.jpg',caption='qowiyah' ,width=120)

    v_president = st.radio("Select Vice Presidential candidate",['VOID','Oladunjoye Esther Titilayomi'])

    
    st.markdown('---')
    st.markdown(f"<h1 style='text-align: center;'>FINANCIAL SECRETARY</h1>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
            st.image('finsec.jpg',caption=' LAWAL ODUNAYO GBEMISOLA, A 200L Student' ,width=200)

    finsec = st.radio("Select FINANCIAL SECRETARY candidate",['VOID',' Lawal Odunayo Gbemisola'])

    
    st.markdown('---')
    st.markdown(f"<h1 style='text-align: center;'>GENERAL SECRETARY</h1>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
            st.image('gensec.jpg',caption='Okoya Abidemi Olamide, A 200L Student' ,width=200)


    gensec = st.radio("Select GENERAL SECRETARY candidate",['VOID','Okoya Abidemi Olamide'])



    
    st.markdown('---')
    st.markdown(f"<h1 style='text-align: center;'>PUBLIC RELATIONS OFFICER</h1>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
            st.image('pro.jpg',caption='Ogunseye Tiwalade Isaac, A 200L Student' ,width=180)



    pro = st.radio("Select PUBLIC RELATIONS OFFICER candidate",['VOID','Ogunseye Tiwalade Isaac'])
    



    
    if 'clicked' not in st.session_state:
        st.session_state['clicked'] = False
    if st.button('Submit vote'):
            session_state.page = 'fresh'
            with st.spinner('Submitting, Please wait...'): 
                        if check_internet_connection():
                            if not st.session_state['clicked']:
                                st.session_state['clicked'] = True
                                gc = gspread.service_account(filename='credentials.json')
                                sh = gc.open_by_key('116wtaWh0Emg_XPIaZ7XQBfU4Bup5EkkF1_JWY3dU030')
                                sheet = sh.worksheet('VOTE')
                                next_empty_row = get_next_empty_row(sheet)
                                name, level = search_student_details(user)
                                vote_cell_to_update =[]
                                vote_cell_to_update.append(Cell(next_empty_row, 1, user))
                                vote_cell_to_update.append(Cell(next_empty_row, 2, name))
                                vote_cell_to_update.append(Cell(next_empty_row, 3, level))
                                vote_cell_to_update.append(Cell(next_empty_row, 4, president))
                                vote_cell_to_update.append(Cell(next_empty_row, 5, v_president))
                                vote_cell_to_update.append(Cell(next_empty_row, 6, finsec))
                                vote_cell_to_update.append(Cell(next_empty_row, 7, gensec))
                                vote_cell_to_update.append(Cell(next_empty_row, 8, pro))

                                sheet.update_cells(vote_cell_to_update)
                                

                                st.success('Vote submitted successfully')
                                st.balloons()
                           
                          
                                t.sleep(3)
                                st.session_state['voter_name'] = name
                                st.session_state['LEVEL'] = level
                                st.session_state['vote_success'] = True
                                st.session_state['logged_in_as'] = 'last page'
                           
                                st.experimental_rerun()
                            else:
                                name, department = search_student_details(user)
                                st.session_state['voter_name'] = name
                                st.session_state['voter_department'] = department
                                st.error('You have already voted')
                                t.sleep(2)
                                with st.spinner('Loading...'):
                                    st.session_state['logged_in_as'] = 'last page'
                                    st.experimental_rerun()
                        
                    

                        else:
                            error_placeholder = st.empty()
                            error_placeholder.error("No internet connection")
                            t.sleep(3)
                            error_placeholder.empty()

               


if st.session_state['logged_in_as'] == 'last page':
    success_page(st.session_state['voter_name'], st.session_state['LEVEL'])

             
                



        
            


def login_page():
       
    if st.session_state['logged_in_as'] is None:
        selected = option_menu(
                menu_title=None,
                options=["LOGIN", "VOTE INFO", "VOTE RESULT"],
                icons=["box-arrow-in-left", "envelope-paper-fill", "file-earmark-bar-graph-fill"],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
                styles="menu-bar",
                
        )

        
        if selected == "VOTE INFO":
            st.markdown(f"<h1 style='text-align: center;'> WELCOME METABOLITE</h1>", unsafe_allow_html=True)
            with st.spinner('Loading...'):
                scopes = ["https://www.googleapis.com/auth/spreadsheets"]
                creds = Credentials.from_service_account_file('credentials.json', scopes= scopes)
                client = gspread.authorize(creds)
                sheet_id = '116wtaWh0Emg_XPIaZ7XQBfU4Bup5EkkF1_JWY3dU030'
                sheet = client.open_by_key(sheet_id)
                casted_vote = len(sheet.worksheet("VOTE").get_all_records())
                num_of_voters = len(sheet.worksheet("Accreditation_list").get_all_records())

            st.write(f'NUMBER OF VOTE CASTED: {casted_vote}')
            st.write(f'NUMBER OF ACCREDITED VOTERS: {num_of_voters}')

        elif selected == "VOTE RESULT":
            st.markdown(f"<h1 style='text-align: center;'> WELCOME METABOLITE</h1>", unsafe_allow_html=True)

            st.write(f'Result in progress...')

        else:
            # selected == "LOGIN":
            st.markdown(f"<h1 style='text-align: center;'> WELCOME METABOLITE</h1>", unsafe_allow_html=True)

            st.write('Please enter your credentials below to login')

            handle_login('Student', check_user_login, check_duplicate_vote)
           

    elif st.session_state['logged_in_as'] == 'Student' and not st.session_state['vote_success']:
        voting_page()



            
if 'vote_success' not in st.session_state:
    st.session_state['vote_success'] = False


login_page()
    
