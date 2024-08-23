import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
    comfort_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    comfort_perks = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[1]')
    phone_number_button = (By.CLASS_NAME, "np-button")
    phone_number = (By.ID, 'phone')
    next_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
    code_phone_number_input = (By.ID, 'code')
    confirm_phone_number = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
    card = (By.CLASS_NAME, 'pp-button.filled')
    add_card = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]')
    digits_card = (By.XPATH, '//*[@id="number"]')
    digits_code_card = (By.NAME, 'code')
    closed_card_method_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    add_card_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    select_outside_the_CVV_code = (By.CLASS_NAME, 'section.active.unusual')
    payment_method = (By.CLASS_NAME, 'pp-value-text')
    comment_to_driver = (By.ID, 'comment')
    comment_to_driver_button = (By.CLASS_NAME, 'input-container')
    request_blankets_and_tissues_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[1]')
    blankets_and_handkerchiefs_label = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]')
    ice_cream_button_selection = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    call_a_taxi_load_page = (By.CLASS_NAME, 'smart-button-wrapper')

    # Para colocar destino inicial y final en la app
    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    # Para seleccionar comfort taxi

    def click_request_taxi_button(self):
        self.driver.find_element(*self.request_taxi_button).click()

    def click_select_comfort_button(self):
        self.driver.find_element(*self.comfort_button).click()

    def validated_comfort_choice_with_perks(self):
        return self.driver.find_element(*self.comfort_perks).text

    def set_comfort_option(self):
        self.click_request_taxi_button()
        self.click_select_comfort_button()

    # Para colocar telefono en la app
    def click_phone_number_button(self):
        self.driver.find_element(*self.phone_number_button).click()
        time.sleep(2)
    def placed_phone_number(self):
        self.driver.find_element(*self.phone_number).send_keys(data.phone_number)
        time.sleep(2)

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()
        time.sleep(2)

    def placed_phone_code(self):
        self.driver.find_element(*self.code_phone_number_input).send_keys(retrieve_phone_code(self.driver))
        time.sleep(2)

    def click_confirm_phone_number(self):
        self.driver.find_element(*self.confirm_phone_number).click()
        time.sleep(2)

    def validated_phone_number(self):
        return self.driver.find_element(*self.phone_number_button).text

    def set_phone_number(self):
        self.click_phone_number_button()
        self.placed_phone_number()
        self.click_next_button()
        self.placed_phone_code()
        self.click_confirm_phone_number()

    # Para colocar tarjeta de pago en la app

    def click_card_button(self):
        self.driver.find_element(*self.card).click()

    def click_add_card(self):
        self.driver.find_element(*self.add_card).click()
        time.sleep(2)

    def placed_digits_card(self):
        self.driver.find_element(*self.digits_card).send_keys(data.card_number)
        time.sleep(2)

    def placed_digits_code_card(self):
        self.driver.find_element(*self.digits_code_card).send_keys(data.card_code)
        time.sleep(2)
    def click_add_card_button(self):
        self.driver.find_element(*self.select_outside_the_CVV_code).click()
        self.driver.find_element(*self.add_card_button).click()
        time.sleep(3)

    def click_closed_card_method_button(self):
        self.driver.find_element(*self.closed_card_method_button).click()

    def validated_payment_method(self):
        return self.driver.find_element(*self.payment_method).text

    def set_card_method_payment(self):
        self.click_card_button()
        self.click_add_card()
        self.placed_digits_card()
        self.placed_digits_code_card()
        self.click_add_card_button()
        self.click_closed_card_method_button()

    # Para colocar comentario a conductor en la app
    def placed_comment_to_driver(self):
        self.driver.find_element(*self.comment_to_driver).send_keys(data.message_for_driver)

    def validated_comment_to_driver(self):
        return self.driver.find_element(*self.comment_to_driver_button).text

    def set_comment_to_driver(self):
        self.placed_comment_to_driver()

    # Solicitar mantas y panuelos en la app
    def wait_for_load_label_blankets_and_handkerchiefs(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.blankets_and_handkerchiefs_label))

    def click_request_blankets_and_handkerchiefs_button(self):
        self.driver.find_element(*self.blankets_and_handkerchiefs_label).click()
    def set_request_blankets_and_handkerchiefs(self):
        self.wait_for_load_label_blankets_and_handkerchiefs()
        self.click_request_blankets_and_handkerchiefs_button()

    # Solicitar nieve en la app
    def wait_for_load_label_ice_cream(self):
        WebDriverWait(self.driver,3).until(expected_conditions.visibility_of_element_located(self.ice_cream_button_selection))

    def click_ice_cream_button_twice(self):
        self.driver.find_element(*self.ice_cream_button_selection).click()
        self.driver.find_element(*self.ice_cream_button_selection).click()

    def set_request_ice_cream(self):
        self.wait_for_load_label_ice_cream()
        self.click_ice_cream_button_twice()

    # Para confirmar que aparece boton de "Call a taxi"

    def call_a_taxi_button_visibility(self):
        return self.driver.find_element(*self.call_a_taxi_load_page).text

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()  #desired_capabilities=capabilities "No permitia correr las pruebas"

    def test_1_set_route(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(5)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_2_comfort_button(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(3)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        time.sleep(3)
        routes_page.set_comfort_option()
        time.sleep(3)
        comfort_text_perks = routes_page.validated_comfort_choice_with_perks()
        assert comfort_text_perks == 'Blanket and handkerchiefs'

    def test_3_phone_number(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(3)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        time.sleep(3)
        routes_page.set_comfort_option()
        time.sleep(3)
        comfort_text_perks = routes_page.validated_comfort_choice_with_perks()
        assert comfort_text_perks == 'Blanket and handkerchiefs'
        routes_page.set_phone_number()
        phone_number_validation = routes_page.validated_phone_number()
        assert phone_number_validation == '+1 123 123 12 12'

    def test_4_card_method_payment(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(3)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        time.sleep(3)
        routes_page.set_comfort_option()
        time.sleep(3)
        comfort_text_perks = routes_page.validated_comfort_choice_with_perks()
        assert comfort_text_perks == 'Blanket and handkerchiefs'
        routes_page.set_phone_number()
        phone_number_validation = routes_page.validated_phone_number()
        assert phone_number_validation == '+1 123 123 12 12'
        routes_page.set_card_method_payment()
        payment_method_validation = routes_page.validated_payment_method()
        assert payment_method_validation == 'Card'

    def test_5_placed_comment_to_driver(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(3)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        time.sleep(3)
        routes_page.set_comfort_option()
        time.sleep(3)
        comfort_validation_by_text_perks = routes_page.validated_comfort_choice_with_perks()
        assert comfort_validation_by_text_perks == 'Blanket and handkerchiefs'
        routes_page.set_phone_number()
        phone_number_validation = routes_page.validated_phone_number()
        assert phone_number_validation == '+1 123 123 12 12'
        routes_page.set_card_method_payment()
        payment_method_validation = routes_page.validated_payment_method()
        assert payment_method_validation == 'Card'
        routes_page.set_comment_to_driver()
        comment_to_driver_validation_error = routes_page.validated_comment_to_driver()
        assert comment_to_driver_validation_error == ''

    def test_6_select_blankets_and_handkerchiefs(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(3)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        time.sleep(3)
        routes_page.set_comfort_option()
        time.sleep(3)
        comfort_validation_by_text_perks = routes_page.validated_comfort_choice_with_perks()
        assert comfort_validation_by_text_perks == 'Blanket and handkerchiefs'
        routes_page.set_phone_number()
        phone_number_validation = routes_page.validated_phone_number()
        assert phone_number_validation == '+1 123 123 12 12'
        routes_page.set_card_method_payment()
        payment_method_validation = routes_page.validated_payment_method()
        assert payment_method_validation == 'Card'
        routes_page.set_comment_to_driver()
        comment_to_driver_validation_error = routes_page.validated_comment_to_driver()
        assert comment_to_driver_validation_error == ''
        routes_page.set_request_blankets_and_handkerchiefs()

    def test_7_select_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(3)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        time.sleep(3)
        routes_page.set_comfort_option()
        time.sleep(3)
        comfort_validation_by_text_perks = routes_page.validated_comfort_choice_with_perks()
        assert comfort_validation_by_text_perks == 'Blanket and handkerchiefs'
        routes_page.set_phone_number()
        phone_number_validation = routes_page.validated_phone_number()
        assert phone_number_validation == '+1 123 123 12 12'
        routes_page.set_card_method_payment()
        payment_method_validation = routes_page.validated_payment_method()
        assert payment_method_validation == 'Card'
        routes_page.set_comment_to_driver()
        comment_to_driver_validation_error = routes_page.validated_comment_to_driver()
        assert comment_to_driver_validation_error == ''
        routes_page.set_request_blankets_and_handkerchiefs()
        routes_page.set_request_ice_cream()

    def test_8_wait_for_call_a_taxi_active_button(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(3)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        time.sleep(3)
        routes_page.set_comfort_option()
        time.sleep(3)
        comfort_validation_by_text_perks = routes_page.validated_comfort_choice_with_perks()
        assert comfort_validation_by_text_perks == 'Blanket and handkerchiefs'
        routes_page.set_phone_number()
        phone_number_validation = routes_page.validated_phone_number()
        assert phone_number_validation == '+1 123 123 12 12'
        routes_page.set_card_method_payment()
        payment_method_validation = routes_page.validated_payment_method()
        assert payment_method_validation == 'Card'
        routes_page.set_comment_to_driver()
        comment_to_driver_validation_error = routes_page.validated_comment_to_driver()
        assert comment_to_driver_validation_error == ''
        routes_page.set_request_blankets_and_handkerchiefs()
        routes_page.set_request_ice_cream()
        time.sleep(3)
        description = routes_page.call_a_taxi_button_visibility()
        assert description == 'Call a taxi\nThe route will run 1 kilometers and take 1 minutes.'

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
