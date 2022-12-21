#%%
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash as d
import time
from streamlit_javascript import st_javascript
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import io 
from st_aggrid import AgGrid
#from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
# %%
st.set_page_config(page_title = 'Otter Financial Reconciliation - beta', layout = 'wide', page_icon = '🍴')
#%%
with st.sidebar:
    choose = option_menu("Financial Reconciliation", ["Executive Summary", "Trends"],
                         icons=['body-text', 'bar-chart'],
                         menu_icon="app", default_index=0, orientation = "vertical",
                         styles={
        "container": {"padding": "3!important", "background-color": "##ED816A"},
        "icon": {"color": "black", "font-size": "20px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#9B6E48"},
    }
    )
#%%
t1 = st.columns(1)
t1= st.title(" Your Financial Reconciliation")
# %%
st.spinner('Getting Your Financial Data...')
df = pd.read_csv('data.csv')
df[["OC Subtotal","OC Tip","other_amount","processing_fee","OC Tax","OC Tax Withheld","Tax Delta","adjustment","commission","net_payout","Subtotal","Tips","Other","Processing Fee","Tax","Tax Withheld","Promos","Adjustment","Merchant Refund","Commission","Order Payout","Final Payout","Tax Delta__1"]] = df[["OC Subtotal","OC Tip","other_amount","processing_fee","OC Tax","OC Tax Withheld","Tax Delta","adjustment","commission","net_payout","Subtotal","Tips","Other","Processing Fee","Tax","Tax Withheld","Promos","Adjustment","Merchant Refund","Commission","Order Payout","Final Payout","Tax Delta__1"]].fillna(0)
dfframe = df[["Ordered Date","OC Order Display ID", "ofo_slug", "OC Brand", "OC Subtotal", "OC Tip", "other_amount", "processing_fee", "OC Tax", "OC Tax Withheld", "Tax Delta", "adjustment","commission", "net_payout"]]
dfframe.columns = ["Order Date", 'Order ID','Platform','Brand','Subtotal','Tip','Other Amount','Processing Fee','Tax','Tax Withheld','Tax Delta','Adjustment','Commission','Expected Payout']
dfframe1 = dfframe.loc[dfframe["Order ID"].notnull(),['Order Date','Order ID','Platform','Brand','Subtotal','Tip','Other Amount','Processing Fee','Tax','Tax Withheld','Tax Delta','Adjustment','Commission','Expected Payout']]
dfframe_canceled1 = df.loc[df["order_status"] == "OFO_STATUS_CANCELED"]
dfframe_canceled2 = dfframe_canceled1[["Ordered Date","OC Order Display ID", "ofo_slug", "OC Brand", "OC Subtotal", "OC Tip", "other_amount", "processing_fee", "OC Tax", "OC Tax Withheld", "Tax Delta", "adjustment","commission", "net_payout"]]
dfframe_canceled2.columns =['Order Date','Order ID','Platform','Brand','Subtotal','Tip','Other Amount','Processing Fee','Tax','Tax Withheld','Tax Delta','Adjustment','Commission','Payout']
dfframe_canceledactpayout = dfframe_canceled1[["Ordered Date","OC Order Display ID", "ofo_slug", "OC Brand", "OC Subtotal", "OC Tip", "other_amount", "processing_fee", "OC Tax", "OC Tax Withheld", "Tax Delta", "adjustment","commission", "net_payout", "Final Payout"]]
dfframe_canceledactpayout.columns =['Order Date','Order ID','Platform','Brand','Subtotal','Tip','Other Amount','Processing Fee','Tax','Tax Withheld','Tax Delta','Adjustment','Commission','Expected Payout', 'Final Payout']
dfframe_orderspaid1 = df.loc[(df["Final Payout"] > 0) & (df["Internal ID"].notnull())]
dfframe_orderspaid2 = dfframe_orderspaid1[["Ordered Date","OC Order Display ID", "ofo_slug", "OC Brand", "order_status", "OC Subtotal", "OC Tip", "other_amount", "processing_fee", "OC Tax", "OC Tax Withheld", "Tax Delta", "adjustment","commission", "net_payout", "Final Payout"]]
dfframe_orderspaid2.columns = ['Order Date','Order ID','Platform','Brand', 'Order Status','Subtotal','Tip','Other Amount','Processing Fee','Tax','Tax Withheld','Tax Delta','Adjustment','Commission','Expected Payout', 'Final Payout']
dfframe_ordersnotpaid1 = df.loc[(df["Final Payout"] == 0) & (df["Internal ID"].notnull())]
dfframe_ordernotpaid2 = dfframe_ordersnotpaid1[["Ordered Date","OC Order Display ID", "ofo_slug", "OC Brand", "order_status", "OC Subtotal", "OC Tip", "other_amount", "processing_fee", "OC Tax", "OC Tax Withheld", "Tax Delta", "adjustment","commission", "net_payout", "Final Payout"]]
dfframe_ordernotpaid2.columns = ['Order Date','Order ID','Platform','Brand', 'Order Status','Subtotal','Tip','Other Amount','Processing Fee','Tax','Tax Withheld','Tax Delta','Adjustment','Commission','Expected Payout', 'Final Payout']
dfframe_negativepay1 = df.loc[(df["Final Payout"] < 0) & (df["Internal ID"].notnull())]
dfframe_negativepay2 = dfframe_negativepay1[["Ordered Date","OC Order Display ID", "ofo_slug", "OC Brand", "order_status", "OC Subtotal", "OC Tip", "other_amount", "processing_fee", "OC Tax", "OC Tax Withheld", "Tax Delta", "adjustment","commission", "net_payout", "Final Payout"]]
dfframe_negativepay2.columns = ['Order Date','Order ID','Platform','Brand', 'Order Status','Subtotal','Tip','Other Amount','Processing Fee','Tax','Tax Withheld','Tax Delta','Adjustment','Commission','Expected Payout', 'Final Payout']
dfframe_pendingorders1 = df.loc[(df["Final Payout"] == 0) & (df["net_payout"] > 0) & (df["Internal ID"].notnull())]
dfframe_pendingorders2 = dfframe_pendingorders1[["Ordered Date","OC Order Display ID", "ofo_slug", "OC Brand", "order_status", "OC Subtotal", "OC Tip", "other_amount", "processing_fee", "OC Tax", "OC Tax Withheld", "Tax Delta", "adjustment","commission", "net_payout", "Final Payout"]]
dfframe_pendingorders2.columns = ['Order Date','Order ID','Platform','Brand', 'Order Status','Subtotal','Tip','Other Amount','Processing Fee','Tax','Tax Withheld','Tax Delta','Adjustment','Commission','Expected Payout', 'Final Payout']
dfframe_actualpay1 = df[["Ordered Date", "OC Order Display ID", "Brand", "Platform", "Subtotal", "Tips", "Other", "Processing Fee", "Tax", "Tax Withheld", "Promos", "Adjustment","Merchant Refund", "Commission", "net_payout","Final Payout"]]
dfframe_actualpay1.columns = ['Order Date', "Order ID", "Brand", "Platform", "Subtotal", "Tips", "Other", "Processing Fee", "Tax", "Tax Withheld", "Promos", "Adjustment","Merchant Refund", "Commission", "Expected Payout","Final Payout"]
dfframe_misccount = df.loc[df["Internal ID__1"] == "NAN"]
dfframe_misccount1 = dfframe_misccount[["Transaction Date", "Payout Date", "Payout ID", "Platform", "TransactionID", "Brand", "Final Payout"]]
dfframe_misccount1.columns = ["Transaction Date", "Payout Date", "Payout ID", "Platform", "TransactionID", "Brand", "Transaction Amount"]
dfframe_miscdebit = df.loc[(df["Internal ID__1"] == "NAN") & (df["Final Payout"] < 0)]
dfframe_miscdebit1 = dfframe_miscdebit[["Transaction Date", "Payout Date", "Payout ID", "Platform", "TransactionID", "Brand", "Final Payout"]]
dfframe_miscdebit1.columns = ["Transaction Date", "Payout Date", "Payout ID", "Platform", "TransactionID", "Brand", "Transaction Amount"]
dfframe_misccredit = df.loc[(df["Internal ID__1"] == "NAN") & (df["Final Payout"] > 0)]
dfframe_misccredit1 = dfframe_misccredit[["Transaction Date", "Payout Date", "Payout ID", "Platform", "TransactionID", "Brand", "Final Payout"]]
dfframe_misccredit1.columns = ["Transaction Date", "Payout Date", "Payout ID", "Platform", "TransactionID", "Brand", "Transaction Amount"]
#%% filter dataframe
#%%
df_exp = round(df["net_payout"].sum(), 2)
df_dexp = round(df.loc[df["ofo_slug"] == "doordash", "net_payout"].sum(), 2)
df_uexp = round(df.loc[df["ofo_slug"] == "ubereats", "net_payout"].sum(), 2)
df_gexp = round(df.loc[df["ofo_slug"] == "grubhub", "net_payout"].sum(), 2)
df_act = round(df.loc[df["Internal ID__1"] != "NAN", "Order Payout"].sum(), 2)
df_dact = round(df.loc[(df["Platform"] == "doordash") & (df["Internal ID__1"] != "NAN"), "Order Payout"].sum(), 2)
df_uact = round(df.loc[(df["Platform"] == "ubereats") & (df["Internal ID__1"] != "NAN"), "Order Payout"].sum(), 2)
df_gact = round(df.loc[(df["Platform"] == "grubhub") & (df["Internal ID__1"] != "NAN"), "Order Payout"].sum(), 2)
df_fpay = round(df["Final Payout"].sum(),2)
df_dpay = round(df.loc[df["Platform"] == "doordash", "Final Payout"].sum(), 2)
df_ufpay = round(df.loc[df["Platform"] == "ubereats", "Final Payout"].sum(), 2)
df_gfpay = round(df.loc[df["Platform"] == "gurbhub", "Final Payout"].sum(), 2)
df_torders = (df["Internal ID"].count())
df_dorder = df.loc[df["ofo_slug"] == "doordash", "Internal ID"].count()
df_uorders = df.loc[df["ofo_slug"] == "ubereats", "Internal ID"].count()
df_gorders = df.loc[df["ofo_slug"] == "grubhub", "Internal ID"].count()
df_tcancel = df.loc[df["order_status"] == "OFO_STATUS_CANCELED", "Internal ID"].count()
df_dcancel = df.loc[(df["order_status"] == "OFO_STATUS_CANCELED") & (df["ofo_slug"] == "doordash"), "Internal ID"].count()
df_ucancel = df.loc[(df["order_status"] == "OFO_STATUS_CANCELED") & (df["ofo_slug"] == "ubereats"), "Internal ID"].count()
df_gcancel = df.loc[(df["order_status"] == "OFO_STATUS_CANCELED") & (df["ofo_slug"] == "grubhub"), "Internal ID"].count() 
df_tcancelexp = round(df.loc[df["order_status"] == "OFO_STATUS_CANCELED", "net_payout"].sum(), 2)
df_dcancelexp = round(df.loc[(df["order_status"] == "OFO_STATUS_CANCELED") & (df["ofo_slug"] == "doordash"), "net_payout"].sum(), 2)
df_ucancelexp = round(df.loc[(df["order_status"] == "OFO_STATUS_CANCELED") & (df["ofo_slug"] == "ubereats"), "net_payout"].sum(), 2)
df_gcancelexp = round(df.loc[(df["order_status"] == "OFO_STATUS_CANCELED") & (df["ofo_slug"] == "grubhub"), "net_payout"].sum(), 2)
df_tcancelact = round(df.loc[df["order_status"] == "OFO_STATUS_CANCELED", "Final Payout"].sum(), 2)
df_dcancelact = round(df.loc[(df["order_status"] == "OFO_STATUS_CANCELED") & (df["Platform"] == "doordash"), "Final Payout"].sum(), 2)
df_ucancelact = round(df.loc[(df["order_status"] == "OFO_STATUS_CANCELED") & (df["Platform"] == "ubereats"), "Final Payout"].sum(), 2)
df_gcancelact = round(df.loc[(df["order_status"] == "OFO_STATUS_CANCELED") & (df["Platform"] == "grubhub"), "Final Payout"].sum(), 2)
df_tfulfilled = df.loc[df["order_status"] != "FULFILLMENT_NOT_FULFILLED", "Internal ID"].count()
df_dfulfilled = df.loc[(df["order_status"] != "FULFILLMENT_NOT_FULFILLED") & (df["ofo_slug"] == "doordash"), "Internal ID"].count()
df_ufulfilled = df.loc[(df["order_status"] != "FULFILLMENT_NOT_FULFILLED") & (df["ofo_slug"] == "ubereats"), "Internal ID"].count()
df_gfulfilled = df.loc[(df["order_status"] != "FULFILLMENT_NOT_FULFILLED") & (df["ofo_slug"] == "grubhub"), "Internal ID"].count()
df_tnfulfilled = df.loc[df["order_status"] == "FULFILLMENT_NOT_FULFILLED", "Internal ID"].count()
df_dnfulfilled = df.loc[(df["order_status"] == "FULFILLMENT_NOT_FULFILLED") & (df["ofo_slug"] == "doordash"), "Internal ID"].count()
df_unfulfilled = df.loc[(df["order_status"] == "FULFILLMENT_NOT_FULFILLED") & (df["ofo_slug"] == "ubereats"), "Internal ID"].count()
df_gnfulfilled = df.loc[(df["order_status"] == "FULFILLMENT_NOT_FULFILLED") & (df["ofo_slug"] == "grubhub"), "Internal ID"].count()
df_torderspaid = df.loc[df["Final Payout"] > 0, "Internal ID"].count()
df_dorderspaid = df.loc[(df["Final Payout"] > 0) & (df["ofo_slug"] == "doordash"), "Internal ID"].count()
df_uorderspaid = df.loc[(df["Final Payout"] > 0) & (df["ofo_slug"] == "ubereats"), "Internal ID"].count()
df_gorderspaid = df.loc[(df["Final Payout"] > 0) & (df["ofo_slug"] == "grubhub"), "Internal ID"].count()
df_torderspaidnot = df.loc[(df["net_payout"] > 0) & (df["Final Payout"] == 0), "Internal ID"].count()
df_dorderspaidnot = df.loc[(df["net_payout"] > 0) & (df["Final Payout"] == 0) & (df["ofo_slug"] == "doordash"), "Internal ID"].count()
df_uorderspaidnot = df.loc[(df["net_payout"] > 0) & (df["Final Payout"] == 0) & (df["ofo_slug"] == "ubereats"), "Internal ID"].count()
df_gorderspaidnot = df.loc[(df["net_payout"] > 0) & (df["Final Payout"] == 0) & (df["ofo_slug"] == "grubhub"), "Internal ID"].count()
#%%
df_tzeropay = df.loc[(df["Final Payout"] == 0), "Internal ID"].count()
df_dzeropay = df.loc[(df["Final Payout"] == 0) & (df["ofo_slug"] == "doordash"), "Internal ID"].count()
df_uzeropay = df.loc[(df["Final Payout"] == 0) & (df["ofo_slug"] == "ubereats"), "Internal ID"].count()
df_gzeropay = df.loc[(df["Final Payout"] == 0) & (df["ofo_slug"] == "grubhub"), "Internal ID"].count()
#%%
df_tnegativepay = df.loc[(df["Final Payout"] < 0), "Internal ID"].count()
df_dnegativepay = df.loc[(df["Final Payout"] < 0) & (df["ofo_slug"] == "doordash"), "Internal ID"].count()
df_unegativepay = df.loc[(df["Final Payout"] < 0) & (df["ofo_slug"] == "ubereats"), "Internal ID"].count()
df_gnegativepay = df.loc[(df["Final Payout"] < 0) & (df["ofo_slug"] == "grubhub"), "Internal ID"].count()
df_tnegativepaysum = round(df.loc[(df["Final Payout"] < 0) & (df["Internal ID"].notnull()), "Final Payout"].sum(), 2)
df_dnegativepaysum = round(df.loc[(df["Final Payout"] < 0) & (df["Internal ID"].notnull()) & (df["ofo_slug"] == "doordash"), "Final Payout"].sum(), 2)
df_unegativepaysum = round(df.loc[(df["Final Payout"] < 0) & (df["Internal ID"].notnull()) & (df["ofo_slug"] == "ubereats"), "Final Payout"].sum(), 2)
df_gnegativepaysum = round(df.loc[(df["Final Payout"] < 0) & (df["Internal ID"].notnull()) & (df["ofo_slug"] == "grubhub"), "Final Payout"].sum(), 2)
#%%
df_tpending = round(df.loc[(df["net_payout"] > 0) & (df["Final Payout"] == 0), "net_payout"].sum(), 2)
df_dpending = round(df.loc[(df["net_payout"] > 0) & (df["Final Payout"] == 0) & (df["ofo_slug"] == "doordash"), "net_payout"].sum(), 2)
df_upending = round(df.loc[(df["net_payout"] > 0) & (df["Final Payout"] == 0) & (df["ofo_slug"] == "ubereats"), "net_payout"].sum(), 2)
df_gpending = round(df.loc[(df["net_payout"] > 0) & (df["Final Payout"] == 0) & (df["ofo_slug"] == "grubhub"), "net_payout"].sum(), 2)
df_tcadjustments = df.loc[df["Adjustment"] < 0, "Internal ID__1"].count()
df_dcadjustments = df.loc[(df["Adjustment"] < 0) & (df["Platform"] == "doordash") & (df["Internal ID__1"] != "NAN"), "Internal ID__1"].count()
df_ucadjustments = df.loc[(df["Adjustment"] < 0) & (df["Platform"] == "ubereats") & (df["Internal ID__1"] != "NAN"), "Internal ID__1"].count()
df_gcadjustments = df.loc[(df["Adjustment"] < 0) & (df["Platform"] == "grubhub") & (df["Internal ID__1"] != "NAN"), "Internal ID__1"].count()
df_tadjustments = round(df.loc[(df["Adjustment"] < 0) & (df["Internal ID__1"] != "NAN"), "Adjustment"].sum(), 2)
df_dadjustments = round(df.loc[(df["Adjustment"] < 0) &  (df["Platform"] == "doordash") & (df["Internal ID__1"] != "NAN"), "Adjustment"].sum(), 2)
df_uadjustments = round(df.loc[(df["Adjustment"] < 0) & (df["Platform"] == "ubereats") & (df["Internal ID__1"] != "NAN"), "Adjustment"].sum(), 2)
df_gadjustments = round(df.loc[(df["Adjustment"] < 0) & (df["Platform"] == "grubhub") & (df["Internal ID__1"] != "NAN"), "Adjustment"].sum(), 2)
#%%
df_tcrefund = df.loc[(df["Merchant Refund"] >0) & (df["Internal ID__1"] != "NAN"), "Internal ID__1"].count()
#%%
df_dcrefund = df.loc[(df["Merchant Refund"] >0) & (df["Internal ID__1"] != "NAN") & (df["Platform"] == "doordash"), "Internal ID__1"].count()
df_ucrefund = df.loc[(df["Merchant Refund"] >0) & (df["Internal ID__1"] != "NAN") & (df["Platform"] == "ubereats"), "Internal ID__1"].count()
df_gcrefund = df.loc[(df["Merchant Refund"] >0) & (df["Internal ID__1"] != "NAN") & (df["Platform"] == "grubhub"), "Internal ID__1"].count()
df_trefund = round(df.loc[(df["Merchant Refund"] >0) & (df["Internal ID__1"] != "NAN"), "Final Payout"].sum(), 2)
df_drefund = round(df.loc[(df["Merchant Refund"] >0) & (df["Internal ID__1"] != "NAN") & (df["Platform"] == "doordash"), "Final Payout"].sum(), 2)
df_urefund = round(df.loc[(df["Merchant Refund"] >0) & (df["Internal ID__1"] != "NAN") & (df["Platform"] == "ubereats"), "Final Payout"].sum(), 2)
df_grefund = round(df.loc[(df["Merchant Refund"] >0) & (df["Internal ID__1"] != "NAN") & (df["Platform"] == "grubhub"), "Final Payout"].sum(), 2)
df_delta = round(df_act - df_exp, 2)
df_fdelta = round(df_fpay - df_exp, 2)
#%%
df_tcmisc = df.loc[df["Internal ID__1"] == "NAN" , "Internal ID__1"].count()
df_dcmisc = df.loc[(df["Internal ID__1"] == "NAN") & (df["Platform"] == "doordash"), "Internal ID__1"].count()
df_ucmisc = df.loc[(df["Internal ID__1"] == "NAN") & (df["Platform"] == "ubereats"), "Internal ID__1"].count()
df_gcmisc = df.loc[(df["Internal ID__1"] == "NAN") & (df["Platform"] == "grubhub"), "Internal ID__1"].count()
#%%
df_tmisc = round(df.loc[df["Internal ID__1"] == "NAN", "Final Payout"].sum(), 2)
df_dmisc = round(df.loc[(df["Internal ID__1"] == "NAN") & (df["Platform"] == "doordash"), "Final Payout"].sum(), 2)
df_umisc = round(df.loc[(df["Internal ID__1"] == "NAN") & (df["Platform"] == "ubereats"), "Final Payout"].sum(), 2)
df_gmisc = round(df.loc[(df["Internal ID__1"] == "NAN") & (df["Platform"] == "grubhub"), "Final Payout"].sum(), 2)
df_tdebit = round(df.loc[(df["Internal ID__1"] == "NAN") & (df["Final Payout"] < 0), "Final Payout"].sum(), 2)
df_ddebit = round(df.loc[(df["Internal ID__1"] == "NAN") & (df["Platform"] == "doordash") & (df["Final Payout"] < 0),"Final Payout"].sum(), 2)
df_udebit = round(df.loc[(df["Internal ID__1"] == "NAN") & (df["Platform"] == "ubereats") & (df["Final Payout"] < 0), "Final Payout"].sum(), 2)
df_gdebit = round(df.loc[(df["Internal ID__1"] == "NAN") & (df["Platform"] == "grubhub") & (df["Final Payout"] < 0), "Final Payout"].sum(), 2)
df_tcredit = round(df.loc[(df["Internal ID__1"] == "NAN") & (df["Final Payout"] > 0), "Final Payout"].sum(), 2)
df_dcredit = round(df.loc[(df["Internal ID__1"] == "NAN") & (df["Platform"] == "doordash") & (df["Final Payout"] > 0), "Final Payout"].sum(), 2)
df_ucredit = round(df.loc[(df["Internal ID__1"] == "NAN") & (df["Platform"] == "ubereats") & (df["Final Payout"] > 0), "Final Payout"].sum(), 2)
df_gcredit = round(df.loc[(df["Internal ID__1"] == "NAN") & (df["Platform"] == "grubhub") & (df["Final Payout"] > 0), "Final Payout"].sum(), 2)
#%%
m1, m2, m3, m4, m5, m6, m7 = st.columns([1,1,5,5,5,1,1], gap ="large")
m3.metric("Expected Order Payout", "${:,}".format(df_exp), help = "Sum of order payout collected at the time of the order")
m4.metric("Actual Order Payout", "${:,}".format(df_act), "${:,}".format(df_delta), help = "Comparison of order payouts without adjustments and refunds with expected payout")
m5.metric("Final Payout","${:,}".format(df_fpay),"${:,}".format(df_fdelta), help = "Comparison of payouts after adjustments and refunds with expected payout")
# %% Summary Block for count
n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,1.2,1,1,1.2,1,1])
with n3:
    st.write("Total Orders Received")
