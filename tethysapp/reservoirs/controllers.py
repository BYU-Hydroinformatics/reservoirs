from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button
import pywaterml.waterML as pwml
from django.http import JsonResponse, HttpResponse
from tethys_sdk.workspaces import app_workspace
from django.shortcuts import render
from tethys_sdk.gizmos import SelectInput, RangeSlider
from tethys_sdk.permissions import login_required
import numpy as np
import json
from tethys_sdk.routing import controller
import os
import numpy as np
import json
import pandas as pd
import requests
import geoglows
import datetime
from datetime import date
from datetime import timedelta
from scipy import integrate
from .auxiliary import *
from .app import Reservoirs as app

BASE_URL = app.get_custom_setting('Hydroser_Endpoint')
@login_required()

@controller(name='home', url='reservoirs')
def home(request):

    """
    Controller for the app home page.
    """

    url_request_base = 'http://ec2-18-204-193-247.compute-1.amazonaws.com:5000/API'

    response = requests.get(f'{url_request_base}/stations')
    stations_dict = response.json()
    df = pd.DataFrame.from_dict(stations_dict)

    try:
        sites_name = [('None', 0)]
        for index, row in df.iterrows():
            if 'Presa' in row['Station']:
                info = row['Station'], row['StationName']
                sites_name.append(info)

        variables = SelectInput(
            display_text='',
            name='variables',
            multiple=False,
            original=True,
            options=tuple(sites_name)
        )

        context = {
            'variables': variables,
        }
        return render(request, 'reservoirs/home.html', context)

    except Exception as e:
        print(e)
        variables = SelectInput(
            display_text='Select a Reservoir',
            name='variables',
            multiple=False,
            original=True,
            options=tuple([])
        )

        context = {
            'variables': variables,
        }
        return render(request, 'reservoirs/home.html', context)



@controller(name='GetSites', url='reservoirs/GetSites', app_workspace=True)
def GetSites(request, app_workspace):

    aw_path=app_workspace.path
    url_request_base = 'http://ec2-18-204-193-247.compute-1.amazonaws.com:5000/API'

    response = requests.get(f'{url_request_base}/stations')
    response2 = requests.get(f'{url_request_base}/availability')
    availability_dict = response2.json()
    stations_dict = response.json()
    df = pd.DataFrame.from_dict(stations_dict)
    df2 = pd.DataFrame.from_dict(availability_dict)
    return_object = {}

    sites_info = [('None', 'none', 0, 0, 0, 0)]
    # list of longitude and latitude of stations
    for index, row in df.iterrows():
        for index, row2 in df2.iterrows():
            if 'Presa' in row['Station']:
                if row['Station'] in row2['Station']:
                    info1 = row['Station'], row['StationName'], row['Latitude2'], row['Longitude2'], row2['StrtDate'], row2['EndDate']
                    sites_info.append(info1)
    return_object['siteInfo'] = sites_info
    return JsonResponse(return_object)

# def getMonthlyAverage(request):
#
#     url = "http://128.187.106.131/app/index.php/dr/services/cuahsi_1_1.asmx?WSDL"
#     water = pwml.WaterMLOperations(url=url)
#     m_avg = water.GetMonthlyAverage(None, site_full_code, variable_full_code, start_date, end_date)
#
#     data = {'Months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
#             'Monthly Average': m_avg,
#             }
#     return_object = pd.DataFrame(data, columns=['Months', 'Monthly Average'])
#
#     return JsonResponse(return_object)
#
#
# def getTimeSeries(request):
#
#     return_object = {}
#     url = "http://128.187.106.131/app/index.php/dr/services/cuahsi_1_1.asmx?WSDL"
#     water = pwml.WaterMLOperations(url=url)
#     sites = water.GetSites()
def GetInfoReal(request):
    return_object = {}
#no changes made to this, I don't think I need it
    fullsitecode = request.GET.get("full_code")
    site_name = request.GET.get("site_name")
    # myvalues = []
    # url = "http://128.187.106.131/app/index.php/dr/services/cuahsi_1_1.asmx?WSDL"
    water = pwml.WaterMLOperations(url=BASE_URL)

    info_site = water.GetInfo(fullsitecode)

    return_object['siteInfo'] = info_site

    return JsonResponse(return_object)

