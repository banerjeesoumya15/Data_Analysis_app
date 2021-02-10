# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 13:18:33 2021

@author: Soumya
"""

# import packages
import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import os
#import time

def file_selector(path='./datasets'):
    '''
    Selects a file present in the path folder.

    Parameters
    ----------
    path : str, optional
        The path wwhere files are present. The default is './datasets'.

    Returns
    -------
    str
        Full path of the selected file.

    '''
    filenames = os.listdir(path)
    selected_file = st.selectbox("Select a file", filenames)
    return os.path.join(path, selected_file)

def main():
    '''
    Data Analysis app using streamlit
    This app generates various general plots required to analyse a 
    typical dataset.

    Returns
    -------
    None.

    '''
    
    st.header('Data Analysis')
    st.subheader('Using streamlit')
    
    # select file
    full_filename = file_selector()
    st.success("You selected \{}".format(full_filename[2:]))
    #st.markdown("> You selected \{}".format(full_filename[2:]))
    
    # Read data
    df = pd.read_csv(full_filename)
    
    # get list of columns
    columns = list(df.columns)
    
    # Show dataset
    with st.beta_expander("Show Dataset"):
        # number input
        no_of_rows = st.number_input("No. of rows to display", 1, len(df))
        select_column = st.multiselect("Select columns", columns, default=columns[:3])
        st.dataframe(df[select_column].head(no_of_rows))
        
        st.success("Shape of the original dataset is {} rows and {} columns".format(df.shape[0], df.shape[1]))
        
    # Show no. of missing values
    def highlight_positive(s):
        '''
        Define function to highlight positive values

        '''
        is_zero = s!=0
        return ['background-color: yellow' if v else '' for v in is_zero]
        
    with st.beta_expander("Show number of missing values"):
        #st.write(df.isna().sum())
        df_missing_vals = pd.DataFrame(df.isna().sum())
        st.dataframe(df_missing_vals.style.apply(highlight_positive))
    
    # Show datatypes
    with st.beta_expander("Show datatypes"):
        st.write(df.dtypes)
        
    # Show value counts
    with st.beta_expander("Show unique value counts"):
        #st.markdown("#### Select a column")
        select_column = st.selectbox("Select a column", columns)
        st.write(df.loc[:, select_column].value_counts())
        
    # Show summary
    with st.beta_expander("Show Summary"):
        st.write(df.describe())
        
        
    st.markdown("----------")
    # Visualisation
    st.subheader("Visualisation")
    # Correlation plot
    with st.beta_expander("Correlation - heatmap"):
        fig, ax = plt.subplots()
        sns.heatmap(df.corr(), annot=True)
        st.pyplot(fig)
        
    # Generate pie plot
    with st.beta_expander("Pie plot"):
        column = st.selectbox("Select a column", columns, key="Pie plot")
        fig, ax = plt.subplots()
        df.loc[:,column].value_counts().plot.pie(autopct="%1.1f%%")
        st.pyplot(fig)
        
    # Generate count plot
    with st.beta_expander("Count plot"):
        group_by_column = st.selectbox("Select a column to group by", columns)
        selected_columns = st.multiselect("Columns to be displayed", columns, default=columns[0])
        if st.button("Plot"):
            count_plot = df.groupby(group_by_column)[selected_columns].count()
            st.dataframe(count_plot)
            st.bar_chart(count_plot)
            
    with st.beta_expander("Customisable plots"):
        type_of_plot = st.selectbox("Select type of plot", ['area','bar','line','hist','box','kde'])
        selected_columns = st.multiselect("Columns to be displayed", columns, default=columns[0], key='custom plot')
        
        if st.button("Geenerate {} plot".format(type_of_plot)):
            
            if type_of_plot == 'area':
                st.area_chart(df[selected_columns])
                
            elif type_of_plot == 'bar':
                st.bar_chart(df[selected_columns])
                
            elif type_of_plot == 'line':
                st.line_chart(df[selected_columns])
                
            elif type_of_plot:
                st.write(df[selected_columns].plot(kind=type_of_plot))
                #st.pyplot()
                
    st.markdown("-----------")
    if st.button("Thanks"):
        st.balloons()
        
    st.sidebar.header("About App")
    st.sidebar.success("A simple app to perform generic data analysis functions on datasets.")
    st.sidebar.error("Currently the app performs the following functions:")
    st.sidebar.markdown(" - <font color='blue'>Select a file from pre-defined set of files</font>", unsafe_allow_html=True)
    st.sidebar.markdown(" - <font color='blue'>Preview the dataset as per number of rows and columns selected</font>", unsafe_allow_html=True)
    st.sidebar.markdown(" - <font color='blue'>Highlight number of missing values in each column</font>", unsafe_allow_html=True)
    st.sidebar.markdown(" - <font color='blue'>Display datatypes of each column</font>", unsafe_allow_html=True)
    st.sidebar.markdown(" - <font color='blue'>Display number of unique values in a column</font>", unsafe_allow_html=True)
    st.sidebar.markdown(" - <font color='blue'>Display summary of numerical columns of the dataset</font>", unsafe_allow_html=True)
    
    st.sidebar.markdown(" - <font color='blue'>Visualise heatmap of correlation matrix</font>", unsafe_allow_html=True)
    st.sidebar.markdown(" - <font color='blue'>Display pie plot, bar plot, line plot, box plot, histogram, distribution plot</font>", unsafe_allow_html=True)
    
    st.sidebar.text("")
    st.sidebar.text("")
    st.sidebar.markdown("Built by Soumya")
    st.sidebar.markdown("e-mail: banerjeesoumya15@gmail.com")
        

if __name__=='__main__':
    main()