with n4:
    st.subheader(df_torders)
with n5:
    check = st.checkbox('Partners', key = 'dtfygubhjkn', help = "Includes orders later canceled.")
with n6:
    st.write("Total Orders Canceled")
with n7:
    st.subheader(df_tcancel)
with n8:
    if df_tcancel / df_torders > 0.1:
        cautionicon = st.write("⚠️")
        check1 = st.checkbox("Partners", key = 'rdtcfyvgubhijlkn')
    else:
        check1 = st.checkbox("Partners", key = 'rdtcfyvgubhijlkn')
if check and check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dorder, df_uorders, df_gorders]})
            st.dataframe(ofodf)
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dcancel, df_ucancel, df_gcancel]})
            st.dataframe(ofodf)
    with n5:
            check11 = st.checkbox ("Details", key = 'receiveddetailscombined')
    with n8:
            check22 = st.checkbox ("Details", key ='canceleddetailscombined')
    if check11 and check22:
        st.markdown("Total Orders Received") 
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="receivedfiltercombined")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"], label_visibility='hidden')
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe1
        st.dataframe(filter_dataframe(dfx))
        st.markdown("Canceled Orders")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="canceledfiltercombined")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"], label_visibility='hidden')
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_canceled2    
        st.dataframe(filter_dataframe(dfx))
    elif check11:
        st.markdown("Total Orders Received") 
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="receivedfiltercombined")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"], label_visibility='hidden')
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe1
        st.dataframe(filter_dataframe(dfx))
    elif check22: 
        st.markdown("Canceled Orders")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="canceledfiltercombined")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"], label_visibility='hidden')
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_canceled2    
        st.dataframe(filter_dataframe(dfx))