@controller(name='GetInfo', url='reservoirs/GetInfo', app_workspace = True)
def GetInfo(request, app_workspace):
    return_object = {}
    try:

        url_request_base = 'http://ec2-18-204-193-247.compute-1.amazonaws.com:5000/API'
        response = requests.get(f'{url_request_base}/stations')
        response2 = requests.get(f'{url_request_base}/availability')
        stations_dict = response.json()
        availability_dict = response2.json()
        df2 = pd.DataFrame.from_dict(availability_dict)
        df = pd.DataFrame.from_dict(stations_dict)

        fullsitecode = request.GET.get("full_code")
        stn_id = request.GET.get("site_name")
        var_id = 'Level4'

        df_new = df2[df2['Station'].isin([stn_id])]
        df_new2 = df[df['Station'].isin([stn_id])]
        min_val = df_new2['MinLevelSta'].tolist()[0]
        max_val = df_new2['MaxLevelSta'].tolist()[0]

        date_ini = df_new['StrtDate'].tolist()[0]
        date_end = df_new['EndDate'].tolist()[0]

        response = requests.get(
            f'{url_request_base}/data/dailydata?stn_id={stn_id}&var_id={var_id}&date_ini={date_ini}&date_end={date_end}')  # Make a GET request to the URL

        # Print status code (and associated text)
        # Print data returned (parsing as JSON)
        dailydata_dict = response.json()
        # Parse `response.text` into JSON
        df = pd.DataFrame.from_dict(dailydata_dict)

        x_values = []
        y_values = []

        for index, row in df.iterrows():
            x_values.append(row['Date'])
            y_values.append(row['Value'])

        recent_val = y_values[-1]
        recent_date = x_values[-1]

        start_date = min(x_values)
        end_date = max(x_values)

        return_object['stn_id']=stn_id
        return_object['station']=fullsitecode
        return_object['var_id']=var_id
        return_object['min_level']=min_val
        return_object['max_level'] = max_val
        return_object['start_date']=start_date
        return_object['end_date'] = end_date
        return_object['recent_val'] = recent_val
        return_object['recent_date'] = recent_date
        # fullsitecode = request.GET.get("full_code")
        # site_name = request.GET.get("site_name")
        # # print(site_name)
        # site_name_only = site_name.split(' ')[-1]
        #
        # wlh_json_file_path = os.path.join(app.get_app_workspace().path, 'waterLevel_hist.json')
        #
        # with open(wlh_json_file_path) as f:
        #     wlh_data_reservoir = json.load(f)
        #
        # data_site = wlh_data_reservoir[site_name]
        # historical = get_historicaldata(site_name_only)['values']
        #
        # for i in range(len(historical)):
        #     historical[i][1] -= data_site['ymin']         # change the values from elevations to depths
        # return_object['values_hist'] = historical
        #
        # min = data_site['minlvl'] - data_site['ymin']         # lines for the min/max levels
        # max = data_site['maxlvl'] - data_site['ymin']
        # firstday = historical[0][0]
        # lastday = historical[len(historical)-1][0]
        # return_object['minimum'] = min
        # return_object['maximum'] = max
        # last_elv = wlh_data_reservoir[site_name]['dataValue']
        # return_object['last_elv'] = last_elv
        # avg_elevations = get_historicalaverages(site_name_only)
        # return_object['el_um'] = avg_elevations['elevacion_um']
        # return_object['el_ua'] = avg_elevations['elevacion_ua']
        # # return_object['minimum'] = [[firstday, min], [lastday, min]]
        # # return_object['maximum'] = [[firstday, max], [lastday, max]]
        #
        # values_sc = make_storagecapcitycurve(site_name_only)
        # volumes_info = get_reservoir_volumes(site_name_only,data_site,last_elv)
        # # mysiteinfo = []
        # # myvalues = []
        # # url = "http://128.187.106.131/app/index.php/dr/services/cuahsi_1_1.asmx?WSDL"
        # # water = pwml.WaterMLOperations(url=BASE_URL)
        #
        # # mysiteinfo.append(water.GetInfo(fullsitecode))
        #
        # # return_object['siteInfo'] = mysiteinfo
        # return_object['values_sc'] = values_sc
        # return_object['volumes'] = volumes_info
    except Exception as e:
        print(e)
        return_object['error'] = "The site does not have historical data information."
    return JsonResponse(return_object)

@controller(name='GetValues', url='reservoirs/GetValues')
def GetValues(request):
    return_object = {}

    try:
        url_request_base = 'http://ec2-18-204-193-247.compute-1.amazonaws.com:5000/API'

        date_ini = request.GET.get("start_date")
        date_end = request.GET.get("end_date")

        stn_id = request.GET.get("stn_id")
        var_id = 'Level4'
        request_final_url = f'{url_request_base}/data/dailydata?stn_id={stn_id}&var_id={var_id}&date_ini={date_ini}&date_end={date_end}'
        response = requests.get(request_final_url)
        # breakpoint()
        dailydata_dict = response.json()
        # Parse `response.text` into JSON
        df = pd.DataFrame.from_dict(dailydata_dict)
        return_object['myvalues']=df.to_dict('records')

        # fullsitecode = request.GET.get("full_code")
        # mysiteinfo = []
        # myvalues = []
        # # url = "http://128.187.106.131/app/index.php/dr/services/cuahsi_1_1.asmx?WSDL"
        # water = pwml.WaterMLOperations(url=BASE_URL)
        #
        # mysiteinfo.append(water.GetInfo(fullsitecode))
        #
        # start_date = mysiteinfo[0]['siteInfo'][0]['beginDateTime']
        # end_date = mysiteinfo[0]['siteInfo'][0]['endDateTime']
        # variable_full_code = 'RES-EL'
        # values_x = water.GetValues(fullsitecode, variable_full_code, start_date, end_date)
        # myvalues.append(values_x)
        # timeStamps = []
        # valuesTimeSeries = []
        #
        # return_object['myvalues'] = myvalues
    except Exception as e:
        return_object['error'] = "There is no historical water level data available for this site."

    return JsonResponse(return_object)

