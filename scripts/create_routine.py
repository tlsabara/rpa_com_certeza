#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import selenium.common.exceptions as SeleniumErrors
from datetime import datetime
from time import sleep

# Global Context

url_site = 'https://cotz.com.br/'

# Login Context
input_username = '//*[@id="login"]'
input_password = '//*[@id="pass"]'
btn_login = '//button[@class="btt_contained btt_plus"]'


# Register Hour Context
# year have 04 digits
# month have 02 digits
url_to_register_hours = 'https://cotz.com.br/obj.php?obj=acao_evento&op=calendario&mes={month}&ano={year}'
btn_add_actions = '//*[@id="add_acao_evento"]'

# Form to register action
linked_user = '//*[@id="p_v"]'
linked_user_options = '//select[@id="p_v"]/option'
linked_project = '//*[@id="i_pro"]'
linked_project_options = '//*[@id="i_pro"]/option'
linked_event = '//*[@id="i_e"]'
linked_event_options = '//*[@id="i_e"]/option'
linked_date = '//*[@id="d_a_e"]'
responsable = '//*[@id="i_u_r"]'
activity_description = '//*[@id="richText_dsc_c"]/div'
hours_company = '//*[@id="t_h"]'
hours_on_client = '//*[@id="t_h_p"]'
hours_on_homeoffice = '//*[@id="t_h_o"]'
check_send_mail = '//*[@id="e_resp_com"]'
btn_register_task = '//*[@id="btnCreate"]'
div_conteudo = '//div[@id="conteudo"]'

# Exec Variables
value_username = 'thiago.sabara@4mti.com.br'
value_password = 'NOVAnuptg09'

browser = webdriver.Chrome()

# Acessar o site
browser.maximize_window()
wait = WebDriverWait(browser, 15)
browser.get(url_site)

# Fazer o login
browser.find_element(By.XPATH, input_username).send_keys(value_username)
browser.find_element(By.XPATH, input_password).send_keys(value_password)
browser.implicitly_wait(.5)
browser.find_element(By.XPATH, btn_login).click()
wait.until(ec.visibility_of_element_located((By.XPATH, div_conteudo)))

# Acessar a página de registro
browser.get(url_to_register_hours.format(month='06', year='2023'))
btn_add = wait.until(ec.visibility_of_element_located((By.XPATH, btn_add_actions)))

# Abrir o formulário de registro
btn_add.click()
select_linked_user = wait.until(ec.visibility_of_element_located((By.XPATH, linked_user)))


# realizar o registro

## Selecionar pessoa vinculada
value_select = 'Enforce Group'
select_linked_user.click()
browser.implicitly_wait(.5)
for i in browser.find_elements(By.XPATH, linked_user_options):
    if i.text == value_select:
        i.click()
        break
# select_linked_user.click()

## Selecionar o projeto
value_select = 'Dataself'
browser.find_element(By.XPATH, linked_project).click()
for i in browser.find_elements(By.XPATH, linked_project_options):
    if i.text == value_select:
        i.click()
        break
# browser.find_element(By.XPATH, linked_project).click()

## Selecionar o evento
value_select = 'Desenvolvimento'
browser.find_element(By.XPATH, linked_event).click()
for i in browser.find_elements(By.XPATH, linked_event_options):
    if i.text == value_select:
        i.click()
        break

## Selecionar a data
value_date = datetime(2023, 6, 27).strftime('%d/%m/%Y')

browser.find_element(
    By.XPATH,
    linked_date
).clear()

browser.find_element(
    By.XPATH,
    linked_date
).send_keys(value_date)

## Aplicar a descrição da atividade
value_text = """
Correção de Merges
Correção do Pipeline
Issue #2699 e #2701
Correção de BUGs
"""
browser.find_element(
    By.XPATH,
    activity_description
).clear()

browser.find_element(
    By.XPATH,
    activity_description
).send_keys(value_text)

## Aplicar as horas de execução
value_hours_company = "08:35"
if value_hours_company:
    browser.find_element(
        By.XPATH,
        hours_company
    ).clear()

    browser.find_element(
        By.XPATH,
        hours_company
    ).send_keys(value_hours_company)

value_hours_client = "00:00"
if value_hours_company:
    browser.find_element(
        By.XPATH,
        hours_on_client
    ).clear()

    browser.find_element(
        By.XPATH,
        hours_on_client
    ).send_keys(value_hours_client)

value_hours_homeoffice = "00:00"
if value_hours_company:
    browser.find_element(
        By.XPATH,
        hours_on_homeoffice
    ).clear()

    browser.find_element(
        By.XPATH,
        hours_on_homeoffice
    ).send_keys(value_hours_homeoffice

## Check de envio de email
value_inform_mail = False

if value_inform_mail:
    browser.find_element(
        By.XPATH,
        check_send_mail
    ).click()

## Submeter o fomulário
browser.find_element(By.XPATH, btn_register_task).click()

sleep(5)

alert = Alert(browser)
alert_text = alert.text

success_message = 'Ação do evento cadastrada com sucesso!'

if alert_text == success_message:
    alert.accept()


