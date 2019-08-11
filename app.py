# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 22:44:31 2019

@author: DB
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from textwrap import dedent as d
from dash.dependencies import Input, Output

from utils import show_water_data, draw_water_bg_map, \
draw_bird_sample_map, draw_tree9, parse_treemap_input, draw_amount_series

external_stylesheets = [
        "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
        "https://freelancerlife.info/static/css/FreeLancerLife.css"
        ]

bird_df = pd.read_csv('鳥類資料統整201907_mod.csv')

app = dash.Dash(external_stylesheets=external_stylesheets)

app.title = '布袋鹽田資料視覺化'

server = app.server

## default figs
bg_map = draw_water_bg_map()
bs_map = draw_bird_sample_map()
d_water_fig = show_water_data([1,2,3], 0)

n,exp,v = parse_treemap_input(bird_df, C='名稱')
tree_bird = draw_tree9(v,n,exp)

n,exp,v = parse_treemap_input(bird_df, C='棲地類型')
tree_habitat = draw_tree9(v,n,exp)

n,exp,v = parse_treemap_input(bird_df, C='科名')
tree_family = draw_tree9(v,n,exp)

bseries_fig = draw_amount_series(bird_df, '樣區編號')

app.layout = html.Div([
    html.Div([
    html.Div(className='col-1'),
    html.Div([
    html.H1(children='布袋鹽田鳥類生態調查資料視覺化(初版)', style={ 'text-align': 'center' }),
    html.Div([
        html.Div([
            html.H2('So, dear customer:',className='card-title'),
            dcc.Markdown('''      
            **this is the prototype demo app for your project**,
            
            這是這個案子的初稿，我將我想的到的資料視覺化元素放了上去，先讓你們看看可不可以，有沒有哪些東西要新增或減少。
            版型的部分我還不滿意，但要等確認要哪些元件後再做統一調整會比較適合。
            
            目前將水文資料和鳥類調查資料分開:
                
            * 水文資料
            
                含有1地圖(可用滑鼠點選或按住拖選調查點位)、1下拉式選單(選擇圖表要畫哪個水文參數)、
                1文字輸出(顯示目前點選了那些樣點)、及1個水文資料時間序列散布圖。在地圖上及下拉式選單的動作會立刻更新這張圖表的內容。
                
            * 鳥類資料
            
                含有一地圖(單純顯示樣站，沒有點選功能)、1資料表(可以篩選資料，會更新3張treemap與1張plot)、3張treemap(用來呈現種類、棲地類別、科別的占比)、
                1下拉式選單(用來決定散布圖要用哪個單位來呈現總數量)、1數量時間序列散布圖。
                
            資料表的篩選操作說明:
                
            1. 在每個欄位名稱的左邊有兩個三角，點選後可以讓資料表依此欄位昇序或降序排列。
                
            2. 第二列為各欄位的篩選條件，可以直接輸入條件，如: `> 100`、或是直接輸入數值 `小白鷺`，
            或部分文字，如:在名稱的篩選條件只輸入`小`，則會將名稱有小的都抓出來。
                
            3. 如果沒有符合的篩選條件，則資料表會是空白，此時對應到的圖表會是改以依據沒有任何篩選條件的完整數據呈現。
            
            以上，再得到你的回應之後，會再做內容的修訂與版面、美觀上的優化。
            
            #### 我的聯絡方式
            * email: even311379@hotmail.com
            * phone: 0989914039
            * 個人網站： [PUF studio](https://freelancerlife.info)
            ''',style={'padding-left':'5rem'},className='card-text'),
        ],className='card-body')
    ],className='card border-secondary mb-3'),
    html.H2(children='水文資料', style={ 'text-align': 'left' }),
    ## the first row (left part is panels, right part is the map)
    html.Div([
        html.Div([
            html.Div([
                html.H4('選單區',className='card-title'),
                ## 選點位
                html.Div([
                    html.Div([
                        html.P('在地圖上選取調查點位:'),
                        html.P(id='sdata',style={'padding-left':'5rem'})
                    ],className = 'card-body')
                ], className='card border-secondary mb-3'),
                ## 選水文資料
                html.Div([
                    html.Div([
                        html.P('選擇水文資料'),
                        dcc.Dropdown(
                            id = 'WaterParameter',
                            options=[
                                {'label': '溫度', 'value': 0},
                                {'label': '導電度（mS/cm）', 'value': 1},
                                {'label': '氧化還原電位（mV, ORP）', 'value': 2},
                                {'label': '溶氧量（mg/L, DO）', 'value': 3},
                                {'label': '溶氧度（%）', 'value': 4},
                                {'label': '濁度（NTU）', 'value': 5},
                                {'label': '酸鹼值（pH）', 'value': 6},
                                {'label': '鹽度（ppt）', 'value': 7},
                                {'label': '總固形物（g/L, TDS）', 'value': 8},
                                {'label': '水深', 'value': 9},
                            ],
                            value=0,
                            multi=False,
                            placeholder="選擇水文參數"),
                    ], className='card-body'),
                ], className = 'card border-secondary mb-3')
            ],className='card-body'),
        ],className='col col-lg-6 card border-secondary mb-3'),
        html.Div([
            html.Div([
                html.H4('水文資料調查點位',style={ 'text-align': 'center' }),
                html.Div(dcc.Graph(id='bg_map',figure=bg_map)),
            ],className='card-body')
        ],className='col col-lg-6 card border-secondary mb-3'),
    ],className='row'),
    
    ## The second row, shows water and bird data
    html.Div([
        html.Div([
            html.Div([
                dcc.Markdown('水文資料: 溫度',id='water_fig_title'),
                html.Div(dcc.Graph(id='water_fig', figure=d_water_fig)),
            ], className = 'card-body')
        ], className='card border-secondary mb-3', style={"width":"100%"})
    ],className='row'),
    html.Br(),
    html.Br(),
    html.H2(children='鳥類資料', style={ 'text-align': 'left' }),
    html.Div([
        html.Div([
            html.Div([
                html.H4('資料表',style={ 'text-align': 'center' }),
                dash_table.DataTable(
                    id='bird_table',
                    data = bird_df.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in bird_df.columns],
                    fixed_rows={ 'headers': True, 'data': 0 },
                    style_cell={'width': '75px','whiteSpace': 'no-wrap'},
                    style_as_list_view=True,
                    style_cell_conditional=[{'if':{'column_id':c}, 'textAlign':'left'} for c in ['年','月','樣區編號','樣站編號']],
                    filter_action='native',
                    sort_action='native',
                ),
            ],className='card-body')
        ], className='col col-lg-6 card border-secondary mb-3'),
    html.Div([
        html.Div([
            html.H4('鳥類調查樣區',style={ 'text-align': 'center' }),
            html.Div(dcc.Graph(id='bs_map',figure=bs_map)),
        ],className='card-body')
    ],className='col col-lg-6 card border-secondary mb-3'),
    ],className='row'),
    html.Div([
        html.H5('物種比例',style={ 'text-align': 'center' },className='col col-lg-4'),
        html.H5('棲地比例',style={ 'text-align': 'center' },className='col col-lg-4'),
        html.H5('科名比例',style={ 'text-align': 'center' },className='col col-lg-4'),
    ], className='row'),     
    html.Div([
        html.Div([
            dcc.Graph(id='tree_bird', figure=tree_bird, config=dict(displayModeBar=False))
        ],className='col col-lg-4'),
        html.Div([
            dcc.Graph(id='tree_habitat', figure=tree_habitat, config=dict(displayModeBar=False))
        ],className='col col-lg-4'),
        html.Div([
            dcc.Graph(id='tree_family', figure=tree_family, config=dict(displayModeBar=False))
        ],className='col col-lg-4'),
    ], className='row'),
    html.Br(),
    html.Div([
        html.H5('總數趨勢圖',style={ 'text-align': 'left' }, className='col col-lg-4'),
        html.P('選擇分類單位:',style={ 'text-align': 'right' }, className='col col-lg-4'),
        html.Div([
            dcc.Dropdown(
                id = 'UnitSelector',
                options=[
                    {'label': '樣區編號', 'value': '樣區編號'},
                    {'label': '樣站編號', 'value': '樣站編號'},
                    {'label': '物種', 'value': '名稱'},
                    {'label': '棲地型態', 'value': '棲地類型'},
                    {'label': '科名', 'value': '科名'},
                ],
                value='樣區編號',
                multi=False,
                placeholder="選擇分類單位"),
        ],className='col col-lg-4'),
    ],className='row'),
    dcc.Graph(id='bs_series',figure=bseries_fig, className='row'),
    ],className='col-10'),
    html.Div(className='col-1')
    ],className='row'),
    html.Br(),
    html.Br(),
    ],className='container-fluid')

    
