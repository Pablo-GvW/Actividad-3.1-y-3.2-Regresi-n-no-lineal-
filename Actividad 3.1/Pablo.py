############# Funcion para vargar un acrhivo como un dataframe########
def cargar_dataset(archivo):
    import pandas as pd
    import os
    extension = os.path.splitext(archivo)[1].lower() #con os recupera la parte despues del punto
    if extension ==".csv":
        df=pd.read_csv(archivo)
        return(df)
    elif extension ==".xlsx":
        df=pd.read_excel(archivo)
        return(df)
    elif extension ==".json":
        df=pd.read_json(archivo)
        return(df)
    elif extension ==".html":
        df=pd.read_html(archivo)
        return(df)
    else:
        raise ValueError(f"Formato de archivo no soportado{extension}")
    
#cuenta de valores
def cuenta_valores_nulos(dataframe): 
    import pandas as pd
    #por columna
    valores_nulos_cols = dataframe.isnull().sum()
    #por dataframe
    valores_nulos_df = dataframe.isnull().sum().sum()

    return("Valores nulos por columna", valores_nulos_cols,
           "valores nulos por dataframe", valores_nulos_df)


###########Bfill#########
def sustitucion_bfill(dataframe, cols):  
    for col in cols:  
        data_type = dataframe[col].dtype  
        if (data_type == "object") | (data_type == "category")|(data_type == "int64") | (data_type == "float64"):  
            dataframe[col] = dataframe[col].fillna(method="bfill")  
    return dataframe  

###########ffill#########
def sustitucion_ffill(dataframe, cols):  
    for col in cols:  
        data_type = dataframe[col].dtype  
        if (data_type == "object") | (data_type == "category")|(data_type == "int64") | (data_type == "float64"):  
            dataframe[col] = dataframe[col].fillna(method="ffill") 
    return dataframe  

###########string concreto#########
def sustitucion_string_concreto(dataframe, cols):  
    for col in cols:  
        data_type = dataframe[col].dtype  
        if (data_type == "object") | (data_type == "category"):  
            dataframe[col] = dataframe[col].fillna("f")
    return dataframe  


###########promedio#########
def sustitucion_promedio(dataframe, cols):  
    for col in cols:  
        data_type = dataframe[col].dtype  
        if (data_type == "int64") | (data_type == "float64"):  
            mean_value = dataframe[col].mean()    
            dataframe[col] = dataframe[col].fillna(round(mean_value, 1)) 
    return dataframe 

###########mediana#########
def sustitucion_mediana(dataframe, cols):  
    for col in cols:  
        data_type = dataframe[col].dtype  
        if (data_type == "int64") | (data_type == "float64"):  
            mediana_value = dataframe[col].median()    
            dataframe[col] = dataframe[col].fillna(round(mediana_value, 1)) 
    return dataframe 

###########constante########
def sustitucion_constante(dataframe, cols):  
    for col in cols:  
        data_type = dataframe[col].dtype  
        if (data_type == "int64") | (data_type == "float64"):  
            dataframe[col] = dataframe[col].fillna(0)
    return dataframe 

def sustitucion_constante_fuera_de_rango(dataframe, cols):  
    for col in cols:  
        data_type = dataframe[col].dtype  
        if (data_type == "int64") | (data_type == "float64")| (data_type == "object") | (data_type == "category"):  
            dataframe[col] = dataframe[col].fillna(99)
    return dataframe 

#########Sustitución de Atípicos############ 

def sustitucion_valores_atipicos(df):
    import pandas as pd
    cuantitativos = df.select_dtypes(include=['float', 'float64', 'int', 'int64'])
    cualitativos = df.select_dtypes(include=['object', 'datetime', 'category'])
    for columnas in cuantitativos:
        
        percentile25 = cuantitativos[columnas].quantile(0.25) #Q1
        percentile75 = cuantitativos[columnas].quantile(0.75) #Q3
        iqr = percentile75 - percentile25
        Limite_Superior_iqr = percentile75 + 1.5*iqr
        Limite_Inferior_iqr = percentile25 - 1.5*iqr
        print("Limite superior permitido", Limite_Superior_iqr)
        print("Limite inferior permitido", Limite_Inferior_iqr)
        cuanti_limpio = cuantitativos[(cuantitativos<=Limite_Superior_iqr)&(cuantitativos>=Limite_Inferior_iqr)]
        df_limpio1 = cuanti_limpio.fillna(round(cuanti_limpio.mean(),1))
        df_limipio = pd.concat([cualitativos, df_limpio1], axis=1)
    return df_limipio

def limpiar_porcentaje(x):
    import pandas as pd
    if isinstance(x, str) and '%' in x:
        return float(x.strip('%')) / 100
    return pd.to_numeric(x, errors='coerce')