elif check:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dorder, df_uorders, df_gorders]})
            st.dataframe(ofodf)
    with n5:
            #textbox = st.checkbox("Orders", key = "seetorders")
            check11 = st.checkbox("Details", key = 'receiveddetails')
    if check11:
                st.markdown("Total Orders Received") 
                def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                    modify =st.checkbox("Filter Platforms", key ="receivedfilter")
                    if not modify:
                        return dfx

                    dfx = dfx.copy()

                    for col in dfx.columns:
                        if is_object_dtype(dfx[col]):
                            try:
                                dfx[col] = pd.to_datetime(dfx[col])
                            except Exception:
                                pass
                        if is_datetime64_any_dtype (dfx[col]):
                            dfx[col] = dfx[col].dt.tz_localize(None)
                    modification_container = st.container()
                    with modification_container:
                        to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"], label_visibility='hidden')
                        for column in to_filter_columns:
                            left, right =st.columns((1,20))
                            left.write("↳")
                            if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                                user_cat_input = right.multiselect(
                                    f"Values for {column}",
                                    dfx[column].unique(),
                                    default = list(dfx[column].unique())
                                )
                                dfx = dfx[dfx[column].isin(user_cat_input)]
                            else:
                                user_text_input = right.text_input(
                                    f"{column}",
                                )   
                                if user_text_input:
                                    dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                    return dfx
                dfx = dfframe1
                st.dataframe(filter_dataframe (dfx))
