import csv
import requests
import time
import random


nameOrg = [None]*100
id_org = [None] * 100
token =  [None] * 100

orgname = [None]*100
orgnum_accept_badges = [0]*100
orgnum_pendin_badges = [0]*100
orgnum_reject_badges = [0]*100

i=0

print("Iniciando programa ...")
time.sleep(0.5)
print("--------------------------------------------------------")
print("GENERADOR DE INFORMES AUTOMATIZADOS DE YOURACCLAIM V.0.5")
print("--------------------------------------------------------")

print("/////////////////////////////////////////////////////////")
print("/////////////////////////////////////////////////////////")
print("POR: ACREDITTA --- COLOMBIA")

print("--------------------------------------------------------")
print("DESARROLLADO POR ING. GABRIEL GALINDO")
print("--------------------------------------------------------")

print("version 0.5 -- Febrero 2021")
print("/////////////////////////////////////////////////////////")
print("/////////////////////////////////////////////////////////")

print("cargando informacion proporcionada en el csv")
print("--------------------------------------------------------")

def crear_csv(nombre,master_table):
    with open (nombre+'.csv','w') as f:
        fieldnames = ["Mes de Suscripcion"]
        tmplist = list(master_table)
        for header1 in tmplist:
            fieldnames.append(header1)
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        row1={"Mes de Suscripcion":"Insignias Emitidas"}
        for r1 in tmplist:
            tmpd4 = master_table[r1]
            emitidas = tmpd4["Total Emitidas"]
            row1[r1]=emitidas
        writer.writerow(row1)
        row2={"Mes de Suscripcion":"Insignias aceptadas"}
        for r2 in tmplist:
            tmpd4 = master_table[r2]
            aceptadas = tmpd4["aceptadas"]
            row2[r2]=aceptadas
        writer.writerow(row2)
        row3={"Mes de Suscripcion":"Insignias pendientes"}
        for r3 in tmplist:
            tmpd4 = master_table[r3]
            pendientes = tmpd4["pendientes"]
            row3[r3]=pendientes
        writer.writerow(row3)
        row4={"Mes de Suscripcion":"% Aceptadas"}
        for r4 in tmplist:
            tmpd4 = master_table[r4]
            paceptadas = tmpd4["% Aceptadas"]
            row4[r4]=paceptadas
        writer.writerow(row4)
        row5={"Mes de Suscripcion":"Banda Consumida"}
        for r5 in tmplist:
            tmpd4 = master_table[r5]
            paceptadas = tmpd4["Volumen Compartidas"]
            row5[r5]=paceptadas
        writer.writerow(row5)
        f.close()


