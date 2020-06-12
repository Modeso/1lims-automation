from ui_testing.testcases.base_test import BaseTest
from ui_testing.pages.my_profile_page import MyProfile
from ui_testing.pages.header_page import Header
from api_testing.apis.users_api import UsersAPI
from parameterized import parameterized
from api_testing.apis.base_api import BaseAPI


class MyProfileTestCases(BaseTest):
    def setUp(self):
        super().setUp()
        self.header_page = Header()
        self.my_profile_page = MyProfile()
        self.users_api = UsersAPI()
        # generate random username/email & password
        self.username = self.generate_random_string()
        self.email = self.header_page.generate_random_email()

        response, payload = self.users_api.create_new_user(username=self.username, emai=self.email)
        self.current_password = payload["password"]
        self.info('create User {}:{}'.format(self.username, self.current_password))

        self.users_api._get_authorized_session(username=self.username, password=self.current_password, reset_token=True)
        self.set_authorization(auth=self.users_api.AUTHORIZATION_RESPONSE)

        self.my_profile_page.get_my_profile_page()

    # Blocked by https://modeso.atlassian.net/browse/LIMS-6425
    # def tearDown(self):
    #     self.users_api.delete_active_user(id=self.userId)
    #     return super().tearDown()

    def test001_user_can_change_password_and_press_on_cancel(self):
        """
        My Profile: Make sure after you change the password and press on cancel button, 
        the password shouldn't change

        LIMS-6091
        """
        # new password value
        self.new_password = self.my_profile_page.generate_random_text()

        # change the password value
        self.my_profile_page.change_password(self.current_password, self.new_password)

        # try to authorize with the new password
        baseAPI = BaseAPI()
        with self.assertRaises(KeyError) as e:
            baseAPI._get_authorized_session(username=self.base_selenium.username, password=self.new_password, reset_token=True)

    def test002_my_profile_should_show_username_and_email(self):
        """
        My Profile: Make sure that the user name & email displayed above the language

        LIMS-6090
        """
        username = self.base_selenium.get_text(element='my_profile:username')
        self.info('Check the username is {}'.format(self.username))
        self.assertEqual(username.lower(), self.username.lower())

        email = self.base_selenium.get_text(element='my_profile:email')
        self.info('Check the email is {}'.format(self.email))
        self.assertTrue(email.lower(), self.email.lower()) 

    def test003_user_can_change_password_and_login_successfully(self):
        """
        My Profile: Make sure that you can change the password 
        and login with the new one successfully 

        LIMS-6084
        """
        # new password value
        new_password = self.my_profile_page.generate_random_text()

        # change password
        self.my_profile_page.change_password(self.current_password, new_password, True)

        # Authorize
        baseAPI = BaseAPI()
        auth_token = baseAPI._get_authorized_session(username=self.base_selenium.username, password=new_password)
        
        # check if the auth token has value
        self.assertTrue(auth_token)

    @parameterized.expand(['EN', 'DE'])
    def test004_user_can_change_the_language(self, lang):
        """
        My Profile: Language Approach: Make sure that you can change language

        LIMS-6089
        """
        # change the EN to DE
        self.my_profile_page.chang_lang('DE')
        
        if lang == 'EN':
            # change the DE to EN
            self.my_profile_page.chang_lang('EN')
        
        # get page name
        page_name = self.base_selenium.get_text('my_profile:page_name')

        if lang == 'EN':
            self.assertEqual(page_name, 'My Profile') 
        else:
            self.assertEqual(page_name, 'Mein Profil')

    def test005_company_profile_upload_file_then_cancel_should_not_save(self):
        """
        My Profile: Signature Approach: Make sure after you upload the signature 
        & press on cancel button, this signature didn't submit
        
        LIMS-6086
        """
        # open signature tab
        self.base_selenium.click('my_profile:signature_tab')

        # choose file from assets to be uploaded
        file_name = 'logo.png'

        # upload the file then cancel
        self.my_profile_page.upload_file(
            file_name=file_name, drop_zone_element='my_profile:signature_field', save=False, remove_current_file=True)

        # go back to the company profile
        self.my_profile_page.get_my_profile_page()

        # open signature tab
        self.base_selenium.click('my_profile:signature_tab')

        # check that the image is not saved
        is_the_file_exist = self.base_selenium.check_element_is_exist(
            element='general:file_upload_success_flag')
        self.assertFalse(is_the_file_exist)

    def test007_my_profile_user_can_upload_logo(self):
        """
        My Profile: Signature Approach: Make sure that you can upload the signature successfully
        LIMS-6085
        """
        # open signature tab
        self.base_selenium.click('my_profile:signature_tab')
        # choose file from assets to be uploaded
        file_name = 'logo.png'
        # upload the file then save
        uploaded_file_name = self.my_profile_page.upload_file(
            file_name=file_name, drop_zone_element='my_profile:signature_field', save=True, remove_current_file=True)
        # check that the uploaded file has the same name as file choosed
        self.assertEqual(uploaded_file_name, file_name)
        
    def test008_my_profile_user_can_update_logo(self):
        """
        My Profile: Signature Approach: Make sure that you can remove any signature
        LIMS-6095
        """
        # open signature tab
        self.base_selenium.click('my_profile:signature_tab')

        # choose file from assets to be uploaded
        file_name = 'logo.png'

        # upload the first file
        uploaded_file_name =self.my_profile_page.upload_file(
            file_name=file_name, drop_zone_element='my_profile:signature_field', save=True, remove_current_file=True)

        # remove the file
        self.base_selenium.click('general:remove_file')
        self.my_profile_page.save()      

        # get array of all uploded files
        is_the_file_exist = self.base_selenium.check_element_is_exist(
            element='general:file_upload_success_flag')

        # there is no files
        self.assertFalse(is_the_file_exist)

    def test009_you_cant_upload_more_than_one_logo(self):
        """
        My Profile: Signature Approach: Make sure you can't download more than one signature
        LIMS-6087
        """
        # open signature tab
        self.base_selenium.click('my_profile:signature_tab')
        # choose file from assets to be uploaded
        file_name = 'logo.png'
        other_file_name = 'logo2.png'

        # upload the first file
        uploaded_file_name = self.my_profile_page.upload_file(
            file_name=file_name, drop_zone_element='my_profile:signature_field', save=True, remove_current_file=True)

        # upload other file beside the current one
        uploaded_other_file_name = self.my_profile_page.upload_file(
            file_name=other_file_name, drop_zone_element='my_profile:signature_field', save=True, remove_current_file=False)

        # wait to see if the file upload
        self.my_profile_page.sleep_medium()

        # get array of all uploded files
        files_uploaded_flags = self.base_selenium.find_elements('general:files_upload_success_flags')

        # only 1 file should be uploded
        self.assertEqual(len(files_uploaded_flags), 1)