elif check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dcancel, df_ucancel, df_gcancel]})
            st.dataframe(ofodf)
    with n8:
            check22 = st.checkbox ("Details", key = 'canceleddetails')
    if check22:
                st.markdown("Canceled Orders")
                def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                    modify =st.checkbox("Filter Platforms", key ="canceledfilter")
                    if not modify:
                        return dfx

                    dfx = dfx.copy()

                    for col in dfx.columns:
                        if is_object_dtype(dfx[col]):
                            try:
                                dfx[col] = pd.to_datetime(dfx[col])
                            except Exception:
                                pass
                        if is_datetime64_any_dtype (dfx[col]):
                            dfx[col] = dfx[col].dt.tz_localize(None)
                    modification_container = st.container()
                    with modification_container:
                        to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"], label_visibility='hidden')
                        for column in to_filter_columns:
                            left, right =st.columns((1,20))
                            left.write("↳")
                            if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                                user_cat_input = right.multiselect(
                                    f"Values for {column}",
                                    dfx[column].unique(),
                                    default = list(dfx[column].unique())
                                )
                                dfx = dfx[dfx[column].isin(user_cat_input)]
                            else:
                                user_text_input = right.text_input(
                                    f"{column}",
                                )   
                                if user_text_input:
                                    dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                    return dfx
                dfx = dfframe_canceled2
                st.dataframe(filter_dataframe (dfx))
            

