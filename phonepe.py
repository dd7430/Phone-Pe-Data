import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as plt
import json
import requests
from PIL import Image

mydb = psycopg2.connect(host="localhost",
                        user='postgres',
                        port="5432",
                        database="phonepe_data",
                        password="Danv2001")

cursor= mydb.cursor()

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1= cursor.fetchall()

Aggregrated_insurance = pd.DataFrame(table1, columns=("States", "Years", "Quarter", 'Transaction_Type', 'Transaction_Count', "Transaction_Amount"))

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2= cursor.fetchall()

Aggregrated_transaction = pd.DataFrame(table2, columns=("States", "Years", "Quarter", 'Transaction_Type', 'Transaction_Count', "Transaction_Amount"))

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3= cursor.fetchall()

Aggregrated_user = pd.DataFrame(table3, columns=("States", "Years", "Quarter", 'Brands', 'Transaction_Count', "Percentage"))

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= cursor.fetchall()

Map_insurance = pd.DataFrame(table4, columns=("States", "Years", "Quarter", 'District_Name', 'Transaction_Count', "Transaction_Amount"))

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= cursor.fetchall()

Map_transaction = pd.DataFrame(table5, columns=("States", "Years", "Quarter", 'District_Name', 'Transaction_Count', "Transaction_Amount"))

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= cursor.fetchall()

Map_user = pd.DataFrame(table6, columns=("States", "Years", "Quarter", 'District_Name', 'Registered_Users', "App_Opens"))

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= cursor.fetchall()

Top_insurance = pd.DataFrame(table7, columns=("States", "Years", "Quarter", 'Pincodes', 'Transaction_Count', "Transaction_Amount"))

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

Top_transaction = pd.DataFrame(table8, columns=("States", "Years", "Quarter", 'Entity_Name', 'Transaction_Count', "Transaction_Amount"))

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= cursor.fetchall()

Top_user = pd.DataFrame(table9, columns=("States", "Years", "Quarter", 'Pincodes', 'Registered_Users'))