@app.callback(
    Output('sdata', 'children'),
    [Input('bg_map', 'selectedData')])
def display_selected_data(selectedData):
    if selectedData:
        tt = [int(i['hovertext']) for i in selectedData['points']]
        return str(tt)[1:-1]
    else:
        return '請選擇地圖上的點位'

@app.callback(
        Output('water_fig','figure'),
        [Input('bg_map', 'selectedData'),
         Input('WaterParameter', 'value')])
def Update_WaterFigure(selectedData, value):
    if not selectedData:
        idl = [1]
    else:
        idl = [int(i['hovertext']) for i in selectedData['points']]
    return show_water_data(idl, value)

@app.callback(
        Output('water_fig_title','children'),
        [Input('bg_map', 'selectedData'),
         Input('WaterParameter', 'value')])
def Update_WaterFigureTitle(selectedData, value):
    para_names = ['溫度','導電度（mS/cm）','氧化還原電位（mV, ORP）','溶氧量（mg/L, DO）','溶氧度（%）','濁度（NTU）','酸鹼值（pH）','鹽度（ppt）','總固形物（g/L, TDS）','水深']
    V = para_names[value]
    if not selectedData:
        idl = [1]
    else:
        idl = [int(i['hovertext']) for i in selectedData['points']]
    dd = str(idl)
    text = d(f"""
             {V}:
                 
            包含樣站: {dd[1:-1]}
    """)
    return text