#%% summary block for sum
n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,1.2,1,1,1.2,1,1])
with n3:
    st.write("Canceled Orders - Expected Payout")
with n4:
    st.subheader("${:,}".format(df_tcancelexp))
with n5:
    check = st.checkbox('Partners', key = 'cancel_exp')
with n6:
    st.write("Canceled Order - Actual Payout")
with n7:
    st.subheader("${:,}".format(df_tcancelact))
with n8:
    check1 = st.checkbox("Partners", key = 'cancel_act', help = 'Note: Certain delivery platforms may credit orders despite cancelations as contingent with their guidelines.')
if check and check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dcancelexp, df_ucancelexp, df_gcancelexp]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dcancelact, df_ucancelact, df_gcancelact]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n5:
            check11 = st.checkbox ("Details", key = 'canceledexpectedcombined')
    with n8:
            check22 = st.checkbox ("Details", key ='canceledactualcombined')
    if check11 and check22:
        st.markdown("Canceled Orders Expected Payout") 
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="cancelexecptedpayoutcombined")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"], label_visibility='hidden')
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_canceled2
        st.dataframe(filter_dataframe(dfx))
        st.markdown("Canceled Orders Actual Payout")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="canceledactualpayoutcombined")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"], label_visibility='hidden')
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_canceledactpayout   
        st.dataframe(filter_dataframe(dfx))
    elif check11:
        st.markdown("Canceled Orders Expected Payout") 
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="cancelexpectedpayoutcombined2")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"], label_visibility='hidden')
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_canceled2
        st.dataframe(filter_dataframe(dfx))
    elif check22:
        st.markdown("Canceled Orders Actual Payout")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="canceledactuaasdffiltercombined")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"], label_visibility='hidden')
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_canceledactpayout    
        st.dataframe(filter_dataframe(dfx))
elif check:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dcancelexp, df_ucancelexp, df_gcancelexp]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n5:
            check11 = st.checkbox("Details", key = 'canceledexpectedbox')
    if check11:
            st.markdown("Canceled Orders Expected Payout") 
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="cancelexpectedpayout2")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"], label_visibility='hidden')
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe_canceled2
            st.dataframe(filter_dataframe(dfx))
elif check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dcancelact, df_ucancelact, df_gcancelact]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n8:
            check22 = st.checkbox ("Details", key = 'canceledactualpayoutcheckbox2')
    if check22: 
            st.markdown("Canceled Orders Actual Payout")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                    modify =st.checkbox("Filter Platforms", key ="canceledactualpayoutfilter2")
                    if not modify:
                        return dfx

                    dfx = dfx.copy()

                    for col in dfx.columns:
                        if is_object_dtype(dfx[col]):
                            try:
                                dfx[col] = pd.to_datetime(dfx[col])
                            except Exception:
                                pass
                        if is_datetime64_any_dtype (dfx[col]):
                            dfx[col] = dfx[col].dt.tz_localize(None)
                    modification_container = st.container()
                    with modification_container:
                        to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"], label_visibility='hidden')
                        for column in to_filter_columns:
                            left, right =st.columns((1,20))
                            left.write("↳")
                            if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                                user_cat_input = right.multiselect(
                                    f"Values for {column}",
                                    dfx[column].unique(),
                                    default = list(dfx[column].unique())
                                )
                                dfx = dfx[dfx[column].isin(user_cat_input)]
                            else:
                                user_text_input = right.text_input(
                                    f"{column}",
                                )   
                                if user_text_input:
                                    dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                    return dfx
            dfx = dfframe_canceledactpayout
            st.dataframe(filter_dataframe (dfx))
#Orders paid vs not paid
n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,1.2,1,1,1.2,1,1])
with n3:
    st.write("Total Orders Paid")
