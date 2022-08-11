import unittest
from unittest.mock import patch
from gofindme import create_api_url, flags, get_donations, get_number_donations
import json


class TestGofindme(unittest.TestCase):
    def setUp(self):
        self.test_flags = flags()
        self.test_flags.campaign = "https://www.gofundme.com/f/my-test-campaign"

    def tearDown(self):
        pass

    def test_api_url(self):
        api_url = create_api_url(self.test_flags.campaign)
        self.assertEqual(
            api_url,
            "https://gateway.gofundme.com/web-gateway/v1/feed/my-test-campaign/",
        )

    def test_get_number_donations(self):
        with patch("requests.get") as mocked_get:
            mocked_get.return_value.text = '{"references":{"counts":{"total_photos":2,"total_co_photos":2,"total_community_photos":0,"total_comments":2,"total_updates":13,"total_donations":64,"total_unique_donors":46,"amount_raised_unattributed":1735.0,"number_of_donations_unattributed":32,"campaign_hearts":82,"social_share_total":536}},"meta":{"last_updated_at":"2022-08-11T14:37:37.602266-05:00"}}'
            api_url = create_api_url(self.test_flags.campaign)
            number_of_donations = get_number_donations(api_url)
            self.assertEqual(number_of_donations, 64)

    def test_get_donations(self):
        with patch("requests.get") as mocked_get:
            mocked_get.return_value.text = '{"references":{"donations":[{"donation_id":922307279,"amount":25.0,"is_offline":false,"is_anonymous":false,"created_at":"2022-07-25T13:38:49-05:00","name":"Susan McTest","profile_url":"","verified":true,"currencycode":"USD","fund_id":60746401,"checkout_id":"102714322"},{"donation_id":921777937,"amount":100.0,"is_offline":false,"is_anonymous":false,"created_at":"2022-07-23T17:53:29-05:00","name":"Gabriel Testersmith","profile_url":"","verified":true,"currencycode":"USD","fund_id":60746401,"checkout_id":"102533348"},{"donation_id":918458065,"amount":15.0,"is_offline":false,"is_anonymous":false,"created_at":"2022-07-14T12:26:25-05:00","name":"Richard Testerson","profile_url":"","verified":true,"currencycode":"USD","fund_id":60746401,"checkout_id":"101412247"},{"donation_id":910853713,"amount":20.0,"is_offline":false,"is_anonymous":false,"created_at":"2022-06-22T12:43:38-05:00","name":"Joshua Ruthtest","profile_url":"","verified":true,"currencycode":"USD","fund_id":60746401,"checkout_id":"98877550"},{"donation_id":910825321,"amount":20.0,"is_offline":false,"is_anonymous":false,"created_at":"2022-06-22T11:15:43-05:00","name":"Barbara MacTester","profile_url":"","verified":true,"currencycode":"USD","fund_id":60746401,"checkout_id":"98868173"},{"donation_id":853711963,"amount":100.0,"is_offline":false,"is_anonymous":false,"created_at":"2022-01-18T20:38:38-06:00","name":"Nicole Testme","profile_url":"","verified":true,"currencycode":"USD","fund_id":60746401,"checkout_id":"79994354"}]},"meta":{"last_updated_at":"2022-08-11T15:29:57.874545-05:00","has_next":false}}'
            names = {
                "1": "Susan McTest",
                "2": "Gabriel Testersmith",
                "3": "Richard Testerson",
                "4": "Joshua Ruthtest",
                "5": "Barbara MacTester",
                "6": "Nicole Testme",
            }
            donations_amounts = {
                "1": 25.0,
                "2": 100.0,
                "3": 15.0,
                "4": 20.0,
                "5": 20.0,
                "6": 100.0,
            }
            api_url = create_api_url(self.test_flags.campaign)
            donations = get_donations(api_url, 5)
            for i in range(len(donations)):
                donations_dict = json.loads(donations[i])
                print(donations_dict["name"])
                self.assertEqual(donations_dict["name"], names[str(i + 1)])
                print(donations_dict["amount"])
                self.assertEqual(
                    donations_dict["amount"], donations_amounts[str(i + 1)]
                )


if __name__ == "__main__":
    unittest.main()
