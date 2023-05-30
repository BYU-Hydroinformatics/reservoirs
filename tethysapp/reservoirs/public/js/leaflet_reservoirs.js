function getInfoTable() {
    $("#info_table-loading").removeClass("d-none");
    let full_site_code = $("#variables").val();
    let site_full_name = $("#variables option:selected").text();

    let fsc = {
      full_code: full_site_code,
      site_name: site_full_name
    }
    if (site_full_name !== "None") {
        $.ajax({
        type: "GET",
        url: "GetInfo/",
        dataType: "JSON",
        data: fsc,

        success: function(result) {
          try{
            let mystation = $("#variables").val();
            var mysitename = result['stn_id'];
            var sitecode = result['station'];
            var variable = result['var_id'];
            var beginDateTime = result['start_date'];
            var endDateTime = result['end_date'];
            var recentDateTime = result['recent_date']
            var recentValue = result['recent_val']
            var minValue = result['min_val']
            var maxValue = result['max_val']
            if (!result.hasOwnProperty('error')){
              $("#info_site_table").html(

                `<div class="table-responsive">
                  <table class="table">
                    <tbody>
                      <tr>
                        <td>Site Name</td>
                        <td id="stn_id">${mysitename}</td>
                      </tr>
                      <tr>
                        <td>Site Code</td>
                        <td id="site_code">${sitecode}</td>
                      </tr>
                      <tr>
                        <td>Active Variable</td>
                        <td>${variable}</td>
                      </tr>
                      <tr>
                        <td>Beginning Date Time </td>
                        <td id="start_date">${beginDateTime.split("T")[0]}</td>
                      </tr>
                      <tr>
                        <td>End Date Time </td>
                        <td id="end_date">${endDateTime.split("T")[0]}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>`);
            }
            else{
              $("#info_site_table").html(result['error'])
            }

              $("#info_site_table").removeClass("d-none");
              $("#info_site-loading").removeClass("d-none");
              $("#title-site").removeClass("d-none");
              $("#timeseries").removeClass("d-none");
              $("#info_table-loading").addClass("d-none");
          }
          catch(e){
            console.log(e);
            $("#info_table-loading").addClass("d-none");
          }
        }
      })
  } else {
    $("#info_table-loading").addClass("d-none");
  }
}


$("#variables").on("change",function(){
  $("#info_site_table").addClass("d-none");
  $("#timeseries").addClass("d-none");
  $("#info_site-loading").addClass("d-none");
  $("#info_table-loading").addClass("d-none");
  getInfoTable()
})

var map = L.map('mapid', {
    zoom: 7.6,
    minZoom: 1.20,
    boxZoom: true,
    maxBounds: L.latLngBounds(L.latLng(-100.0,-270.0), L.latLng(100.0, 270.0)),
    center: [18.7357, -70.1627],
});


var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
var Esri_Imagery_Labels = L.esri.basemapLayer('ImageryLabels');
basemaps = {"Basemap": L.layerGroup([Esri_WorldImagery, Esri_Imagery_Labels]).addTo(map)}