def Transaction_Amount_Count_Y(df, year):
    A1 = df[df["Years"] == year]
    A1.reset_index(drop= True, inplace= True)

    A11 = A1.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    A11.reset_index(inplace= True)
    
    col1,col2 = st.columns(2)
    with col1:

        fig_amount = plt.bar(A11, x="States", y="Transaction_Amount", title=f"{year} Transaction Amount", color_discrete_sequence=plt.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = plt.bar(A11, x="States", y="Transaction_Count", title=f"{year} Transaction Count", color_discrete_sequence=plt.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_count)
    
        
    col1,col2 = st.columns(2)
    with col1:
        
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        d1 = json.loads(response.content)
        state_names= []
        for feature in d1["features"]:
            state_names.append(feature["properties"]["ST_NM"])
            
        state_names.sort()

        india_fig_1 = plt.choropleth(A11, geojson=d1, locations= "States", featureidkey="properties.ST_NM",
                                    color="Transaction_Amount", color_continuous_scale="Rainbow",
                                    range_color= (A11["Transaction_Amount"].min(), A11["Transaction_Amount"].max()),
                                    hover_name="States", title= f"{year} Transaction Amount", fitbounds= "locations",
                                    height=600, width=600)
        india_fig_1.update_geos(visible= False)
        
        st.plotly_chart(india_fig_1)
    
    with col2:
        
        india_fig_2 = plt.choropleth(A11, geojson=d1, locations= "States", featureidkey="properties.ST_NM",
                                    color="Transaction_Count", color_continuous_scale="Rainbow",
                                    range_color= (A11["Transaction_Count"].min(), A11["Transaction_Count"].max()),
                                    hover_name="States", title= f"{year} Transaction Count", fitbounds= "locations",
                                    height=600, width=600)
        india_fig_2.update_geos(visible= False)
        
        st.plotly_chart(india_fig_2)
        
    return A1
        
    
def Transaction_Amount_Count_Y_Q(df, quarter):
    A1 =df[df["Quarter"] == quarter]
    A1.reset_index(drop= True, inplace= True)

    A11 = A1.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    A11.reset_index(inplace= True)
    
    col1,col2 = st.columns(2)
    with col1:

        fig_amount = plt.bar(A11, x="States", y="Transaction_Amount", title=f"{A1['Years'].unique()} YEAR {quarter} QUARTER Transaction Amount", color_discrete_sequence=plt.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = plt.bar(A11, x="States", y="Transaction_Count", title=f"{A1['Years'].unique()} YEAR {quarter} QUARTER Transaction Count", color_discrete_sequence=plt.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_count)
    
        
    col1,col2 = st.columns(2)
    with col1:
        
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        d1 = json.loads(response.content)
        state_names= []
        for feature in d1["features"]:
            state_names.append(feature["properties"]["ST_NM"])
            
        state_names.sort()

        india_fig_1 = plt.choropleth(A11, geojson=d1, locations= "States", featureidkey="properties.ST_NM",
                                    color="Transaction_Amount", color_continuous_scale="Rainbow",
                                    range_color= (A11["Transaction_Amount"].min(), A11["Transaction_Amount"].max()),
                                    hover_name="States", title= f"{A1['Years'].unique()} YEAR {quarter} QUARTER Transaction Amount", fitbounds= "locations",
                                    height=600, width=600)
        india_fig_1.update_geos(visible= False)
        
        st.plotly_chart(india_fig_1)
    
    with col2:
        india_fig_2 = plt.choropleth(A11, geojson=d1, locations= "States", featureidkey="properties.ST_NM",
                                    color="Transaction_Count", color_continuous_scale="Rainbow",
                                    range_color= (A11["Transaction_Count"].min(), A11["Transaction_Count"].max()),
                                    hover_name="States", title= f"{A1['Years'].unique()} YEAR {quarter} QUARTER Transaction Count", fitbounds= "locations",
                                    height=600, width=600)
        india_fig_2.update_geos(visible= False)
        
        st.plotly_chart(india_fig_2)
        
    return A1
        
        
def Aggregrated_Tran_Transaction_Type(df, state):

    A1 =df[df["States"] == state]
    A1.reset_index(drop= True, inplace= True)

    A11 = A1.groupby("Transaction_Type")[["Transaction_Count","Transaction_Amount"]].sum()
    A11.reset_index(inplace= True)
    
    col1,col2= st.columns(2)
    with col1:
        fig_pie_1= plt.pie(data_frame = A11, names="Transaction_Type", values= "Transaction_Amount", 
                        width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)

        st.plotly_chart(fig_pie_1)
    
    with col2:
        fig_pie_2= plt.pie(data_frame = A11, names="Transaction_Type", values= "Transaction_Count", 
                        width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)

        st.plotly_chart(fig_pie_2)
        
def Aggregated_User_Plot_1(df, year):
    aguy = df[df["Years"]==year]
    aguy.reset_index(drop=True, inplace=True)

    aguy_g = pd.DataFrame(aguy.groupby("Brands")["Transaction_Count"].sum())
    aguy_g.reset_index(inplace=True)


    fig_bar_1 = plt.bar(aguy_g, x="Brands", y="Transaction_Count", title=f"{year} Brands and Transaction Count",
                        width = 900, color_discrete_sequence= plt.colors.sequential.haline, hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguy

def Aggregated_User_Plot_2(df, quarter):
    aguyq = df[df["Quarter"]== quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_Count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1 = plt.bar(aguyqg, x="Brands", y="Transaction_Count", title=f"{quarter} Quarter Brands and Transaction Count",
                            width = 900, color_discrete_sequence= plt.colors.sequential.haline, hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguyq

def Aggregrated_User_Plot_3(df, state):
    auyqs = df[df["States"]==state] 
    auyqs.reset_index(drop=True, inplace=True)

    fig_line_1= plt.line(auyqs, x="Brands", y="Transaction_Count", hover_data="Percentage",
                        title=f"{state} Brands, Transaction Count and Percentage", color_discrete_sequence=plt.colors.sequential.algae_r,
                        width=1000, markers=True)
    st.plotly_chart(fig_line_1)
    
    return auyqs

#TMap Insurance District
def map_insurance_district(df, state):

    A1 =df[df["States"] == state]
    A1.reset_index(drop= True, inplace= True)

    A11 = A1.groupby("District_Name")[["Transaction_Count","Transaction_Amount"]].sum()
    A11.reset_index(inplace= True)
    
    col1,col2 = st.columns(2)
    with col1:

        fig_bar_1= plt.bar(A11, x="Transaction_Amount", y= "District_Name", height=600,
                        orientation="h", title=f"{state} District And Transaction Amount", color_discrete_sequence=plt.colors.sequential.Darkmint_r)

        st.plotly_chart(fig_bar_1)
    
    with col2:

        fig_bar_2= plt.bar(A11, x="Transaction_Count", y= "District_Name", height=600,
                        orientation="h", title=f"{state} District And Transaction Count", color_discrete_sequence=plt.colors.sequential.Blackbody_r)

        st.plotly_chart(fig_bar_2)
        
        
#map_user_plot_1
def map_user_plot_1(df, year):
    muy = df[df["Years"]==year]
    muy.reset_index(drop=True, inplace=True)

    muy_g = muy.groupby("States")[["Registered_Users", "App_Opens"]].sum()
    muy_g.reset_index(inplace=True)

    fig_line_1= plt.line(muy_g, x="States", y=["Registered_Users", "App_Opens"],
                        title=f"{year} Registered User and App Open",
                        width=1000, height=800, markers=True)
    st.plotly_chart(fig_line_1)
    
    return muy

#map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq = df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyq_g = muyq.groupby("States")[["Registered_Users", "App_Opens"]].sum()
    muyq_g.reset_index(inplace=True)

    fig_line_2= plt.line(muyq_g, x="States", y=["Registered_Users", "App_Opens"],
                        title=f"{df['Years'].min()} Year {quarter} Quarter Registered User and App Open",
                        width=1000, height=800, markers=True)
    st.plotly_chart(fig_line_2)

    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs =  df[df["States"]== states]
    muyqs.reset_index(drop=True, inplace=True)
    
    col1, col2= st.columns(2)
    with col1:
        fig_map_user_bar_1 = plt.bar(muyqs, x= "Registered_Users", y= "District_Name", orientation= "h",
                                    title= f"{states.upper()} Registered Users", height= 800, color_discrete_sequence= plt.colors.sequential.Reds_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2 = plt.bar(muyqs, x= "App_Opens", y= "District_Name", orientation= "h",
                                    title= f"{states.upper()} App Opens", height= 800, color_discrete_sequence= plt.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_2)
        
#Top_Insurance_Plot_1
def top_insurance_plot_1(df, state):
    tiy = df[df["States"]== state]
    tiy.reset_index(drop=True, inplace=True)

    tiy_g = tiy.groupby("Pincodes")[["Transaction_Count", "Transaction_Amount"]].sum()
    tiy_g.reset_index(inplace=True)
    
    col1, col2= st.columns(2)
    with col1:
        fig_top_insurance_bar_1 = plt.bar(tiy, x= "Quarter", y= "Transaction_Amount", hover_data= "Pincodes",
                                    title= "Transaction Amount", height= 650, width=600, color_discrete_sequence= plt.colors.sequential.Reds_r)
        st.plotly_chart(fig_top_insurance_bar_1)
        
    with col2:
        fig_top_insurance_bar_2 = plt.bar(tiy, x= "Quarter", y= "Transaction_Count", hover_data= "Pincodes",
                                    title= "Transaction Count",height= 650, width=600, color_discrete_sequence= plt.colors.sequential.algae_r)
        st.plotly_chart(fig_top_insurance_bar_2)


#Top_Transaction_Plot_1
def top_transaction_plot_1(df, state):
    tty = df[df["States"]== state]
    tty.reset_index(drop=True, inplace=True)

    tty_g = tty.groupby("Entity_Name")[["Transaction_Count", "Transaction_Amount"]].sum()
    tty_g.reset_index(inplace=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig_top_insurance_bar_1 = plt.bar(tty, x= "Quarter", y= "Transaction_Amount", hover_data= "Entity_Name",
                                    title= "Transaction Amount", height= 650, width=600, color_discrete_sequence= plt.colors.sequential.Reds_r)
        st.plotly_chart(fig_top_insurance_bar_1)
    
    with col2:
        fig_top_insurance_bar_2 = plt.bar(tty, x= "Quarter", y= "Transaction_Count", hover_data= "Entity_Name",
                                        title= "Transaction Count", height= 650, width=600, color_discrete_sequence= plt.colors.sequential.algae_r)
        st.plotly_chart(fig_top_insurance_bar_2)
 
    
# top user plot 1
def top_user_plot_1(df, years):
    tuy = df[df["Years"]==years]
    tuy.reset_index(drop=True, inplace=True)

    tuy_g = pd.DataFrame(tuy.groupby(["States", "Quarter"])["Registered_Users"].sum())
    tuy_g.reset_index(inplace=True)

    fig_top_user_plot_1 = plt.bar(tuy_g, x="States", y="Registered_Users", hover_name="States", color="Quarter", width=1000, height=800,
                                color_discrete_sequence=plt.colors.sequential.Plasma_r, title=f"{years} Registered Users Top User")
    st.plotly_chart(fig_top_user_plot_1)

    return tuy

#top user plot 2
def top_user_plot_2(df,state):
    tuys = df[df["States"]== state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_user_plot_2 = plt.bar(tuys, x="Quarter", y="Registered_Users", title=f"{state} Registered Users, Pincodes, Quarter",
                                width= 1000, height=800, color="Registered_Users", hover_data="Pincodes", color_continuous_scale= plt.colors.sequential.Mint_r)

    st.plotly_chart(fig_top_user_plot_2)
    
    
    
def top_chart_transaction_amount(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user='postgres',
                            port="5432",
                            database="phonepe_data",
                            password="Danv2001")

    cursor= mydb.cursor()

    query_1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''
                
    cursor.execute(query_1)
    table_1= cursor.fetchall()

    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_amount"))
    
    col1,col2= st.columns(2)
    
    with col1:
        fig_amount_1 = plt.bar(df_1, x="states", y="transaction_amount", title="Transaction Amount Descending",
                            hover_name= "states", color_discrete_sequence=plt.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_1)

    #plot_2
    query_2= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;'''
                
    cursor.execute(query_2)
    table_2= cursor.fetchall()

    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_amount"))

    with col2:
        
        fig_amount_2 = plt.bar(df_2, x="states", y="transaction_amount", title="Transaction Amount Ascending",
                            hover_name= "states", color_discrete_sequence=plt.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_2)



    #plot_3
    query_3= f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''
                
    cursor.execute(query_3)
    table_3= cursor.fetchall()

    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_3 = plt.bar(df_3, y="states", x="transaction_amount", title="Transaction Amount Average", orientation='h',
                        hover_name= "states", color_discrete_sequence=plt.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_amount_3)
    
    
 #top chart transaction count   
def top_chart_transaction_count(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user='postgres',
                            port="5432",
                            database="phonepe_data",
                            password="Danv2001")

    cursor= mydb.cursor()

    query_1= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''
                
    cursor.execute(query_1)
    table_1= cursor.fetchall()

    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_count"))
    
    col1,col2 = st.columns(2)
    
    with col1:
        fig_amount_1 = plt.bar(df_1, x="states", y="transaction_count", title="Transaction Count Descending",
                            hover_name= "states", color_discrete_sequence=plt.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_1)

    #plot_2
    query_2= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''
                
    cursor.execute(query_2)
    table_2= cursor.fetchall()

    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_count"))
    
    with col2:

        fig_amount_2 = plt.bar(df_2, x="states", y="transaction_count", title="Transaction Count Ascending",
                            hover_name= "states", color_discrete_sequence=plt.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_2)



    #plot_3
    query_3= f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''
                
    cursor.execute(query_3)
    table_3= cursor.fetchall()

    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_3 = plt.bar(df_3, y="states", x="transaction_count", title="Transaction Count Average", orientation='h',
                        hover_name= "states", color_discrete_sequence=plt.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_amount_3)
    

def top_chart_registered_users(table_name, state):
    mydb = psycopg2.connect(host="localhost",
                            user='postgres',
                            port="5432",
                            database="phonepe_data",
                            password="Danv2001")

    cursor= mydb.cursor()

    query_1= f'''SELECT district, SUM(registered_users) AS registered_users
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY district
                ORDER BY registered_users DESC
                LIMIT 10;'''
                
    cursor.execute(query_1)
    table_1= cursor.fetchall()

    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("district", "registered_users"))
    
    col1,col2 = st.columns(2)
    
    with col1:
        fig_amount_1 = plt.bar(df_1, x="district", y="registered_users", title="Registered Users Descending",
                            hover_name= "district", color_discrete_sequence=plt.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_1)

    #plot_2
    query_2= f'''SELECT district, SUM(registered_users) AS registered_users
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY district
                ORDER BY registered_users 
                LIMIT 10;'''
                
    cursor.execute(query_2)
    table_2= cursor.fetchall()

    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("district", "registered_users"))
    
    with col2:
        fig_amount_2 = plt.bar(df_2, x="district", y="registered_users", title="Registered Users Ascending",
                            hover_name= "district", color_discrete_sequence=plt.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_2)



    #plot_3
    query_3= f'''SELECT district, AVG(registered_users) AS registered_users
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY district
                ORDER BY registered_users;'''
                
    cursor.execute(query_3)
    table_3= cursor.fetchall()

    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("district", "registered_users"))

    fig_amount_3 = plt.bar(df_3, y="district", x="registered_users", title="Registered Users Average", orientation='h',
                        hover_name= "district", color_discrete_sequence=plt.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_amount_3)
    

def top_chart_app_opens(table_name, state):
    mydb = psycopg2.connect(host="localhost",
                            user='postgres',
                            port="5432",
                            database="phonepe_data",
                            password="Danv2001")

    cursor= mydb.cursor()

    query_1= f'''SELECT district, SUM(app_opens) AS app_opens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY district
                ORDER BY app_opens DESC
                LIMIT 10;'''
                
    cursor.execute(query_1)
    table_1= cursor.fetchall()

    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("district", "app_opens"))

    col1,col2 = st.columns(2)
    
    with col1:
        fig_amount_1 = plt.bar(df_1, x="district", y="app_opens", title="App Opens Descending",
                            hover_name= "district", color_discrete_sequence=plt.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_1)

    #plot_2
    query_2= f'''SELECT district, SUM(app_opens) AS app_opens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY district
                ORDER BY app_opens
                LIMIT 10;'''
                
    cursor.execute(query_2)
    table_2= cursor.fetchall()

    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("district", "app_opens"))
    
    with col2:
        fig_amount_2 = plt.bar(df_2, x="district", y="app_opens", title="App Opens Ascending",
                            hover_name= "district", color_discrete_sequence=plt.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_2)



    #plot_3
    query_3= f'''SELECT district, AVG(app_opens) AS app_opens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY district
                ORDER BY app_opens;'''
                
    cursor.execute(query_3)
    table_3= cursor.fetchall()

    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("district", "app_opens"))

    fig_amount_3 = plt.bar(df_3, y="district", x="app_opens", title="App Opens Average", orientation='h',
                        hover_name= "district", color_discrete_sequence=plt.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_amount_3)
    
    
def top_chart_registered_users_1(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user='postgres',
                            port="5432",
                            database="phonepe_data",
                            password="Danv2001")

    cursor= mydb.cursor()

    query_1= f'''SELECT states, SUM(registered_users) AS registered_users
                FROM {table_name}
                GROUP BY states
                ORDER BY registered_users DESC
                LIMIT 10;'''
                
    cursor.execute(query_1)
    table_1= cursor.fetchall()

    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "registered_users"))
    
    col1,col2 = st.columns(2)
    
    with col1:
        fig_amount = plt.bar(df_1, x="states", y="registered_users", title="Registered Users Descending",
                            hover_name= "states", color_discrete_sequence=plt.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query_2= f'''SELECT states, SUM(registered_users) AS registered_users
                FROM {table_name}
                GROUP BY states
                ORDER BY registered_users DESC
                LIMIT 10;'''
                
    cursor.execute(query_2)
    table_2= cursor.fetchall()

    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "registered_users"))
    
    with col2:
        fig_amount_2 = plt.bar(df_2, x="states", y="registered_users", title="Registered Users Ascending",
                            hover_name= "states", color_discrete_sequence=plt.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount_2)



    #plot_3
    query_3= f'''SELECT states, AVG(registered_users) AS registered_users
                FROM {table_name}
                GROUP BY states
                ORDER BY registered_users;'''
                
    cursor.execute(query_3)
    table_3= cursor.fetchall()

    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "registered_users"))

    fig_amount_3 = plt.bar(df_3, y="states", x="registered_users", title="Registered Users Average", orientation='h',
                        hover_name= "states", color_discrete_sequence=plt.colors.sequential.Bluered_r, height=800, width=1000)
    st.plotly_chart(fig_amount_3)
    

#streamlit part

st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    
    select= option_menu("Main Menu",["HOME","DATA EXPLORATION", "TOP CHARTS" ] )
    
if select == "HOME":
    
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    
    with col2:
        st.image(Image.open(r"C:\Users\USER PC\OneDrive\Desktop\Projects\phonepe\download.png"),width= 600)
        
    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\USER PC\OneDrive\Desktop\Projects\phonepe\v-emhrqu_400x400.png"),width=600)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")
        
    
    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\USER PC\OneDrive\Desktop\Projects\phonepe\download11.jpeg"),width= 600)



elif select == "DATA EXPLORATION":
    
    tab1, tab2, tab3 = st.tabs(["Aggregrated", "Map", "Top"])
    
    with tab1:
        method = st.radio("Select the Method", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])
        
        if method == "Insurance Analysis":
            
            col1,col2= st.columns(2)
            with col1:
            
                years=st.slider("Select the Year", Aggregrated_insurance["Years"].min(), Aggregrated_insurance["Years"].max(), Aggregrated_insurance["Years"].min())
            tac_Y = Transaction_Amount_Count_Y(Aggregrated_insurance, years) 
            
            col1, col2= st.columns(2)
            with col1:
                
                quarters=st.slider("Select the Quarter", tac_Y["Quarter"].min(), tac_Y["Quarter"].max(), tac_Y["Quarter"].min())
            Transaction_Amount_Count_Y_Q(tac_Y, quarters)
                
        
        elif method == "Transaction Analysis":
            
            col1,col2= st.columns(2)
            with col1:
            
                years=st.slider("Select the Year", Aggregrated_transaction["Years"].min(), Aggregrated_transaction["Years"].max(), Aggregrated_transaction["Years"].min())
            Aggregrated_transaction_tac_Y = Transaction_Amount_Count_Y(Aggregrated_transaction, years)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select the State",Aggregrated_transaction_tac_Y["States"].unique())
                
            Aggregrated_Tran_Transaction_Type(Aggregrated_transaction_tac_Y, states)
            
            col1, col2= st.columns(2)
            with col1:
                
                quarters=st.slider("Select the Quarter", Aggregrated_transaction_tac_Y["Quarter"].min(), Aggregrated_transaction_tac_Y["Quarter"].max(), Aggregrated_transaction_tac_Y["Quarter"].min())
            Aggregrated_transaction_tac_Y_Q= Transaction_Amount_Count_Y_Q(Aggregrated_transaction_tac_Y, quarters)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select the State_Ty",Aggregrated_transaction_tac_Y_Q["States"].unique())
                
            Aggregrated_Tran_Transaction_Type(Aggregrated_transaction_tac_Y_Q, states)
        
        elif method == "User Analysis":
            
            
            col1,col2= st.columns(2)
            with col1:
            
                years=st.slider("Select the Year", Aggregrated_user["Years"].min(), Aggregrated_user["Years"].max(), Aggregrated_user["Years"].min())
            Aggregrated_user_Y = Aggregated_User_Plot_1(Aggregrated_user, years)
            
            col1, col2= st.columns(2)
            with col1:
                
                quarters=st.slider("Select the Quarter", Aggregrated_user_Y["Quarter"].min(), Aggregrated_user_Y["Quarter"].max(), Aggregrated_user_Y["Quarter"].min())
            Aggregrated_user_Y_Q= Aggregated_User_Plot_2(Aggregrated_user_Y, quarters)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select the State",Aggregrated_user_Y_Q["States"].unique())
                
            Aggregrated_User_Plot_3(Aggregrated_user_Y_Q, states)
        
    
    with tab2:
        method_2 = st.radio("Select the Method", ["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])
        
        if method_2== "Map Insurance Analysis":
            
            col1,col2= st.columns(2)
            with col1:
            
                years=st.slider("Select the Year Map Insurance", Map_insurance["Years"].min(), Map_insurance["Years"].max(), Map_insurance["Years"].min())
            map_insurance_tac_Y = Transaction_Amount_Count_Y(Map_insurance, years)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select the State Map Insurance",map_insurance_tac_Y["States"].unique())
                
            map_insurance_district(map_insurance_tac_Y, states)
            
            col1, col2= st.columns(2)
            with col1:
                
                quarters=st.slider("Select the Quarter Map Insurance", map_insurance_tac_Y["Quarter"].min(), map_insurance_tac_Y["Quarter"].max(), map_insurance_tac_Y["Quarter"].min())
            map_insurance_tac_Y_Q= Transaction_Amount_Count_Y_Q(map_insurance_tac_Y, quarters)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select the State Map Insurance",map_insurance_tac_Y_Q["States"].unique())
                
            map_insurance_district(map_insurance_tac_Y_Q, states)
        
        
        elif method_2 == "Map Transaction Analysis":
            
            col1,col2= st.columns(2)
            with col1:
            
                years=st.slider("Select the Year Map Transaction", Map_transaction["Years"].min(), Map_transaction["Years"].max(), Map_transaction["Years"].min())
            map_transaction_tac_Y = Transaction_Amount_Count_Y(Map_transaction, years)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select the State Map Transaction",map_transaction_tac_Y["States"].unique())
                
            map_insurance_district(map_transaction_tac_Y, states)
            
            col1, col2= st.columns(2)
            with col1:
                
                quarters=st.slider("Select the Quarter Map Transaction", map_transaction_tac_Y["Quarter"].min(), map_transaction_tac_Y["Quarter"].max(),map_transaction_tac_Y["Quarter"].min())
            map_transaction_tac_Y_Q= Transaction_Amount_Count_Y_Q(map_transaction_tac_Y, quarters)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select the State Map Transaction Quarter",map_transaction_tac_Y_Q["States"].unique())
                
            map_insurance_district(map_transaction_tac_Y_Q, states)
            
        
        elif method_2 == "Map User Analysis":
            
            col1,col2= st.columns(2)
            with col1:
            
                years=st.slider("Select the Year Map User", Map_user["Years"].min(), Map_user["Years"].max(), Map_user["Years"].min())
            map_user_Y = map_user_plot_1(Map_user, years)
            
            col1, col2= st.columns(2)
            with col1:
                
                quarters=st.slider("Select the Quarter Map User_Q", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q= map_user_plot_2(map_user_Y, quarters)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select the State Map User Quarter",map_user_Y_Q["States"].unique())
                
            map_user_plot_3(map_user_Y_Q, states)
    
    with tab3:
        method_3 = st.radio("Select the Method", ["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])
        
        if method_3== "Top Insurance Analysis":
           
            col1,col2= st.columns(2)
            with col1:
            
                years=st.slider("Select the Year Top Insurance", Top_insurance["Years"].min(), Top_insurance["Years"].max(), Top_insurance["Years"].min())
            top_insurance_tac_Y = Transaction_Amount_Count_Y(Top_insurance, years)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select the State Top Insurance Quarter", top_insurance_tac_Y["States"].unique())
                
            top_insurance_plot_1(top_insurance_tac_Y, states)
            
            col1, col2= st.columns(2)
            with col1:
                
                quarters=st.slider("Select the Quarter Top Insurance_Q", top_insurance_tac_Y["Quarter"].min(), top_insurance_tac_Y["Quarter"].max(),top_insurance_tac_Y["Quarter"].min())
            top_insurance_Y_Q= Transaction_Amount_Count_Y_Q(top_insurance_tac_Y, quarters)
        
        elif method_3 == "Top Transaction Analysis":
            
            col1,col2= st.columns(2)
            with col1:
            
                years=st.slider("Select the Year Top Insurance", Top_transaction["Years"].min(), Top_transaction["Years"].max(), Top_transaction["Years"].min())
            top_transaction_tac_Y = Transaction_Amount_Count_Y(Top_transaction, years)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select the State Top Insurance Quarter", top_transaction_tac_Y["States"].unique())
                
            top_transaction_plot_1(top_transaction_tac_Y, states)
            
            col1, col2= st.columns(2)
            with col1:
                
                quarters=st.slider("Select the Quarter Top Insurance_Q", top_transaction_tac_Y["Quarter"].min(), top_transaction_tac_Y["Quarter"].max(),top_transaction_tac_Y["Quarter"].min())
            top_transaction_Y_Q= Transaction_Amount_Count_Y_Q(top_transaction_tac_Y, quarters)
        
        
        elif method_3 == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
            
                years=st.slider("Select the Year Top User", Top_user["Years"].min(), Top_user["Years"].max(), Top_user["Years"].min())
            top_user_Y = top_user_plot_1(Top_user, years)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select the State",top_user_Y["States"].unique())
                
            top_user_plot_2(top_user_Y, states)
        
elif select == "TOP CHARTS":
    
    question= st.selectbox("Select the Question",["Transaction Amount and Count of Aggregated Insurance",
                                                  "Transaction Amount and Count of Map Insurance",
                                                  "Transaction Amount and Count of Top Insurance",
                                                  "Transaction Amount and Count of Aggregated Transaction",
                                                  "Transaction Amount and Count of Map Transaction",
                                                  "Transaction Amount and Count of Top Transaction",
                                                  "Transaction Count of Aggregated User",
                                                  "Registered Users of Map User",
                                                  "App Opens of Map User",
                                                  "Registered Users of Top User"])

    if question == "Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")
        
    
    elif question == "Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")
        
    elif question == "Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")
        
    elif question == "Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")
        
    elif question == "Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")
        
    elif question == "Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")
        
    elif question == "Transaction Count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")
        
    elif question == "Registered Users of Map User":
        
        states= st.selectbox("Select the State", Map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("Map_user", states)
        
    elif question == "App Opens of Map User":
        
        states= st.selectbox("Select the State", Map_user["States"].unique())
        st.subheader("APP OPENS")
        top_chart_app_opens("Map_user", states)
        
    elif question == "Registered Users of Top User":
        
        st.subheader("REGISTERED USERS")
        top_chart_registered_users_1("Top_user")
    