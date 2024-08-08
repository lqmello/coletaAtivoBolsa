from flask import Flask, render_template,request,redirect,url_for
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
from time import sleep
import pandas as pd

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    ativo = request.form['ativo']

    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager().install()),
        options=options
    )

    driver.get(
        'https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados'
        '/market-data/cotacoes/outros-ativos.htm'
    )

    ativo = ativo.upper().split(',')
    empresas = ativo
    valores = list()
    data_cotacao = list()
    hora_cotacao = list()
    oscilacao_cotacao = list()
    index=0

    for empresa in empresas:
        input_busca = driver.find_element(By.ID,"txtCampoPesquisa")
        input_busca.send_keys(empresa,Keys.CLEAR,Keys.ENTER)
        sleep(.1)
        span_val = driver.find_element(By.ID,"cotacaoAtivo")

        input_busca = driver.find_element(By.ID,"txtCampoPesquisa").clear()

        cotacao_valor = span_val.text

        data = driver.find_element(By.ID,"dataConsulta").text
        hora = driver.find_element(By.ID,"horaConsulta").text
        oscilacao = driver.find_element(By.ID,"oscilacaoAtivo").text
        valores.append(cotacao_valor)
        data_cotacao.append(data)
        hora_cotacao.append(hora)
        oscilacao_cotacao.append(oscilacao)

    dados = {
        'empresa': empresas,
        'valor': valores,
        'data': data_cotacao,
        'hora': hora_cotacao,
        'oscilacao': oscilacao_cotacao
    }
    df_empresas = pd.DataFrame(dados)
    df_empresas = df_empresas.style.to_html(classes='table striped', escape=False, justify="left")
    format_html = open('templates/saida.html','w')
    format_html.write(df_empresas)
    format_html.close()
    return redirect(url_for('saida'))

@app.route('/saida')
def saida():
    return render_template('saida.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)