//base graph
var getSitesNow = function(){
  $("#info_table-loading").removeClass("d-none");
    $.ajax({
        type: "GET",
        url: "GetSites/",
        dataType: "JSON",

        success: function(result) {
          try{
            var damIcon = L.icon({
                iconUrl:'https://img.icons8.com/color/344/dam.png',
                shadowUrl:'https://img.icons8.com/color/344/dam.png',

                iconSize:[40, 40], // size of the icon
                shadowSize:[35, 35], // size of the shadow
            });
            var mySites = result.siteInfo;

            for(var i=0; i< mySites.length; ++i){
                if (mySites[i][2]!=0) {

                    var markerLocation = new L.LatLng(mySites[i][2], mySites[i][3]);
                    var marker = new L.Marker(markerLocation,{icon: damIcon})
                    marker.bindPopup(mySites[i][1]);
                    map.addLayer(marker)
                }
            }

            $("#variables").change(function() {
                let curres = $("#variables").val()
                id = curres
                var markers = [];
                if (id == 0) {
                    var base_view = new L.latLng(18.993036, -70.507958)
                    map.setView(base_view, 8)
                    map.closePopup()
                } else {
                    for (var i=0; i<mySites.length; ++i) {
                        var markerLocation = new L.LatLng(mySites[i][2], mySites[i][3]);
                        var marker = new L.Marker(markerLocation,{icon: damIcon});
                        marker.bindPopup(mySites[i][0]);
                        map.addLayer(marker)
                        markers.push(marker)
                        if (id == mySites[i][1]) {
                            map.setView(markerLocation, 10);
                            for (var j in markers){
                                if (markers[j]._popup._content == mySites[i][0]){
                                    markers[j].openPopup()
                                }
                            }
                        }
                    }
                }
            })
          }
          catch(e){
            console.log(e);
            $("#info_table-loading").addClass("d-none");
          }
          $("#info_table-loading").addClass("d-none");
         },
         error: function(e){
          console.log(e)
          $("#info_table-loading").addClass("d-none");
         }
    })
}
getSitesNow();

function getValues() {
  try{
    $('#mytimeseries-loading').removeClass('d-none');
    $('#error_ts').addClass('d-none');
    $('#myDiv').addClass('d-none');
    let site_full_code = $("#variables").val();
    let stn_id = $("#stn_id").text();
    let start_date = $("#start_date").text();
    let end_date = $("#end_date").text();
    let fsc = {
        'site_code': site_full_code, //stationname
        'start_date': start_date,
        'end_date': end_date,
        'stn_id': stn_id //station (actual full name)
    }
    $.ajax({
        type: "GET",
        url: "GetValues/",
        dataType: "JSON",
        data: fsc,
        success: function(result) {

            if(!result.hasOwnProperty('error')){
              $('#error_ts').addClass('d-none');
              $('#myDiv').removeClass('d-none');
              // $('#volume_chart').removeClass('d-none');
              // $('#forecast_chart').removeClass('d-none');


              var values = result['myvalues'];
              sitename = stn_id;
              const mydatavalues = [];
              const mydateTime = [];

              for(var i=0; i<values.length; ++i){
                  mydatavalues.push(values[i]['Value']);
                  mydateTime.push(values[i]['Date'])
              }

              $("#ts_button").on("click",function(){
                dm(mydateTime,mydatavalues,"M","Time","Water_Level");
              })
              var values_trace = {
                type: "scatter",
                x: mydateTime,
                y: mydatavalues,
                line: {color: '#17BECF'}
              }

              var data = [values_trace];

              var layout = {
                  title: 'Water Surface Level',
                  xaxis: {
                      title: {
                          text: 'Years [yr]',
                          font: {
                          family: 'Courier New, monospace',
                          size: 18,
                          color: '#7f7f7f'
                          }
                      },
                  },
                  yaxis: {
                      title: {
                          text: 'Meters [m]',
                          font: {
                          family: 'Courier New, monospace',
                          size: 18,
                          color: '#7f7f7f'
                          }
                      }
                  },
                  autosize:true
              };

              Plotly.newPlot('myDiv', data, layout);
              window.onresize = function() {
                  Plotly.relayout('myDiv', {
                      'xaxis.autorange': true,
                      'yaxis.autorange': true
                  });
              };

            }
            else{
              $('#error_ts').removeClass('d-none');
              $('#myDiv').addClass('d-none');
              $("#error_ts").html(`${result['error']}`)
            }
            $('#mytimeseries-loading').addClass('d-none');
        },
        error: function(e){
          $('#mytimeseries-loading').addClass('d-none');
          $('#error_ts').addClass('d-none');
        }

    })
  }
  catch(e){
    $('#mytimeseries-loading').addClass('d-none');
    $('#error_ts').addClass('d-none');
  }
}