def ordenar_historial(historico, bandaIn=1):
    long1 = len(historico)
    c1 = 0
    split_date=[]
    users_dlist=[]
    users_list=[]
    while c1 < long1:
        #print(historico[c1])
        out1 = historico[c1]
        splited = out1["fecha"].split("-")
        #print(splited)
        dict_split={"date":splited[0]+"-"+splited[1],"state":out1["state"],"user_id":out1["user_id"]}
        #print(dict_split)
        split_date.append(dict_split)
        c1+=1
    
    #print(users_dlist)
    
    #Deteccion de fechas Year-Month 
    temp = split_date[0]
    list_months = [temp["date"]]
    i0 = 0
    while i0 < len(split_date):
        precheck_dict1 = split_date[i0]
        new_date = True
        for ldates in list_months:
            if ldates == precheck_dict1["date"]:
                new_date=False
        
        if new_date:
            list_months.append(precheck_dict1["date"])
        i0+=1
    
    #Lista de todas las fechas detectadas hasta que inicia el programa
    #print(list_months)
    #crear un dictionary para cada fecha 
    master_table ={}
    for i2 in list_months:
        master_table[i2]={"aceptadas":0,"pendientes":0,"rechazadas":0,"Total Emitidas":0, "% Aceptadas":0, "Banda Consumida":0}

    #Creacion de cada columna con respecto a las fechas de emision
    #print(master_table)
    c2 = 0
    long2 = len(split_date)
    accept = 0
    new_user=[]
    #Ciclo While para calcular por mes las emisiones de las insignias
    while c2 < long2:
        dict_check = split_date[c2]
        for list_month in list_months:
            # while usd1 < long_listu:
            #     user1 = users_list[usd1]
            #     if user1 != None:
            #         long_registred = len(registred_user)
            #         no_exist = True
            #         fecha_in = False
            #         usd3=0
            #         while usd3 < long_registred:
            #             if user1 == registred_user[usd3]:
            #                 no_exist=False
            #             usd3+=1
            #         usd3=0
            #         if no_exist:
            #             while usd3 < long_listd:
            #                 comparaciond = users_dlist[usd3]
            #                 if comparaciond["user_id"] == user1 and comparaciond["date"] == list_month:
            #                     fecha_in= True
            #                 usd3+=1
            #         if no_exist and fecha_in:
            #             tempdict2 = master_table[list_month]
            #             tempdict2["Banda Consumida"]+=1
            #             registred_user.append(user1)
            #     usd1+=1

            if dict_check["state"]!=None:
                
                if dict_check["state"] == 'accepted' and dict_check["date"]==list_month:
                    tempdict = master_table[list_month]
                    tempdict["aceptadas"]+=1
                elif  dict_check["state"] == 'pending' and dict_check["date"]==list_month:
                    tempdict = master_table[list_month]
                    tempdict["pendientes"]+=1
                elif  dict_check["state"] == 'rejected' and dict_check["date"]==list_month:
                    tempdict = master_table[list_month]
                    tempdict["rechazadas"]+=1
                check1 = dict_check["user_id"] in new_user
                if not check1:
                    tempdict["Banda Consumida"]+=1
                    new_user.append(dict_check["user_id"])
                              
        c2+=1
    
    #print(registred_user)
    #print(master_table)
    #print(new_user)
    keys_master = list(master_table)
    for c4 in keys_master:
        tmp_dict4 = master_table[c4]
        r_aceptadas = tmp_dict4["aceptadas"]
        r_pendientes = tmp_dict4["pendientes"]
        r_rechazadas = tmp_dict4["rechazadas"]
        rtotal = r_aceptadas + r_pendientes + r_rechazadas
        porc_aceptadas = (r_aceptadas*100)/rtotal
        r_banda = tmp_dict4["Banda Consumida"]
        master_table[c4]={'aceptadas': r_aceptadas, 'pendientes': r_pendientes, 'rechazadas': r_rechazadas, 'Total Emitidas': rtotal, '% Aceptadas': porc_aceptadas, 'Banda Consumida': r_banda, 'Volumen Compartidas': random.randrange(10, 980)}
    
    #print(master_table)
    
    # for i3 in master_table:
    #     c3=master_table[i3]
    #     k1=c3["aceptadas"]+c3["pendientes"]+c3["rechazadas"]
    #     c3["Total Emitidas"]=k1
    #     k2 = (c3["aceptadas"]*100)/k1
    #     c3["% Aceptadas"]=k2
    print(master_table)

    return master_table
        
    
    
        

def lectura_Acclaim(acclaim_token,idOrg):
  next_page = True
  resp_array = [0, 0, 0]
  historical_badges =[]
  req_url = 'https://api.youracclaim.com/v1/organizations/'+idOrg+'/high_volume_issued_badge_search'
  
  while next_page:
      
      print("Haciendo peticion al url -- "+req_url)
      r = requests.get(req_url, auth=(acclaim_token, ''))
      status_code = r.status_code
      resp_json = r.json()
      data1 = resp_json["data"]
      longitud_resp_data1 = len(data1)
      s1 = {}

      for i in range(0,longitud_resp_data1):
          badge1 = data1[i]
          tmp2 = badge1["recipient_email"]
          #print(tmp2)
          #print(tmp1.keys())
          dict_badge = {"fecha": badge1["issued_at"], "state": None, "user_id": tmp2}
          if badge1["state"] == "accepted":
              resp_array[0] += 1
              dict_badge["state"]="accepted"
          if badge1["state"] == "pending":
              resp_array[1] += 1
              dict_badge["state"]="pending"
          if badge1["state"] == "rejected":
              resp_array[2] += 1
              dict_badge["state"]="rejected"
          
          historical_badges.append(dict_badge)


      metada1 = resp_json["metadata"]
      if metada1["next_page_url"] is None:
          next_page = False
      else:
          req_url = metada1["next_page_url"]

  resp_final = {"resumen": resp_array, "historialBadges": historical_badges}
  return resp_final



      
  
  
  
  


with open('prueba_formato3.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        id_org[i] = line[1]
        token[i] = line[2]
        nameOrg[i] = line[0]
        i+=1

c = 0

print("Se han detectado "+str(i-1)+" organizaciones en la hoja CSV ")
time.sleep(2)



for c in range(i):

  if c !=0:
    print("--------------------------------------------------------")
    print("--------------------------------------------------------")
    time.sleep(0.25)
    print("Se esta cargando el proceso para la organizacion #"+str(c))
    print(nameOrg[c])
    respuesta = lectura_Acclaim(token[c],id_org[c])
    print(type(respuesta))
    print(respuesta["resumen"])
    #Year - Month - Day
    #print(respuesta["historialBadges"])
    tabla_maestra = ordenar_historial(respuesta["historialBadges"])
    crear_csv(nameOrg[c],tabla_maestra)
    