@controller(name='GetForecast', url='reservoir/GetForecast')
def GetForecast(request):
    return_object = {}
    rating_curves_file_path = os.path.join(app.get_app_workspace().path, 'rating_curves_DR.xlsx')
    rating_curves = pd.read_excel(rating_curves_file_path)

    site_name = request.GET.get("site_name")
    # print(site_name)
    site_name_only = site_name.split(' ')[-1]
    # print(site_name_only)
    streams_json_file_path = os.path.join(app.get_app_workspace().path, 'streams.json')
    wlh_json_file_path = os.path.join(app.get_app_workspace().path, 'waterLevel_hist.json')

    with open(streams_json_file_path) as f:
        stream_data_reservoir = json.load(f)

    with open(wlh_json_file_path) as f:
        wlh_data_reservoir = json.load(f)

    df_rc = pd.DataFrame({'volume_rc': rating_curves[f'{site_name_only}_Vol_MCM'].tolist(),'elevation_rc': rating_curves[f'{site_name_only}_Elev_m'].tolist()})
    volume_datetime = [0]*15
    daily_vtotal_max = [0]*15
    daily_vtotal_75 = [0]*15
    daily_vtotal_avg = [0]*15

    try:
        for id in stream_data_reservoir[site_name]:
            df = geoglows.streamflow.forecast_stats(id, 'csv')
            df_max = df["flow_max_m^3/s"].dropna()
            s5_df = df["flow_75%_m^3/s"].dropna()
            df_avg = df["flow_avg_m^3/s"].dropna()
            volumes_max = []
            volumes_75 = []
            volumes_avg = []

            volumes_max.append(integrate.trapz(y = df_max[0:8], dx = 10800 ))
            volumes_max.append(integrate.trapz(y = df_max[8:16], dx = 10800 ))
            volumes_max.append(integrate.trapz(y = df_max[16:24], dx = 10800 ))
            volumes_max.append(integrate.trapz(y = df_max[24:32], dx = 10800 ))
            volumes_max.append(integrate.trapz(y = df_max[32:40], dx = 10800 ))
            volumes_max.append(integrate.trapz(y = df_max[40:48], dx = 10800 ))
            volumes_max.append(integrate.trapz(y = df_max[48:52], dx = 21600 ))
            volumes_max.append(integrate.trapz(y = df_max[52:56], dx = 21600 ))
            volumes_max.append(integrate.trapz(y = df_max[56:60], dx = 21600 ))
            volumes_max.append(integrate.trapz(y = df_max[60:64], dx = 21600 ))
            volumes_max.append(integrate.trapz(y = df_max[64:68], dx = 21600 ))
            volumes_max.append(integrate.trapz(y = df_max[68:72], dx = 21600 ))
            volumes_max.append(integrate.trapz(y = df_max[72:76], dx = 21600 ))
            volumes_max.append(integrate.trapz(y = df_max[76:80], dx = 21600 ))
            volumes_max.append(integrate.trapz(y = df_max[80:84], dx = 21600 ))

            volumes_75.append(integrate.trapz(y = s5_df[0:8], dx = 10800 ))
            volumes_75.append(integrate.trapz(y = s5_df[8:16], dx = 10800 ))
            volumes_75.append(integrate.trapz(y = s5_df[16:24], dx = 10800 ))
            volumes_75.append(integrate.trapz(y = s5_df[24:32], dx = 10800 ))
            volumes_75.append(integrate.trapz(y = s5_df[32:40], dx = 10800 ))
            volumes_75.append(integrate.trapz(y = s5_df[40:48], dx = 10800 ))
            volumes_75.append(integrate.trapz(y = s5_df[48:52], dx = 21600 ))
            volumes_75.append(integrate.trapz(y = s5_df[52:56], dx = 21600 ))
            volumes_75.append(integrate.trapz(y = s5_df[56:60], dx = 21600 ))
            volumes_75.append(integrate.trapz(y = s5_df[60:64], dx = 21600 ))
            volumes_75.append(integrate.trapz(y = s5_df[64:68], dx = 21600 ))
            volumes_75.append(integrate.trapz(y = s5_df[68:72], dx = 21600 ))
            volumes_75.append(integrate.trapz(y = s5_df[72:76], dx = 21600 ))
            volumes_75.append(integrate.trapz(y = s5_df[76:80], dx = 21600 ))
            volumes_75.append(integrate.trapz(y = s5_df[80:84], dx = 21600 ))

            volumes_avg.append(integrate.trapz(y = df_avg[0:8], dx = 10800 ))
            volumes_avg.append(integrate.trapz(y = df_avg[8:16], dx = 10800 ))
            volumes_avg.append(integrate.trapz(y = df_avg[16:24], dx = 10800 ))
            volumes_avg.append(integrate.trapz(y = df_avg[24:32], dx = 10800 ))
            volumes_avg.append(integrate.trapz(y = df_avg[32:40], dx = 10800 ))
            volumes_avg.append(integrate.trapz(y = df_avg[40:48], dx = 10800 ))
            volumes_avg.append(integrate.trapz(y = df_avg[48:52], dx = 21600 ))
            volumes_avg.append(integrate.trapz(y = df_avg[52:56], dx = 21600 ))
            volumes_avg.append(integrate.trapz(y = df_avg[56:60], dx = 21600 ))
            volumes_avg.append(integrate.trapz(y = df_avg[60:64], dx = 21600 ))
            volumes_avg.append(integrate.trapz(y = df_avg[64:68], dx = 21600 ))
            volumes_avg.append(integrate.trapz(y = df_avg[68:72], dx = 21600 ))
            volumes_avg.append(integrate.trapz(y = df_avg[72:76], dx = 21600 ))
            volumes_avg.append(integrate.trapz(y = df_avg[76:80], dx = 21600 ))
            volumes_avg.append(integrate.trapz(y = df_avg[80:84], dx = 21600 ))

            i=0
            while i < len(volumes_max):
                daily_vtotal_max[i] = daily_vtotal_max[i] + volumes_max[i]
                daily_vtotal_75[i] = daily_vtotal_75[i] + volumes_75[i]
                daily_vtotal_avg[i] = daily_vtotal_avg[i] + volumes_avg[i]
                volume_datetime[i] = date.today() + timedelta(days = i)
                i = i + 1

        presa_rc_vol = df_rc['volume_rc']
        presa_rc_elev = df_rc['elevation_rc']
        # print(presa_rc_vol)
        init_elv_r = wlh_data_reservoir[site_name]['dataValue']
        lookup_iv = min(range(len(presa_rc_elev)), key=lambda i: abs(presa_rc_elev[i]-init_elv_r))
        # print(len(presa_rc_elev))
        # print(lookup_iv)
        init_vol_r = presa_rc_vol[lookup_iv]
        # print(init_elv_r)

        return_object['max2'] = [x + (init_vol_r * 1000000)  for x in daily_vtotal_max]
        return_object['se52'] = [x + (init_vol_r * 1000000)  for x in daily_vtotal_75]
        return_object['avg2'] = [x + (init_vol_r * 1000000)  for x in daily_vtotal_avg]

        # return_object['max2'] = daily_vtotal_max
        # return_object['se52'] = daily_vtotal_75
        # return_object['avg2'] = daily_vtotal_avg
        #volume to elevation


        elevations_max =[]
        elevations_75 =[]
        elevations_avg =[]
        # print(daily_vtotal_max)
        for volume_max, volume_75, volume_avg in zip(daily_vtotal_max,daily_vtotal_75,daily_vtotal_avg):
            lookup_max = min(range(len(presa_rc_vol)), key=lambda i: abs(presa_rc_vol[i]-(init_vol_r + volume_max/1000000)))
            lookup_75 = min(range(len(presa_rc_vol)), key=lambda i: abs(presa_rc_vol[i]-(init_vol_r + volume_75/1000000)))
            lookup_avg = min(range(len(presa_rc_vol)), key=lambda i: abs(presa_rc_vol[i]-(init_vol_r + volume_avg/1000000)))


            matching_elev_max = presa_rc_elev[lookup_max]
            matching_elev_75 = presa_rc_elev[lookup_75]
            matching_elev_avg = presa_rc_elev[lookup_avg]
            # print(matching_elev_max,matching_elev_75,matching_elev_avg)
            elevations_max.append(matching_elev_max)
            elevations_75.append(matching_elev_75)
            elevations_avg.append(matching_elev_avg)

        # print(elevations_max)
        return_object['max'] = elevations_max
        return_object['se5'] = elevations_75
        return_object['avg'] = elevations_avg
        return_object['date'] = volume_datetime
    except KeyError as e:
        return_object['error'] = f'The reservoir {site_name} does not have forecast data available.'
        print(e)

    return JsonResponse(return_object)