function getValues2() {
  try{
    $('#mytimeseries-loading').removeClass('d-none');
    $('#error_ts').addClass('d-none');
    $('#myDiv').addClass('d-none');
    let site_full_code = $("#variables").val();
    let stn_id = $("#stn_id").text();
    let start_date = $("#start_date").text();
    let end_date = $("#end_date").text();
    let fsc = {
        'site_code': site_full_code, //stationname
        'start_date': start_date,
        'end_date': end_date,
        'stn_id': stn_id //station (actual full name)
    }
    $.ajax({
        type: "GET",
        url: "GetValues",
        dataType: "JSON",
        data: fsc,
        success: function(result) {
          try{

            $("#error_info").addClass("d-none");
            $("#container_tabs_info").removeClass("d-none");

            var values = result['myvalues'];
            sitename = values[0]['Station'];
            const mydatavalues = [];
            const mydateTime = [];

            for(var i=0; i<values.length; ++i){
                mydatavalues.push(values[i]['Value']);
                mydateTime.push(values[i]['Date'])
            }

            var storage_capacity = result.values_sc;
            var elvs = storage_capacity.map(function (i) { return i[1]})
            var vols = storage_capacity.map(function (i) { return i[0]})
            historical_data = mydatavalues

            var date_hist = historical_data.map(function (i) { return i[0]})
            var elv_hist = historical_data.map(function (i) { return i[1]})
            // elv_hist = elv_hist.map( function (i) { if(i<0){return 0} });
            for(let i=0; i < elv_hist.length; ++i ){
              if(elv_hist[i] < 0 ){
                elv_hist[i] = 0;
              }

            }
            var min_vals_hist = Array(date_hist.length).fill(result.minimum);
            var max_vals_hist = Array(date_hist.length).fill(result.maximum);
            let sc_element = document.getElementById("sc_button");
            $("#sc_button").click(function(){
              dm(elvs,vols,"CMC","M","Storage_Capacity_Curve");
            })
            $("#hist_button").click(function(){
              dm(date_hist,elv_hist,"M","Time","Historical_Data");
            })

            let myreservoir = $("#variables").val();


            var sc_max_trace = {
              type: "scatter",
              name: 'Niveles Reportados',
              x: elvs,
              y: vols,
              fill: 'tozeroy',
              mode: 'lines',
            }
            var data = [sc_max_trace];

        var layout = {
            title: 'Storage Capacity Curve',
            xaxis: {
                title: {
                    text: 'Water Surface Level [m]',
                    font: {
                    family: 'Courier New, monospace',
                    size: 18,
                    color: '#7f7f7f'
                    }
                }
            },
            yaxis: {
                title: {
                    text: 'Volume[CMC]',
                    font: {
                    family: 'Courier New, monospace',
                    size: 18,
                    color: '#7f7f7f'
                    }
                }
            },
            autosize:true

        };

        Plotly.newPlot('site_sc_chart', data, layout);
        var hist_trace = {
          type: "scatter",
          name: 'Water Level Reported',
          x: date_hist,
          y: elv_hist,
          fill: 'tozeroy',
          mode: 'lines',
        }
        var max_trace = {
          type: "scatter",
          name: 'Water Level Reported',
          x: date_hist,
          y: max_vals_hist,
          mode: 'lines',
        }
        var min_trace = {
          type: "scatter",
          name: 'Water Level Reported',
          x: date_hist,
          y: min_vals_hist,
          mode: 'lines',
        }
        var data_hist = [hist_trace,max_trace,min_trace ];

        var layout = {
            title: 'Historical Data',

            yaxis: {
                title: {
                    text: 'Water Surface Level [m]',
                    font: {
                    family: 'Courier New, monospace',
                    size: 18,
                    color: '#7f7f7f'
                    }
                }
            },
            autosize:true,
            showlegend: true,
            legend: {"orientation": "h"}
        };
        Plotly.newPlot('site_hist_chart', data_hist, layout);
        window.onresize = function() {
            Plotly.relayout('site_hist_chart', {
                'xaxis.autorange': true,
                'yaxis.autorange': true
            });
            Plotly.relayout('site_sc_chart', {
                'xaxis.autorange': true,
                'yaxis.autorange': true
            });
        };
        $("#site_info_ta").html(

          `<div class="table-responsive">
            <table class="table table-hover">
            <thead>
              <tr>
              <th>Volume Type</th>
              <th>Value (MCM)</th>
              </tr>
            </thead>
              <tbody>
                <tr>
                  <td>Last Volume</td>
                  <td>${result['volumes']['Actual']} </td>
                </tr>
                <tr>
                  <td>Util Volume</td>
                  <td>${result['volumes']['Util']}</td>
                </tr>
                <tr>
                  <td>Maximun Volume</td>
                  <td>${result['volumes']['Max']}</td>
                </tr>
                <tr>
                  <td>Minimun Volume</td>
                  <td>${result['volumes']['Min']}</td>
                </tr>
              </tbody>
            </table>
          </div>`);
        $("#site_info_ta2").html(

          `<div class="table-responsive">
            <table class="table table-hover">
            <thead>
              <tr>
              <th>Elevation Type</th>
              <th>Value (M)</th>
              </tr>
            </thead>
              <tbody>
                <tr>
                  <td>Last Elevation</td>
                  <td>${result['last_elv']} </td>
                </tr>
                <tr>
                  <td>Maximun Elevation</td>
                  <td>${result['maximum']}</td>
                </tr>
                <tr>
                  <td>Annually Average Elevation</td>
                  <td>${result['el_ua']}</td>
                </tr>
                <tr>
                  <td>Monthly Average Elevation</td>
                  <td>${result['el_um']}</td>
                </tr>
                <tr>
                  <td>Minimun Elevation</td>
                  <td>${result['minimum']}</td>
                </tr>
              </tbody>
            </table>
          </div>`);
        $("#info_site-loading").addClass("d-none");

      }
      catch(e){
        $("#info_site-loading").addClass("d-none");
        $("#container_tabs_info").addClass("d-none");
        $("#error_info").removeClass("d-none");
        $('#error_info').html(`${result.error}`)
      }

    },

    error: function(er){
      $("#info_site-loading").addClass("d-none");
      $("#container_tabs_info").addClass("d-none");
      $("#error_info").addClass("d-none");
    }

    })
  }
  catch(e){
    $("#info_site-loading").addClass("d-none");
    $("#container_tabs_info").addClass("d-none");
    $("#error_info").addClass("d-none");
  }

}

