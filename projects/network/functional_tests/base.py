import time
from datetime import datetime
from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

User = get_user_model()

from selenium.common.exceptions import WebDriverException

MAX_WAIT = 5
SCREEN_DUMP_LOCATION = Path(__file__).parent/'screendumps'


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self) -> None:
        if self._test_has_failed():
            if not SCREEN_DUMP_LOCATION.exists():
                SCREEN_DUMP_LOCATION.mkdir()
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        # slightly obscure but couldn't find a better way!
        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshoting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        folder = SCREEN_DUMP_LOCATION
        classname = self.__class__.__name__
        method = self._testMethodName
        windowid = self._windowid
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return f'{folder}/{classname}.{method}-window{windowid}-{timestamp}'

    @wait
    def wait_for(self, fn):
        return fn()


class LoggedInFunctionalTest(FunctionalTest):

    def setUp(self) -> None:
        user = User.objects.create_user(
            username='harry',
            email='hpotter@test.com',
            password='password',
        )

        self.client.force_login(user)
        super().setUp(self)