with n4:
    st.subheader(df_torderspaid)
with n5:
    check = st.checkbox('Partners', key = 'orderpaid')
with n6:
    st.write("Total Order with No Payment")
with n7:
    st.subheader(df_tzeropay)
with n8:
    if df_tzeropay > 0:
        cautionicon =st.write("⚠️")
        check1 = st.checkbox("Partners", key = 'tzeropay', help = "Recorded orders with no recorded payout or with '$0' in payout")
    else:
        check1 = st.checkbox("Partners", key = 'tzeropay', help = "Recorded orders with no recorded payout or with '$0' in payout")
if check and check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dorderspaid, df_uorderspaid, df_gorderspaid]})
            st.dataframe(ofodf)
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dzeropay, df_uzeropay, df_gzeropay]})
            st.dataframe(ofodf)
    with n5:
            check11 = st.checkbox ("Details", key = 'Totalorderspaidcombined1')
    with n8:
            check22 = st.checkbox ("Details", key ='Totalorderszeropaidcombined1')
    if check11 and check22:
        st.markdown("Total Orders Paid")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="totalorderpaidcombined2")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_orderspaid2
        st.dataframe(filter_dataframe(dfx))
        st.markdown("Total Order with No Payment")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="totalordersnotpaidcombined2")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_ordernotpaid2
        st.dataframe(filter_dataframe(dfx))
    elif check11:
        st.markdown("Total Orders Paid")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="totalorderpaidcombined3")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_orderspaid2
        st.dataframe(filter_dataframe(dfx))
    elif check22:
        st.markdown("Total Order with No Payment")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="totalordersnotpaidcombined3")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_ordernotpaid2
        st.dataframe(filter_dataframe(dfx))

elif check:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dorderspaid, df_uorderspaid, df_gorderspaid]})
            st.dataframe(ofodf)
    with n5:
            check11 = st.checkbox("Details", key = 'paidorderscheckbox1')
    if check11:
        st.markdown("Total Orders Paid")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="totalorderpaidcombined4")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_orderspaid2
        st.dataframe(filter_dataframe(dfx))
elif check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dzeropay, df_uzeropay, df_gzeropay]})
            st.dataframe(ofodf)
    with n8:
        check22 = st.checkbox ("Details", key = 'orderswithzeropayoutcheckbox1')
    if check22:
        st.markdown("Total Order with No Payment")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="totalordersnotpaidcombined4")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_ordernotpaid2
        st.dataframe(filter_dataframe(dfx))
#Negative payout count vs negative payout sum
n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,1.2,1,1,1.2,1,1])
with n3:
    st.write("Total Orders with Negative Payout")
with n4:
    st.subheader((df_tnegativepay))
with n5:
    check = st.checkbox('Partners', key = 'negativepay')
with n6:
    st.write("Sum of Negative Payout")
with n7:
    st.subheader("${:,}".format(df_tnegativepaysum))
with n8:
    if df_tnegativepaysum < 0:
        cautionicon = st.write("⚠️")
        check1 = st.checkbox("Partners", key = 'negativepaysum', help = "Orders with negative net pay")
    else:
        check1 = st.checkbox("Partners", key = 'negativepaysum', help = "Orders with negative net pay")
if check and check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dnegativepay, df_unegativepay, df_gnegativepay]})
            st.dataframe(ofodf)
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dnegativepaysum, df_unegativepaysum, df_gnegativepaysum]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n5:
            check11 = st.checkbox ("Details", key = 'countofnegativepayorders1')
    with n8:
            check22 = st.checkbox ("Details", key ='sumofnegativepayorders1')
    if check11 and check22: 
        st.markdown("Total Orders with Negative Payout")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="totalorderswithnegativepay1")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_negativepay2
        st.dataframe(filter_dataframe(dfx))
    elif check11:
            st.markdown("Total Orders with Negative Payout")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="totalorderswithnegativepay2")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe_negativepay2
            st.dataframe(filter_dataframe(dfx)) 
    elif check22:
            st.markdown("Total Orders with Negative Payout")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="totalorderswithnegativepay3")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe_negativepay2
            st.dataframe(filter_dataframe(dfx)) 
elif check:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dnegativepay, df_unegativepay, df_gnegativepay]})
            st.dataframe(ofodf)
    with n5:
            check11 = st.checkbox ("Details", key = 'countofnegativepayorders2')
    if check11:
            st.markdown("Total Orders with Negative Payout")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="totalorderswithnegativepay4")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe_negativepay2
            st.dataframe(filter_dataframe(dfx)) 
elif check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dnegativepaysum, df_unegativepaysum, df_gnegativepaysum]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n8:
            check22 = st.checkbox ("Details", key ='sumofnegativepayorders2')
    if check22:
            st.markdown("Orders with Negative Payout")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="totalorderswithnegativepay5")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe_negativepay2
            st.dataframe(filter_dataframe(dfx)) 
#Pending order count vs Pending Order sum
n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,1.2,1,1,1.2,1,1])
with n3:
    st.write("Total Orders Pending Payment")
with n4:
    st.subheader((df_torderspaidnot))
with n5:
    check = st.checkbox('Partners', key = 'countoforderspending')
with n6:
    st.write("Sum of Pending Payment")
with n7:
    st.subheader("${:,}".format(df_tpending))
with n8:
    if df_tpending > 0:
        cautionicon = st.write("⚠️")
        check1 = st.checkbox("Partners", key = 'sumoforderspending', help = "Orders with expecting payout missing actual payout")
    else:
        check1 = st.checkbox("Partners", key = 'sumoforderspending', help = "Orders with expecting payout missing actual payout")
if check and check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dorderspaidnot, df_uorderspaidnot, df_gorderspaidnot]})
            st.dataframe(ofodf)
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dpending, df_upending, df_gpending]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n5:
            check11 = st.checkbox("Details", key = "countoforderspendingcheckbox")
    with n8:
            check22 = st.checkbox("Details", key = "sumoforderspendingcheckbox")
    if check11 and check22:
        st.markdown("Total Orders pending")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="countoforderspending1")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_pendingorders2
        st.dataframe(filter_dataframe(dfx))
        st.markdown("Sum of Pending Payment")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="sumoforderspending1")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_pendingorders2
        st.dataframe(filter_dataframe(dfx))
    elif check11:
        st.markdown("Total Orders pending")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="countoforderspending2")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_pendingorders2
        st.dataframe(filter_dataframe(dfx))
    elif check22:
        st.markdown("Sum of Pending Payment")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="sumoforderspending2")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_pendingorders2
        st.dataframe(filter_dataframe(dfx))