function getForecast() {
    $('#fe-loading').removeClass('d-none');
    $('#fv-loading').removeClass('d-none');
    $('#error_vol').addClass('d-none');
    $('#error_fore').addClass('d-none');
    $('#forecast_chart').addClass('d-none');
    $('#volume_chart').addClass('d-none');
    let site_full_name = $('#stn_id').text();
    let fsc = {
        'site_name': site_full_name
    }
    $.ajax({
        type: "GET",
        url: "getForecast",
        dataType: "JSON",
        data: fsc,
        success: function(result) {
          try{
            $('#fe-loading').addClass('d-none');
            $('#fv-loading').addClass('d-none');

            if(!result.hasOwnProperty('error')){
              $('#error_vol').addClass('d-none');
              $('#error_fore').addClass('d-none');
              $('#forecast_chart').removeClass('d-none');
              $('#volume_chart').removeClass('d-none');

                //water elevation
              var values_avg = result.avg;
              var values_se = result.se5;
              var values_max = result.max;
              var mydateTime =  result.date;
              // var init_elv = result.init_elv;

                //volume
              var values_avg2 = result.avg2;
              var values_se2 = result.se52;
              var values_max2 = result.max2;
              var mydateTime2 =  result.date2;

              $("#fv_button").on("click", function(){
                dm2(values_avg,values_se,values_max,mydateTime,"Date","Average Streamflow Forecast Volume (MCM)","75%  Streamflow Forecast Volume (MCM)","Max Streamflow Forecast Volume (MCM)","Forecasted_Volume")
              })
              $("#fe_button").on("click", function(){
                dm2(values_avg2,values_se2,values_max2,mydateTime,"Date","Average Streamflow Forecast Water Elevation (M)","75%  Streamflow Forecast Water Elevation (M)","Max Streamflow Forecast Water Elevation (M)","Forecasted_Water Elevation")
              })


              // var init_vol = result.init_vol;
              //
              //
              // var min_vals = [values_avg[0],values_se[0]];
              // var chart_min =  Math.min.apply(null,min_vals);
              //
              // console.log([values_max[0],values_avg[0],values_se[0]]);
              // console.log(chart_min);
              // var data_chart_limits = Array(mydateTime.length).fill(chart_min-20);
              // var init_chart_limits = Array(mydateTime.length).fill(init_elv);
              // console.log(data_chart_limits);

              // var values_limits_trace= {
              //   type: "scatter",
              //   x: mydateTime,
              //   y: init_chart_limits,
              //   mode: 'lines',
              //   // line: {color: 'rgba(255,0,0,0.2)'},
              //   name: '',
              //
              // }
              var values_max_trace = {
                type: "scatter",
                name: 'Max StreamFlow Forecast',
                x: mydateTime,
                y: values_max,
                fill: 'tonexty',
                mode: 'lines',
                visible:'legendonly'
              }
              var values_avg_trace = {
                type: "scatter",
                name: 'Average StreamFlow Forecast',
                mode: 'lines',
                x: mydateTime,
                y: values_avg,
                // line: {color: '#17BECF'}
              }
              var values_se5_trace = {
                type: "scatter",
                name: '75% StreamFlow Forecast',
                x: mydateTime,
                y: values_se,
                line: {
                  dash: 'dashdot',
                  width: 4
                }
              }
              // var init_limits_trace= {
              //   type: "scatter",
              //   x: mydateTime,
              //   y: init_chart_limits,
              //   mode: 'lines',
              //   // line: {color: 'rgba(255,0,0,0.2)'},
              //   name: 'Initial Volume',
              // }
              var values_max_trace2 = {
                type: "scatter",
                name: 'Max StreamFlow Forecast',
                x: mydateTime,
                y: values_max2,
                fill: 'tonexty',
                mode: 'lines',
                visible: 'legendonly'
              }
              var values_avg_trace2 = {
                type: "scatter",
                name: 'Average StreamFlow Forecast',
                mode: 'lines',
                x: mydateTime,
                y: values_avg2,
                // fill: 'tozeroy',

                // line: {color: '#17BECF'}
              }
              var values_se5_trace2 = {
                type: "scatter",
                name: '75% StreamFlow Forecast',
                x: mydateTime,
                y: values_se2,
                // fill: 'tozeroy',
                line: {
                  dash: 'dashdot',
                  width: 4
                }
              }
              // var data = []
              // if(chart_min > 0){
              //   var data = [values_se5_trace,values_max_trace,values_avg_trace];
              //   // var data = [values_limits_trace,values_max_trace,values_avg_trace,values_se5_trace];
              // }
              // else{
              //   var data = [values_avg_trace,values_max_trace,values_se5_trace];
              //   // var data = [values_limits_trace,values_max_trace,values_avg_trace,values_se5_trace];
              // }
              // var data = [values_limits_trace,values_max_trace,values_avg_trace,values_se5_trace];
              var data = [values_avg_trace,values_max_trace,values_se5_trace];

              var data2 = [values_avg_trace2,values_se5_trace2,values_max_trace2];

              var layout = {
                  title: 'Forecasted Water Surface Level',
                  yaxis: {
                      title: {
                          text: 'Water Surface Level [m]',
                          font: {
                          family: 'Courier New, monospace',
                          size: 18,
                          color: '#7f7f7f'
                          }
                      },
                      autorange:true
                  },
                  autosize:true
              };
              var layout2 = {
                  title: 'Forecasted Volume',
                  yaxis: {
                      title: {
                          text: 'Volume [MCM]',
                          font: {
                          family: 'Courier New, monospace',
                          size: 18,
                          color: '#7f7f7f'
                          }
                      },
                      autorange:true

                  },
                  autosize:true
              };
              Plotly.newPlot('forecast_chart', data, layout);
              Plotly.newPlot('volume_chart', data2, layout2);
              window.onresize = function() {
                  Plotly.relayout('forecast_chart', {
                      'xaxis.autorange': true,
                      'yaxis.autorange': true
                  });
                  Plotly.relayout('volume_chart', {
                      'xaxis.autorange': true,
                      'yaxis.autorange': true
                  });
              };
            }
            else{
              $('#error_vol').removeClass('d-none');
              $('#error_fore').removeClass('d-none');
              $('#forecast_chart').addClass('d-none');
              $('#volume_chart').addClass('d-none');
              $("#error_vol").html(result['error']);
              $("#error_fore").html(result['error']);
            }

          }
          catch(e){
            console.log(e);
            $('#fe-loading').addClass('d-none');
            $('#fv-loading').addClass('d-none');
            $('#error_vol').addClass('d-none');
            $('#error_fore').addClass('d-none');
            $('#forecast_chart').addClass('d-none');
            $('#volume_chart').addClass('d-none');
          }
        },
        error: function(er){
          $('#fe-loading').addClass('d-none');
          $('#fv-loading').addClass('d-none');
          $('#error_vol').addClass('d-none');
          $('#error_fore').addClass('d-none');
          $('#forecast_chart').addClass('d-none');
          $('#volume_chart').addClass('d-none');
        }
    })
}

