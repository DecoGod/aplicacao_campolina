from dash.dependencies import Input, Output, State
import os
import dash_bootstrap_components as dbc
import dash
import pandas as pd
from dash import dcc,dash_table
from dash import html as html
import plotly.express as px
import plotly.graph_objects as go
import sys

def get_values(nd,l,qd, largura, altura, fck, eci, lim):

    dicio_valores = {
        'tabela2' : [],
        'tabela3' : [],
        'tabela4' : [],
    }

    ic = (largura * altura ** 3) / 12

    qk = qd / 1.4

    ei = 0.8 * eci * ic

    deltai = (qk * l ** 4) / (8 * ei)

    mid = nd * deltai + qd * ((l ** 2) / 2)

    dicio_valores['tabela2'].append(deltai)
    dicio_valores['tabela2'].append(mid)


    
    deltam_total = (nd * deltai) * 10 ** (-2)

    mtotald = (qd * (l ** 2) / 2) * 10 ** (-2)

    gamaz = 1/(1 - deltam_total/mtotald)

    mtotal = (gamaz * mtotald) 

    dicio_valores['tabela3'] = [deltam_total, mtotald, gamaz, mtotal]

    zetai = lim + 1
    iteracao = 1

    string_lim = str(lim)
    if '.' in string_lim:
        casas_decimais = len(string_lim.split('.')[1]) + 1
    else:
        casas_decimais = 1


    soma_deltamid = 0
    delta_total = deltai

    while zetai > lim:
        
        hf1 = (nd * deltai ) / l
        delta1 = (hf1 * (l ** 3)) / (3 * ei)
        delta_total += delta1
        deltam1d = nd * delta1
        zeta1 = deltam1d / (mid + soma_deltamid)
        soma_deltamid += deltam1d
        row = {'parametro_t4': iteracao,'hfi_t4' : round(hf1, casas_decimais), 'deltai_t4' : round(delta1, casas_decimais),'deltamid_t4' : round(deltam1d, casas_decimais), 'zetai_t4' : round(zeta1, casas_decimais) }
        dicio_valores['tabela4'].append(row)
        iteracao += 1
        deltai = delta1
        zetai = zeta1

    dicio_valores['tabela2'].append(delta_total)
    dicio_valores['tabela2'].append((mid + soma_deltamid) * 10 ** (-2))


    return dicio_valores



screen = dash.Dash(__name__, external_stylesheets=[
                   dbc.themes.FLATLY], prevent_initial_callbacks=True, suppress_callback_exceptions=True)






