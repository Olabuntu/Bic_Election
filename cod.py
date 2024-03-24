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

    valid_credentials = {
        "213087": "9999",
        "213088": "8987",
        "user": "eeee",

    }

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
    