elif check:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dorderspaidnot, df_uorderspaidnot, df_gorderspaidnot]})
            st.dataframe(ofodf)
    with n5:
            check11 = st.checkbox("Details", key = "countoforderspendingcheckbox2")
    if check11: 
            st.markdown("Total Orders pending")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="countoforderspending3")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe_pendingorders2
            st.dataframe(filter_dataframe(dfx))
elif check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dpending, df_upending, df_gpending]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n8:
            check22 = st.checkbox("Details", key = "sumoforderspendingcheckbox2")
    if check22: 
            st.markdown("Sum of Pending Payment")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="sumoforderspending3")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe_pendingorders2
            st.dataframe(filter_dataframe(dfx))
#Expected vs Actual
n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,1.2,1,1,1.2,1,1])
with n3:
    st.write("Total - Estimated Payout")
with n4:
    st.subheader("${:,}".format(df_exp))
with n5:
    check = st.checkbox('Partners', key = 'estimatedpayout', help = "Estimated Payout is defined as the sum of order payouts collected at the time of the orders")
with n6:
    st.write("Total - Actual Payout")
with n7:
    st.subheader("${:,}".format(df_act))
with n8:
    if df_act < df_exp:
        cautionicon = st.write("⚠️")
        check1 = st.checkbox("Partners", key = 'actualpayout', help = "Final net deposit of orders, it is normal for this amount to be higher than Estimated Payout")
    else:
        check1 = st.checkbox("Partners", key = 'actualpayout', help = "Final net deposit of orders, it is normal for this amount to be higher than Estimated Payout")
if check and check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dexp, df_uexp, df_gexp]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dact, df_uact, df_gact]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n5:
            check11 = st.checkbox ("Details", key = 'totalexpectedpayoutcheckbox1')
    with n8:
            check22 = st.checkbox ("Details", key = 'totalactualpayoutcheckbox2')
    if check11 and check22:
            st.markdown("Orders Contributing to Expected Payout")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="expectedpayoutcombined1")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe1
            st.dataframe(filter_dataframe(dfx))
            st.markdown("Orders Contributing to Actual Payout")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="expectedpayoutcombined1")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = (dfframe_actualpay1)
            st.dataframe(filter_dataframe(dfx))
    elif check11:
            st.markdown("Orders Contributing to Expected Payout")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="expectedpayoutcombined2")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe1
            st.dataframe(filter_dataframe(dfx))    
    elif check22:
            st.markdown("Orders Contributing to Actual Payout")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="expectedpayoutcombined2")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = (dfframe_actualpay1)
            st.dataframe(filter_dataframe(dfx))
elif check:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dexp, df_uexp, df_gexp]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n5:
            check11 = st.checkbox("Details", key = "expectedpayoutcheckbox2")
    if check11:
            st.markdown("Orders Contributing to Expected Payout")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="expectedpayoutcombined3")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe1
            st.dataframe(filter_dataframe(dfx))
elif check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dact, df_uact, df_gact]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n8:
            check22 = st.checkbox("Details", key = "actualpayoutcheckbox2")
    if check22:
            st.markdown("Orders Contributing to Actual Payout")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="expectedpayoutcombined3")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = (dfframe_actualpay1)
            st.dataframe(filter_dataframe(dfx))
# count adjustments vs paid adjustment
n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,1.2,1,1,1.2,1,1])
with n3:
    st.write("Total Orders with Charges")
with n4:
    st.subheader(df_tcadjustments)
with n5:
    check = st.checkbox('Partners', key = 'adjustmentcount')
with n6:
    st.write("Sum of Charges")
with n7:
    st.subheader("${:,}".format(df_tadjustments))
with n8:
    check1 = st.checkbox("Partners", key = 'adjustmentsum')
if check and check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dcadjustments, df_ucadjustments, df_gcadjustments]})
            st.dataframe(ofodf)
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dadjustments, df_uadjustments, df_gadjustments]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n5:
            st.markdown("[Jump](#test)")
    with n8:
            st.markdown("[Jump](#test)")
elif check:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dcadjustments, df_ucadjustments, df_gcadjustments]})
            st.dataframe(ofodf)
    with n5:
            st.markdown("[Jump](#test)")
elif check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dadjustments, df_uadjustments, df_gadjustments]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n8:
            st.markdown("[Jump](#test)")
#count of refunds vs refunds
n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,1.2,1,1,1.2,1,1])
with n3:
    st.write("Total Orders with Merchant Refunds")
with n4:
    st.subheader(df_tcrefund)
with n5:
    check = st.checkbox('Partners', key = 'refundcount', help='Note: Some Partners may display merchant refunds as a lumpsum which are exluded from this count.')
with n6:
    st.write("Sum of Merchant Refunds")
with n7:
    st.subheader("${:,}".format(df_trefund))
with n8:
    check1 = st.checkbox("Partners", key = 'refundsum', help='Note: Some Partners may display merchant refunds as a lumpsum which are exluded from this sum.')
if check and check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dcrefund, df_ucrefund, df_gcrefund]})
            st.dataframe(ofodf)
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_drefund, df_urefund, df_grefund]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n5:
            st.markdown("[Jump](#test)")
    with n8:
            st.markdown("[Jump](#test)")
elif check:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dcrefund, df_ucrefund, df_gcrefund]})
            st.dataframe(ofodf)
    with n5:
            st.markdown("[Jump](#test)")
elif check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_drefund, df_urefund, df_grefund]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n8:
            st.markdown("[Jump](#test)")
# count of misc transactions vs sum 
n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,1.2,1,1,1.2,1,1])
with n3:
    st.write("Total Misc. Transactions")
with n4:
    st.subheader(df_tcmisc)
with n5:
    check = st.checkbox('Partners', key = 'misccount', help='Misc. Transactions: Transactions without any order details.')
with n6:
    st.write("Sum of Misc. Transactions")
with n7:
    st.subheader("${:,}".format(df_tmisc))
with n8:
    check1 = st.checkbox("Partners", key = 'miscsum', help='Misc. Transactions: Transactions without any order details.')
