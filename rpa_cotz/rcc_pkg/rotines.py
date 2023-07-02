import json

from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from time import sleep
from typing import TypeVar

from loaders.config_loader import LoadData

SelfRPARegister = TypeVar("SelfRPARegister", bound="RPARegiter")


class RPARegister:
    """Classe para comportar o registro de uma nova atividade"""

    TARGETS_NAMEFILE = "targets.json"

    url_site = None
    input_username = None
    input_password = None
    btn_login = None
    url_to_register_hours = None
    btn_add_actions = None
    linked_user = None
    linked_user_options = None
    linked_project = None
    linked_project_options = None
    linked_event = None
    linked_event_options = None
    linked_date = None
    responsable = None
    activity_description = None
    hours_company = None
    hours_on_client = None
    hours_on_homeoffice = None
    check_send_mail = None
    btn_register_task = None
    div_conteudo = None
    success_message = None

    def __init__(self, configs: LoadData) -> None:
        self.__targets_loader()
        self.browser = None
        self.configs = configs

        self.btn_add = None
        self.select_linked_user = None

    def __targets_loader(self) -> None:
        """Realiza o carregamento dos XPATHS para os atributos da classe"""
        with open(self.TARGETS_NAMEFILE, "r") as fl:
            targets_dict = json.loads("".join(fl.readlines()))
        self.__dict__.update(targets_dict)

    def register_today(self) -> None:
        """Realiza o registro para a data de hoje"""
        self.__initialize_browser().__access_site().__make_login().__access_calendar()
        return None

    def register_batch(self) -> None:
        """Realiza o registro em batch baseado no arquivo CSV indicado"""
        self.__initialize_browser().__access_site().__make_login().__access_calendar().__iter_parameters_file()

        return None

    def __initialize_browser(self) -> SelfRPARegister:
        """Inicializa o navegador"""
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 15)

        return self

    def __access_site(self) -> SelfRPARegister:
        """Acesso ao site"""
        self.browser.get(self.url_site)

        return self

    def __make_login(self) -> SelfRPARegister:
        """Controla o navegador para realizar o login"""
        self.browser.find_element(By.XPATH, self.input_username).send_keys(
            self.configs.username
        )
        self.browser.find_element(By.XPATH, self.input_password).send_keys(
            self.configs.password
        )
        self.browser.implicitly_wait(0.5)
        self.browser.find_element(By.XPATH, self.btn_login).click()
        self.wait.until(ec.visibility_of_element_located((By.XPATH, self.div_conteudo)))

        return self

    def __access_calendar(self) -> SelfRPARegister:
        """Chamada para acessar o calendário de atividades"""
        month = f"{datetime.now().month:0>2}"
        year = f"{datetime.now().month:0>4}"
        self.browser.get(self.url_to_register_hours.format(month=month, year=year))

        return self

    def __iter_parameters_file(self) -> None:
        """Itera sob os registros do CSV que atendem o requisito"""
        for record in self.configs.next_record():
            valid_insert = self.__insert_form(record)
            if not valid_insert:
                self.__acces_calendar()
                valid_insert = self.__insert_form(record)
            if not valid_insert:
                record.EXECUTION_STATUS = "FALHA"
            else:
                record.EXECUTION_STATUS = "OK"
                record.INSERIDO = True

                # TODO: Melhorar isso com o log
                print(f"Dia {record.DATA} inserido com sucesso")
        self.configs.save_df_data()
        print("DF de dados atualizado")

        return None

    def __insert_form(self, record) -> bool:
        """Inicia a chamada da subrotina de inserir dados em um novo formulário"""
        return (
            self.__sub_open_form()
            .__sub_select_linked_user(record.PESSOA)
            .__sub_select_project(record.PROJETO)
            .__sub_select_event(record.EVENTO)
            .__sub_inset_date(record.DATA)
            .__sub_insert_description(record.TEXTO_ATIVIDADE)
            .__sub_insert_company_hours(record.HORAS_EMPRESA)
            .__sub_insert_client_hours(record.HORAS_CLIENTE)
            .__sub_insert_homeoffice_hours(record.HORAS_HOMEOFFICE)
            .__sub_check_mail_inform(record.INFORM_MAIL)
            .__sub_submit_form()
        )

    def __sub_open_form(self) -> SelfRPARegister:
        """Subrotina para abrir um novo formuário"""
        self.btn_add = self.wait.until(
            ec.visibility_of_element_located((By.XPATH, self.btn_add_actions))
        )
        self.btn_add.click()
        self.select_linked_user = self.wait.until(
            ec.visibility_of_element_located((By.XPATH, self.linked_user))
        )
        return self

    def __sub_select_linked_user(self, value_select: str) -> SelfRPARegister:
        """Seleciona a pessoa relecionada"""
        self.select_linked_user.click()
        self.browser.implicitly_wait(0.5)
        for i in self.browser.find_elements(By.XPATH, self.linked_user_options):
            if i.text == value_select:
                i.click()
                break
        # select_linked_user.click()
        return self

    def __sub_select_project(self, value_select: str) -> SelfRPARegister:
        """Seleciona o projeto relacionado"""
        self.browser.find_element(By.XPATH, self.linked_project).click()
        for i in self.browser.find_elements(By.XPATH, self.linked_project_options):
            if i.text == value_select:
                i.click()
                break
        # browser.find_element(By.XPATH, linked_project).click()
        return self

    def __sub_select_event(self, value_select: str) -> SelfRPARegister:
        """Seleciona o evento relacionado"""
        self.browser.find_element(By.XPATH, self.linked_event).click()
        for i in self.browser.find_elements(By.XPATH, self.linked_event_options):
            if i.text == value_select:
                i.click()
                break
        # browser.find_element(By.XPATH, self.linked_event.click()
        return self

    def __sub_inset_date(self, value_date: str) -> SelfRPARegister:
        """Insere a data da atividade"""
        self.browser.find_element(By.XPATH, self.linked_date).clear()
        self.browser.find_element(By.XPATH, self.linked_date).send_keys(value_date)
        return self

    def __sub_insert_description(self, value_text: str) -> SelfRPARegister:
        """Insere a descrição da atividade"""
        self.browser.find_element(By.XPATH, self.activity_description).clear()

        self.browser.find_element(By.XPATH, self.activity_description).send_keys(
            value_text
        )
        return self

    def __sub_insert_company_hours(
        self, value_hours_company: str = "00:00"
    ) -> SelfRPARegister:
        """Insere o valor de horas na empresa"""
        self.browser.find_element(By.XPATH, self.hours_company).clear()

        self.browser.find_element(By.XPATH, self.hours_company).send_keys(
            value_hours_company
        )
        return self

    def __sub_insert_client_hours(
        self, value_hours_client: str = "00:00"
    ) -> SelfRPARegister:
        """Insere o valor de horas no cliente"""
        self.browser.find_element(By.XPATH, self.hours_on_client).clear()

        self.browser.find_element(By.XPATH, self.hours_on_client).send_keys(
            value_hours_client
        )
        return self

    def __sub_insert_homeoffice_hours(
        self, value_hours_homeoffice: str = "00:00"
    ) -> SelfRPARegister:
        """Insere o valor de horas em Homeoffice"""
        self.browser.find_element(By.XPATH, self.hours_on_homeoffice).clear()

        self.browser.find_element(By.XPATH, self.hours_on_homeoffice).send_keys(
            value_hours_homeoffice
        )
        return self

    def __sub_check_mail_inform(self, inform_mail: bool = False) -> SelfRPARegister:
        """Check no campo inform mail"""
        if inform_mail:
            self.browser.find_element(By.XPATH, self.check_send_mail).click()
        return self

    def __sub_submit_form(self) -> bool:
        """Envia o formulário"""
        self.browser.find_element(By.XPATH, self.btn_register_task).click()

        sleep(5)

        alert = Alert(self.browser)
        alert_text = alert.text

        if alert_text == self.success_message:
            alert.accept()
            return True
        return False