screen.layout =  dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                       html.Div([
  
                            dash_table.DataTable(
                                id='tabela1',
                                columns=[{'name': 'PARÂMETRO - Efeito', 'id': 'parametro'},
                                        {'name': 'Valor', 'id': 'valor'},
                                        ],
                                data=[
                                    {'parametro': 'Nd (KN)','valor' : ''},
                                    {'parametro': 'L (cm)','valor' : ''},
                                    {'parametro': 'qd (KN/cm)','valor' : ''},
                                    {'parametro': 'Largura (cm)','valor' : ''},
                                    {'parametro': 'Altura (cm)','valor' : ''},
                                    {'parametro': 'Fck (Mpa)','valor' : ''},
                                    {'parametro': 'Eci (KN/cm²)','valor' : ''},
                                    {'parametro': '\u03B6lim','valor' : ''},
                                    
                                ],
                                editable=True,
                                style_cell_conditional=[
                                    {'if': {'column_id': 'parametro'},
                                    'width': '40%'},
                                    {'if': {'column_id': 'valor'},
                                    'width': '130px'},
                                ],
                                 style_data_conditional=[{
                                    'if': {'column_id': 'valor'},
                                    'backgroundColor': 'rgb(173, 216, 230)',
                                    'color': 'black'
                                }],
                                style_data={ 'border': '1px solid black' },
                                style_header={ 'border': '1px solid black' }
                            ),
                        ], style={"background-color": "white", "margin-top": "10px", "margin-left": "0px", }),
                        
                    ], md=5,),
                    dbc.Col([
                           html.Div([
  
                            dash_table.DataTable(
                                id='tabela2',
                                columns=[{'name': 'Parametro-Efeito P-delta', 'id': 'parametro_t1'},
                                        {'name': 'Valor', 'id': 'valor_t1'},
                                        {'name': 'Unidade', 'id': 'unidade_t1'},
                                        ],
                                data=[
                                    {'parametro_t1': '\u0394i = \u03B4','valor_t1' : '','unidade_t1' : 'cm'},
                                    {'parametro_t1': 'Mid','valor_t1' : '','unidade_t1' : 'KN.cm'},
                                    {'parametro_t1': '\u0394total','valor_t1' : '','unidade_t1' : 'cm'},
                                    {'parametro_t1': 'Mtotal','valor_t1' : '','unidade_t1' : 'KN.m'},
                                    
                                ],
                                editable=False,
                                cell_selectable = False,
                                style_cell_conditional=[
                                    {'if': {'column_id': 'parametro_t1'},
                                    'width': '30%'},
                                    {'if': {'column_id': 'unidade_t1'},
                                    'width': '10%'},
                                ],
                                 style_data_conditional=[{
                                    'if': {'column_id': 'valor_t1'},
                                    'backgroundColor': 'rgb(173, 216, 230)',
                                    'color': 'black'
                                }],
                                style_data={ 'border': '1px solid black' },
                                style_header={ 'border': '1px solid black' }
                            ),
                            dash_table.DataTable(
                                id='tabela3',
                                columns=[{'name': 'Parametro \u03B3z', 'id': 'parametro_t2'},
                                        {'name': 'Valor', 'id': 'valor_t2'},
                                        {'name': 'Unidade', 'id': 'unidade_t2'},
                                        ],
                                data=[
                                    {'parametro_t2': '\u0394Mtotal,d','valor_t2' : '', 'unidade_t2' : 'KN.m'},
                                    {'parametro_t2': 'Mtotal,d','valor_t2' : '', 'unidade_t2' : 'KN.m'},
                                    {'parametro_t2': '\u03B3z','valor_t2' : '', 'unidade_t2' : 'N.m'},
                                    {'parametro_t2': 'Mtotal','valor_t2' : '', 'unidade_t2' : 'KN.m'},

                                    
                                ],
                                editable=False,
                                cell_selectable = False,
                                 style_data_conditional=[{
                                    'if': {'column_id': 'valor_t2'},
                                    'backgroundColor': 'rgb(173, 216, 230)',
                                    'color': 'black'
                                }],
                                style_data={ 'border': '1px solid black' },
                                style_header={ 'border': '1px solid black' }
                            ),
                        ], style={"background-color": "white", "margin-top": "10px", "margin-left": "0px", }),
                          
                    ], md=7),

                ]),
                dbc.Row([


                    html.Div([
                    html.Img(id="logo", src=screen.get_asset_url("referencia.JPG")),

                    ], style={"background-color": "white", "margin-top": "30px", "padding": "0px", }),
                ]),
                
               
            ], md = 6, style={ "margin-left": "0px", }),
            dbc.Col([
                html.Div([
                    dash_table.DataTable(
                                id='tabela4',
                                columns=[{'name': 'Iterações', 'id': 'parametro_t4'},
                                        {'name': 'Hfi (KN)', 'id': 'hfi_t4'},
                                        {'name': '\u0394i (cm)', 'id': 'deltai_t4'},
                                        {'name': '\u0394Mid (KN.m)', 'id': 'deltamid_t4'},
                                        {'name': '\u03B6i', 'id': 'zetai_t4'},

                                        ],
                                data=[
                                    {'parametro_t4': '','hfi_t4' : '', 'deltai_t4' : '','deltamid_t4' : '', 'zetai_t4' : '' },
                                    {'parametro_t4': '','hfi_t4' : '', 'deltai_t4' : '','deltamid_t4' : '', 'zetai_t4' : '' },
                                    {'parametro_t4': '','hfi_t4' : '', 'deltai_t4' : '','deltamid_t4' : '', 'zetai_t4' : '' },
                                    {'parametro_t4': '','hfi_t4' : '', 'deltai_t4' : '','deltamid_t4' : '', 'zetai_t4' : '' },
                                    {'parametro_t4': '','hfi_t4' : '', 'deltai_t4' : '','deltamid_t4' : '', 'zetai_t4' : '' },
                                    {'parametro_t4': '','hfi_t4' : '', 'deltai_t4' : '','deltamid_t4' : '', 'zetai_t4' : '' },


                                    
                                ],
                                editable=False, locale_format = {'symbol' : ['$', '']},
                                cell_selectable = False,
                                style_cell_conditional=[
                                    {'if': {'column_id': 'parametro_t4'},
                                    'width': '20%'},
                                    {'if': {'column_id': 'hfi_t4'},
                                    'width': '20%'},
                                    {'if': {'column_id': 'deltai_t4'},
                                    'width': '20%'},
                                    {'if': {'column_id': 'deltamid_t4'},
                                    'width': '20%'},
                                    {'if': {'column_id': 'zetai_t4'},
                                    'width': '20%'},

                                ],
                               
                            ),
                    ], style={"background-color": "white", "margin": "5px", "padding": "0px", }),
            ], md = 6),

        ],  style={ "margin-left": "0px", }),
        
    ],  style={ "margin-left": "0px", 'margin-right':'0px' })