if check and check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dcmisc, df_ucmisc, df_gcmisc]})
            st.dataframe(ofodf)
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dmisc, df_umisc, df_gmisc]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n5:
            check11 = st.checkbox ("Details", Key = 'countofamisctranscheckbox1')
    with n8:
            check22 = st.checkbox ("Details", Key = 'sumofamisctranscheckbox1')
    if check11 and check22:
            st.markdown("Misc Transactions")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="misctrqansactionscount1")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe_misccount1
            st.dataframe(filter_dataframe(dfx))
    elif check11:
            st.markdown("Misc. Transactions")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="misctransactionscount2")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe_misccount1
            st.dataframe(filter_dataframe(dfx))
    elif check22:
            st.markdown("Misc. Transactions")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="misctransactionscount3")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe_misccount1
            st.dataframe(filter_dataframe(dfx))
elif check:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Count': [df_dcmisc, df_ucmisc, df_gcmisc]})
            st.dataframe(ofodf)
    with n5:
            check11 = st.checkbox("Details", key = "misctransactioncountcheckbox2")
    if check11:
            st.markdown("Misc. Transactions")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="misctransactionscount4")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe_misccount1
            st.dataframe(filter_dataframe(dfx))
elif check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dmisc, df_umisc, df_gmisc]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n8:
            check22 = st.checkbox("Details", key = "mistransactinocountcheckbox3")
    if check22: 
            st.markdown("Misc. Transactions")
            def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
                modify =st.checkbox("Filter Platforms", key ="misctransactionscount5")
                if not modify:
                    return dfx

                dfx = dfx.copy()

                for col in dfx.columns:
                    if is_object_dtype(dfx[col]):
                        try:
                            dfx[col] = pd.to_datetime(dfx[col])
                        except Exception:
                            pass
                    if is_datetime64_any_dtype (dfx[col]):
                        dfx[col] = dfx[col].dt.tz_localize(None)
                modification_container = st.container()
                with modification_container:
                    to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                    for column in to_filter_columns:
                        left, right =st.columns((1,20))
                        left.write("↳")
                        if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                            user_cat_input = right.multiselect(
                                f"Values for {column}",
                                dfx[column].unique(),
                                default = list(dfx[column].unique())
                            )
                            dfx = dfx[dfx[column].isin(user_cat_input)]
                        else:
                            user_text_input = right.text_input(
                                f"{column}",
                            )   
                            if user_text_input:
                                dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
                return dfx
            dfx = dfframe_misccount1
            st.dataframe(filter_dataframe(dfx))
#%%debit vs credit
n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,1.2,1,1,1.2,1,1])
with n3:
    st.write("Misc. Transactions - Debit  ")
with n4:
    st.subheader("${:,}".format(df_tdebit))
with n5:
    st.write("⚠️")
    check = st.checkbox('Partners ', key = 'miscdebit')
with n6:
    st.write("Misc. Transactions - Credit")
with n7:
    st.subheader("${:,}".format(df_tcredit))
with n8:
    if df_tcredit > 0:
        #test = '<p style="font-family:Sans serif; color:red; font-size: 20x; font-weight: bold; font-style:italic;">Warning</p>'
        #warningicon = st.write("⚠️")
        check1 = st.checkbox("Platform", key = 'misccredit')
    else:
        check1 = st.checkbox("Partners", key = 'misccredit')
if check and check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_ddebit, df_udebit, df_gdebit]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dcredit, df_ucredit, df_gcredit]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n5:
            check11 = st.checkbox("Details", key = "misctransactiondebitcheckbox1")
    with n8:
            check22 = st.checkbox("Details", key = "misctransactioncreditcheckbox1")
    if check11 and check22: 
        st.markdown("Misc. Transactions - Debit")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="misdebit1")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_miscdebit1
        st.dataframe(filter_dataframe(dfx))
        st.markdown("Misc. Transactions - Credit")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="misccredit1")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_misccredit1
        st.dataframe(filter_dataframe(dfx))
    elif check11:
        st.markdown("Misc. Transactions - Debit")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="misdebit2")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_miscdebit1
        st.dataframe(filter_dataframe(dfx))
    elif check22:
        st.markdown("Misc. Transactions - Credit")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="misccredit2")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_misccredit1
        st.dataframe(filter_dataframe(dfx))

elif check:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n4:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_ddebit, df_udebit, df_gdebit]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n5:
            check11 = st.checkbox("Details", key = "misctransactiondebitcheckbox2")
    if check11: 
        st.markdown("Misc. Transactions - Debit")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="misdebit3")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_miscdebit1
        st.dataframe(filter_dataframe(dfx))
elif check1:
    n1, n2, n3, n4, n5, n6, n7, n8, n9 = st.columns([1,1,1,2,1,1,2,1,1])
    with n7:
            ofodf =pd.DataFrame({'Partners': ["Doordash", "UberEats","Grubhub"], 'Order Payout': [df_dcredit, df_ucredit, df_gcredit]})
            st.dataframe(ofodf.style.format({'Order Payout': '${:,.2f}'}))
    with n8:
            check22 = st.checkbox("Details", key = "misctransactioncreditcheckbox2")
    if check22: 
        st.markdown("Misc. Transactions - Credit")
        def filter_dataframe(dfx: pd.DataFrame) -> pd.DataFrame:
            modify =st.checkbox("Filter Platforms", key ="misccredit3")
            if not modify:
                return dfx

            dfx = dfx.copy()

            for col in dfx.columns:
                if is_object_dtype(dfx[col]):
                    try:
                        dfx[col] = pd.to_datetime(dfx[col])
                    except Exception:
                        pass
                if is_datetime64_any_dtype (dfx[col]):
                    dfx[col] = dfx[col].dt.tz_localize(None)
            modification_container = st.container()
            with modification_container:
                to_filter_columns = st.multiselect("Filter dataframe on", ["Platform"])
                for column in to_filter_columns:
                    left, right =st.columns((1,20))
                    left.write("↳")
                    if is_categorical_dtype(dfx[column]) or dfx[column].nunique() < 10:
                        user_cat_input = right.multiselect(
                            f"Values for {column}",
                            dfx[column].unique(),
                            default = list(dfx[column].unique())
                        )
                        dfx = dfx[dfx[column].isin(user_cat_input)]
                    else:
                        user_text_input = right.text_input(
                            f"{column}",
                        )   
                        if user_text_input:
                            dfx = dfx[dfx[column].astype(str).str.contains(user_text_input)]
            return dfx
        dfx = dfframe_misccredit1
        st.dataframe(filter_dataframe(dfx))

# %%

# %%

# %%

# %%