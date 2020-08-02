
#Este proceso esta hecho para obtener informacion sobre productos de CruzVerde para complementar informacion existente 

#Dependencias
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

def main(argu):
    #Parametros
    root_web = argu[0]
    driver_path = argu[1]

    #Set up
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    #Obtención de Lista de Tipos Medicamentos
    driver.get(root_web)
    sleep(5)
    BotonNoGracias = driver.find_element_by_id("onesignal-slidedown-cancel-button")
    BotonNoGracias.click()
    ElementosHTMLProductos = driver.find_elements_by_xpath("//a[contains(@class, 'basic-link basic-link--dark d-block')]")
    ListadeUrls = [element.get_attribute('href') for element in ElementosHTMLProductos]

    Lista_Agrupada = []

    for Tipo in ListadeUrls:
        driver.get("{Tipo}?start=0&sz=2000".format(Tipo=Tipo))
        sleep(2)
        _info_urls = [element.get_attribute("href")\
                    for element in driver.find_elements_by_xpath("//div[contains(@class, 'pdp-link')]//a[contains(@class, 'link')]")]
        _info_labs = [element.get_attribute("innerHTML")\
                    for element in driver.find_elements_by_xpath("//a[contains(@class, 'product-brand text-uppercase m-0')]")]
        Lista_Tipo = get_lista_final(Tipo, _info_urls, _info_labs)
        
        for elemento in Lista_Tipo:
            Lista_Agrupada.append(elemento)
        print("Tipo:{Tipo} esta completamente cargado.".format(Tipo=Tipo))
    
    #Cierre navegador
    driver.close()

    cabeceras = ['Id_producto','Producto','Laboratorio','Clasificacion']
    DataFrame_Final = pd.DataFrame(Lista_Agrupada, columns=cabeceras)
    DataFrame_Final.to_csv('OutputProductos.csv',index=False)
    print("Proceso Terminado")

    return 0

#Funcion para obtener la lista desde cada iteracion


def get_lista_final(Tipo, _info_urls, _info_labs):
    lista_final = []
    largo = len(_info_urls)
    for i in range(0,largo):
        codigo = _info_urls[i].split('/')[-1].split('.')[-2]
        producto = _info_urls[i].split('/')[-2]
        laboratorio = _info_labs[i].strip()
        clasificacion = Tipo.split('/')[-2]
        lista_final.append([codigo,producto,laboratorio,clasificacion])
    return lista_final


if __name__ == '__main__':
    main(sys.argv[1:3])

