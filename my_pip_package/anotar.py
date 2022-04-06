def anotartx():
    items=driver.find_elements_by_xpath('//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr')
                count=len(items)
                porhacer=[]
                if count>0:
                    for i in range(1,count,2):
                        try:
                            tipo=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td[3]').text
                            direccion=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td[2]/div').text
                            if tipo==banco and (direccion=='Sell' or direccion=='Salida' or direccion=='Salidas'):
                                try:
                                    txid=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[1]/div[1]/div[1]/div[1]/p').text
                                    motivo=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[1]/div[1]/div[1]/div[1]/div/p').text
                                except NoSuchElementException:
                                    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="root"]/div[1]/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td[8]/button')))
                                    driver.find_element(By.XPATH,f'//*[@id="root"]/div[1]/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td[8]/button').click()
                                    WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[1]/div[1]/div[1]/div[1]/div/p')))
                                    motivo=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[1]/div[1]/div[1]/div[1]/div/p').text
                                pagados=[]
                                porcancelar=[]
                                fila=1
                                realizados=sheetrealizados.get_all_records()
                                for objeto in realizados:
                                    fila+=1
                                    objeto['FILA']=fila
                                    if objeto['ESTADO']=='PAGADO' or objeto['ESTADO']=='REPORTANDO':
                                        pagados.append(objeto)
                                    if objeto['ESTADO']=='CANCELAR':
                                        porcancelar.append(objeto)
                                if len(realizados)>20:
                                    for objeto in realizados[-20:]:
                                        if objeto['ESTADO']=='COMPLETADO' and objeto['FILA']!='':
                                            pagados.append(objeto)
                                        if objeto['ESTADO']=='CANCELADO' and objeto['FILA']!='' and objeto['REFERENCIA']!='':
                                            porcancelar.append(objeto)
                                else:
                                    for objeto in realizados:
                                        if objeto['ESTADO']=='COMPLETADO' and objeto['FILA']!='':
                                            pagados.append(objeto)
                                        if objeto['ESTADO']=='CANCELADO' and objeto['FILA']!='' and objeto['REFERENCIA']!='':
                                            porcancelar.append(objeto)
                                pagos=sheetpagos.get_all_records()
                                fila=1
                                for pago in pagos:
                                    fila+=1
                                    pago['FILA']=fila
                                rsv=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[1]/div[1]/div[1]/div[4]/div/p').text
                                rsv=round(float(rsv),2) 
                                titular=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[1]/div[1]/div[5]/div/div[1]/div/p').text
                                identificador=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[1]/div[1]/div[5]/div/div[2]/div/p').text
                                idBeneficiario=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[1]/div[1]/div[5]/div/div[3]/div/p').text
                                idBeneficiario=idBeneficiario.replace('.','')           
                                cuenta=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[1]/div[1]/div[5]/div/div[5]/div/p').text
                                cuenta=str(cuenta)
                                cuenta=cuenta.replace(' ','')
                                cuenta=cuenta.replace('-','')
                                porhacer.append(motivo)
                                monto=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td[4]/div').text
                                monto=monto.split(' ')[0].replace('.','')
                                monto=monto.replace(',','.')
                                monto=monto.replace(' ','')
                                monto=round(float(monto),2)
                                transaction_id=datetime.now()
                                transaction_id=transaction_id.strftime("%m/%d/%Y %H:%M")
                                if motivo not in anotados and cuenta[:4]==codigobanco and monto<=limite and len(str(motivo))>4:
                                    tipo=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td[3]').text
                                    direccion=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td[2]/div').text
                                    if tipo==banco and (direccion=='Sell' or direccion=='Salida' or direccion=='Salidas'):
                                        anotados.append(str(motivo))
                                        sheetpagos.append_row([transaction_id,motivo,titular,identificador,idBeneficiario,cuenta,monto,rsv,'','','','',nombreplat])
                                    driver.find_element(By.XPATH,f'//*[@id="root"]/div[1]/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td[8]/button').click()
                                    time.sleep(3.3)
                                    continue
                                completado=False
                                if pagados:
                                    for pago in pagados:
                                        if motivo==str(pago['TX RSV']):
                                            pago['ESTADO']='REPORTANDO'
                                            inputtxt=driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div/input')
                                            time.sleep(0.1)
                                            inputtxt.send_keys(Keys.CONTROL+'a')
                                            time.sleep(0.1)
                                            refrep=re.sub("[^0-9]", "", str(pago['REFERENCIA']))
                                            refrep=str(int(refrep)).rjust(9,'0')
                                            inputtxt.send_keys(refrep)
                                            time.sleep(0.1)
                                            driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[2]/div[1]/div/div/div[3]/button').click()
                                            pago['ESTADO']='COMPLETADO'
                                            sheetrealizados.update_cell(pago['FILA'],9,pago['ESTADO'])
                                            sheetrealizados.update_cell(pago['FILA'],8,refrep)
                                            completado=True
                                            break
                                if porcancelar and completado==False:
                                    for cancelado in porcancelar:
                                        if motivo==str(cancelado['TX RSV']):
                                            cancelado['ESTADO']='CANCELANDO'
                                            referencia=cancelado['REFERENCIA']
                                            if referencia=='ERROR EN CUENTA':
                                                referencia=1
                                            else:
                                                referencia=2
                                            sheetrealizados.update_cell(cancelado['FILA'],9,cancelado['ESTADO'])
                                            driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[2]/div[2]/div/div/div/div').click()
                                            driver.find_element(By.XPATH,f'//*[@id="menu-"]/div[3]/ul/li[{referencia}]').click()
                                            driver.find_element(By.XPATH,f'//*[@id="root"]/div/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i+1}]/td/div/div/div/div/div[2]/div[2]/div/button').click()
                                            cancelado['ESTADO']='CANCELADO'
                                            sheetrealizados.update_cell(cancelado['FILA'],9,cancelado['ESTADO'])
                                            completado=True
                                            break
                                if completado!=True:
                                    driver.find_element(By.XPATH,f'//*[@id="root"]/div[1]/main/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]/td[8]/button').click()
                                time.sleep(6.5)
                        except:
                            time.sleep(1)
                time.sleep(2)