function load_timeseries() {

    let myreservoir = $("#variables").val();


    if (myreservoir === 0) {

        alert("You have not selected a reservoir");

    } else {
      $("#presa_name").html(`${$("#variables option:selected").text()}`)
        // $("#siteinfo").html('');
        // $("#mytimeseries").html('');
        // getValues2();
        $("#obsgraph").modal('show');
        getValues();
        getForecast();

    }
}

$("#timeseries").click(function() {
    load_timeseries();
})


$('#forecast_tab_link').click(function(){
  try{
    Plotly.Plots.resize("forecast_chart");
    Plotly.relayout("forecast_chart", {
        'xaxis.autorange': true,
        'yaxis.autorange': true
    });
  }
  catch(e){
    console.log(e);
  }
})

$('#mytimeseries_tab_link').click(function(){
  try{
    Plotly.Plots.resize("myDiv");
    Plotly.relayout("myDiv", {
        'xaxis.autorange': true,
        'yaxis.autorange': true
    });
  }
  catch(e){
    console.log(e);
  }
})

$('#volumechart_tab_link').click(function(){
  try{
    Plotly.Plots.resize("volume_chart");
    Plotly.relayout("volume_chart", {
        'xaxis.autorange': true,
        'yaxis.autorange': true
    });
  }
  catch(e){
    console.log(e);
  }

})
$('#siteinfo_tab_link').click(function() {
  try {
    var site_sc_chart = document.getElementById("site_sc_chart");
    if (site_sc_chart !== null) {
      Plotly.update("site_sc_chart", {
        layout: {
          xaxis: {
            autorange: true
          },
          yaxis: {
            autorange: true
          }
        }
      });

      var site_hist_chart = document.getElementById("site_hist_chart");
      if (site_hist_chart !== null) {
        Plotly.update("site_hist_chart", {
          layout: {
            xaxis: {
              autorange: true
            },
            yaxis: {
              autorange: true
            }
          }
        });
      }
    }
  } catch (e) {
    console.log(e);
  }
})
