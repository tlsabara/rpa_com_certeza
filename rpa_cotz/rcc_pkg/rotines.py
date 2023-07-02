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
from typing import TypeVar

from rpa_cotz.loaders.config_loader import LoadData

SelfRPARegister = TypeVar('SelfRPARegister', bound='RPARegiter')


class RPARegister:
    """Classe para comportar o registro de uma nova atividade
    """
    url_site = 'https://cotz.com.br/'

    input_username = '//*[@id="login"]'
    input_password = '//*[@id="pass"]'
    btn_login = '//button[@class="btt_contained btt_plus"]'
    url_to_register_hours = 'https://cotz.com.br/obj.php?obj=acao_evento&op=calendario&mes={month}&ano={year}'
    btn_add_actions = '//*[@id="add_acao_evento"]'
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
    success_message = 'Ação do evento cadastrada com sucesso!'

    def __init__(self, configs: LoadData) -> None:
        self.browser = None
        self.configs = configs

        self.btn_add = None
        self.select_linked_user = None

    def __initialize_browser(self) -> object:
        """Inicializa o navegador
        """
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 15)
        return self

    def __access_site(self) -> SelfRPARegister:
        """Acesso ao site
        """
        self.browser.get(self.url_site)
        return self

    def __make_login(self) -> SelfRPARegister:
        """Controla o navegador com o objetivo de realizar o login
        """
        self.browser.find_element(By.XPATH, self.input_username).send_keys(self.configs.username)
        self.browser.find_element(By.XPATH, self.input_password).send_keys(self.configs.password)
        self.browser.implicitly_wait(.5)
        self.browser.find_element(By.XPATH, self.btn_login).click()
        self.wait.until(ec.visibility_of_element_located((By.XPATH, self.div_conteudo)))

        return self

    def __acces_calendar(self) -> SelfRPARegister:
        """chamada para acessar o calendário de atividades
        """
        month = f"{datetime.now().month:0>2}"
        year = f"{datetime.now().month:0>4}"
        self.browser.get(self.url_to_register_hours.format(month=month, year=year))
        self.btn_add = self.wait.until(ec.visibility_of_element_located((By.XPATH, self.btn_add_actions)))
        return self

    def __iter_parameters_file(self) -> SelfRPARegister:
        for record in self.configs.next_record():
            valid_insert = self.__insert_form(record)
            if not valid_insert:
                self.__acces_calendar()
                valid_insert = self.__insert_form(record)
            if not valid_insert:
                record.EXECUTION_STATUS = "FALHA"
            else:
                record.EXECUTION_STATUS = "OK"

    def __insert_form(self, record) -> bool:
        """Inicia a chamada da subrotina de inserir dados em um novo formulário
        """
        return self.__sub_open_form() \
            .__sub_select_linked_user(record.PESSOA) \
            .__sub_select_project(record.PROJETO) \
            .__sub_select_event(record.EVENTO) \
            .__sub_inset_date(record.DATA) \
            .__sub_insert_description(record.TEXTO_ATIVIDADE) \
            .__sub_insert_company_hours(record.HORAS_EMPRESA) \
            .__sub_insert_client_hours(record.HORAS_CLIENTE) \
            .__sub_insert_homeoffice_hours(record.HORAS_HOMEOFFICE) \
            .__sub_check_mail_inform(record.INFORM_MAIL) \
            .__sub_submit_form()

    def __sub_open_form(self) -> SelfRPARegister:
        """subrotina para abrir um novo formuário
        """
        self.btn_add.click()
        self.select_linked_user = self.wait.until(ec.visibility_of_element_located((By.XPATH, self.linked_user)))
        return self

    def __sub_select_linked_user(self, value_select: str) -> SelfRPARegister:
        """Seleciona a pessoa relecionada
        """
        self.select_linked_user.click()
        self.browser.implicitly_wait(.5)
        for i in self.browser.find_elements(By.XPATH, self.linked_user_options):
            if i.text == value_select:
                i.click()
                break
        # select_linked_user.click()
        return self

    def __sub_select_project(self, value_select: str) -> SelfRPARegister:
        """Seleciona o projeto relacionado
        """
        self.browser.find_element(By.XPATH, self.linked_project).click()
        for i in self.browser.find_elements(By.XPATH, self.linked_project_options):
            if i.text == value_select:
                i.click()
                break
        # browser.find_element(By.XPATH, linked_project).click()
        return self

    def __sub_select_event(self, value_select: str) -> SelfRPARegister:
        """Seleciona o evento relacionado
        """
        self.browser.find_element(By.XPATH, self.linked_event).click()
        for i in self.browser.find_elements(By.XPATH, self.linked_event_options):
            if i.text == value_select:
                i.click()
                break
        # browser.find_element(By.XPATH, self.linked_event.click()
        return self

    def __sub_inset_date(self, value_date: str) -> SelfRPARegister:
        """Insere a data da atividade
        """
        self.browser.find_element(
            By.XPATH,
            self.linked_date
        ).clear()
        self.browser.find_element(
            By.XPATH,
            self.linked_date
        ).send_keys(value_date)
        return self

    def __sub_insert_description(self, value_text: str) -> SelfRPARegister:
        """Insere a descrição da atividade
        """
        self.browser.find_element(
            By.XPATH,
            self.activity_description
        ).clear()

        self.browser.find_element(
            By.XPATH,
            self.activity_description
        ).send_keys(value_text)
        return self

    def __sub_insert_company_hours(self, value_hours_company: str = "00:00") -> SelfRPARegister:
        self.browser.find_element(
            By.XPATH,
            self.hours_company
        ).clear()

        self.browser.find_element(
            By.XPATH,
            self.hours_company
        ).send_keys(value_hours_company)
        return self

    def __sub_insert_client_hours(self, value_hours_client: str = "00:00") -> SelfRPARegister:
        self.browser.find_element(
            By.XPATH,
            self.hours_on_client
        ).clear()

        self.browser.find_element(
            By.XPATH,
            self.hours_on_client
        ).send_keys(value_hours_client)
        return self

    def __sub_insert_homeoffice_hours(self, value_hours_homeoffice: str = "00:00") -> SelfRPARegister:
        self.browser.find_element(
            By.XPATH,
            self.hours_on_homeoffice
        ).clear()

        self.browser.find_element(
            By.XPATH,
            self.hours_on_homeoffice
        ).send_keys(value_hours_homeoffice)
        return self

    def __sub_check_mail_inform(self, inform_mail: bool = False) -> SelfRPARegister:
        if inform_mail:
            self.browser.find_element(
                By.XPATH,
                self.check_send_mail
            ).click()
        return self

    def __sub_submit_form(self) -> bool:
        self.browser.find_element(By.XPATH, self.btn_register_task).click()

        sleep(5)

        alert = Alert(self.browser)
        alert_text = alert.text

        if alert_text == self.success_message:
            alert.accept()
            return True
        return False