@app.callback(
        Output('tree_bird','figure'),
        [Input('bird_table','derived_virtual_data')])
def Update_BirdTree(rows):
    if rows is None:
        dff = bird_df
    else:
        dff = pd.DataFrame(rows)
    
    if len(dff) == 0:
        dff = bird_df
    
    n,exp,v = parse_treemap_input(dff, C='名稱')
    tree = draw_tree9(v,n,exp)
    
    return tree
    
@app.callback(
        Output('tree_habitat','figure'),
        [Input('bird_table','derived_virtual_data')])
def Update_HabitatTree(rows):
    if rows is None:
        dff = bird_df
    else:
        dff = pd.DataFrame(rows)
    
    if len(dff) == 0:
        dff = bird_df
        
    n,exp,v = parse_treemap_input(dff, C='棲地類型')
    tree = draw_tree9(v,n,exp)
    
    return tree     

@app.callback(
        Output('tree_family','figure'),
        [Input('bird_table','derived_virtual_data')])
def Update_FamilyTree(rows):
    if rows is None:
        dff = bird_df
    else:
        dff = pd.DataFrame(rows)
    
    if len(dff) == 0:
        dff = bird_df
        
    n,exp,v = parse_treemap_input(dff, C='科名')
    tree = draw_tree9(v,n,exp)
    
    return tree

@app.callback(
    Output('bs_series','figure'),
    [Input('bird_table','derived_virtual_data'),
     Input('UnitSelector', 'value')])
def Update_BS_fig(rows, value):
    if rows is None:
        dff = bird_df
    else:
        dff = pd.DataFrame(rows)
    
    if len(dff) == 0:
        dff = bird_df
        
    bs_fig = draw_amount_series(dff, unit = value)
    
    return bs_fig 
    
if __name__ == '__main__':
    app.run_server(debug=False)