@screen.callback(
    [
        Output('tabela2', 'data'),
        Output('tabela3', 'data'),
        Output('tabela4', 'data')
    ],
    [
        Input('tabela1','data_timestamp')
    ],
    [
        State('tabela1', 'data')
    ]
)
def calcular(timestamp, data):

    try:
        for row in data:
            row['valor'] = float(row['valor'])

        values = get_values(data[0]['valor'],data[1]['valor'], data[2]['valor'],data[3]['valor'],data[4]['valor'],data[5]['valor'],data[6]['valor'], data[7]['valor'])

        data2_values = values['tabela2']
        data3_values = values['tabela3']
        data4_values = values['tabela4']




        data2=[
            {'parametro_t1': '\u0394i = \u03B4','valor_t1' : round(data2_values[0],2),'unidade_t1' : 'cm'},
            {'parametro_t1': 'Mid','valor_t1' :round( data2_values[1],2),'unidade_t1' : 'KN.cm'},
            {'parametro_t1': '\u0394total','valor_t1' : round( data2_values[2],3),'unidade_t1' : 'cm'},
            {'parametro_t1': 'Mtotal','valor_t1' : round( data2_values[3],2),'unidade_t1' : 'KN.m'},
            
        ]
        data3 = [
            {'parametro_t2': '\u0394Mtotal,d','valor_t2' : round(data3_values[0],2), 'unidade_t2' : 'KN.m'},
            {'parametro_t2': 'Mtotal,d','valor_t2' : round(data3_values[1],2), 'unidade_t2' : 'KN.m'},
            {'parametro_t2': '\u03B3z','valor_t2' : round(data3_values[2],2), 'unidade_t2' : 'N.m'},
            {'parametro_t2': 'Mtotal','valor_t2' : round(data3_values[3],2), 'unidade_t2' : 'KN.m'},
        ]
        


        return data2,data3,data4_values
    except:
        data2=[
            {'parametro_t1': '\u0394i = \u03B4','valor_t1' : '','unidade_t1' : 'cm'},
            {'parametro_t1': 'Mid','valor_t1' : '','unidade_t1' : 'KN.cm'},
            {'parametro_t1': '\u0394total','valor_t1' : '','unidade_t1' : 'cm'},
            {'parametro_t1': 'Mtotal','valor_t1' : '','unidade_t1' : 'KN.m'},
            
        ]
        data3 = [
            {'parametro_t2': '\u0394Mtotal,d','valor_t2' : '', 'unidade_t2' : 'KN.m'},
            {'parametro_t2': 'Mtotal,d','valor_t2' : '', 'unidade_t2' : 'KN.m'},
            {'parametro_t2': '\u03B3z','valor_t2' : '', 'unidade_t2' : 'N.m'},
            {'parametro_t2': 'Mtotal','valor_t2' : '', 'unidade_t2' : 'KN.m'},
        ]
        data4=[
            {'parametro_t4': '','hfi_t4' : '', 'deltai_t4' : '','deltamid_t4' : '', 'zetai_t4' : '' },
            {'parametro_t4': '','hfi_t4' : '', 'deltai_t4' : '','deltamid_t4' : '', 'zetai_t4' : '' },
            {'parametro_t4': '','hfi_t4' : '', 'deltai_t4' : '','deltamid_t4' : '', 'zetai_t4' : '' },
            {'parametro_t4': '','hfi_t4' : '', 'deltai_t4' : '','deltamid_t4' : '', 'zetai_t4' : '' },
            {'parametro_t4': '','hfi_t4' : '', 'deltai_t4' : '','deltamid_t4' : '', 'zetai_t4' : '' },
            {'parametro_t4': '','hfi_t4' : '', 'deltai_t4' : '','deltamid_t4' : '', 'zetai_t4' : '' },

        ]
        return data2,data3,data4




server = screen.server

if __name__ == "__main__":
    if len(sys.argv) > 1:
        screen.run_server(debug=True)
    else:
        screen.run_server(debug=True)
