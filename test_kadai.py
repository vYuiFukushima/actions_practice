import os
from playwright.sync_api import Page
import pytest
import datetime

class TestHotelPlanisphere(object):

    # 前後の処理
    @pytest.fixture(scope="function", autouse=True)
    def page_fixture(self, page: Page):
        os.makedirs("test-results", exist_ok=True) # ← テスト前に作る
        self.page = page
        self.page.goto(
            "https://hotel-example-site.takeyaqa.dev/ja/reserve.html?plan-id=0",
            wait_until="networkidle"
        )
        yield
        self.page.close()

    # 当日日付以前を設定すると予約できないこと
    def test_before_today(self):
        page = self.page

        # 宿泊日を入力
        textbox_date = page.locator("#date")
        date_list = textbox_date.input_value().split("/")
        year = date_list[0]
        month = date_list[1]
        day = date_list[2]
        t_year = str(datetime.date.today().year)
        t_month = str(datetime.date.today().month)
        t_day = str(datetime.date.today().day)

        if year == t_year and month == t_month and day == t_day:
            # 当日日付が入力済のため、何もしない
            print("宿泊日:" + year + "/" + month + "/" + day)
        else:
            textbox_date.fill(t_year + "/" + t_month + "/" + t_day)
            textbox_date.press("Tab")

        # 宿泊日数を入力
        page.fill("#term", "1")

        # 人数を入力
        page.fill("#head-count", "1")

        # お得なプランを選択
        page.check("#sightseeing")

        # お名前を入力
        page.fill("#username", "テスト太郎")

        # 確認のご連絡を選択
        page.select_option("#contact", "no")

        # 予約内容を確認するボタンをクリック
        page.click("#submit-button")
        # 待機処理
        page.wait_for_load_state()

        # スクリーンショットの保存
        page.screenshot(path="test-results/before_today.png")

        # 確認
        assert page.text_content("#date ~ div") == "翌日以降の日付を入力してください。", "当日以前の日付では予約ができないこと"

    # 名前が空の状態では予約できないこと
    def test_noname(self):
        page = self.page

        # 宿泊日を入力
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        t_year = str(tomorrow.year)
        t_month = str(tomorrow.month)
        t_day = str(tomorrow.day)

        textbox_date = page.locator("#date")
        textbox_date.fill(t_year + "/" + t_month + "/" + t_day)
        textbox_date.press("Tab")

        # 宿泊日数を入力
        page.fill("#term", "1")

        # 人数を入力
        page.fill("#head-count", "1")

        # お得なプランを選択
        page.check("#sightseeing")

        # 確認のご連絡を選択
        page.select_option("#contact", "no")

        # 予約内容を確認するボタンをクリック
        page.click("#submit-button")
        # 待機処理
        page.wait_for_load_state()

        # スクリーンショットの保存
        page.screenshot(path="test-results/noname.png")


        # 確認
        assert page.text_content("#username ~ div") == "このフィールドを入力してください。", "名前が空欄では予約ができないこと"

    # 3か月以上先の日付では予約できないこと
    def test_three_month_later(self):
        page = self.page

        # 宿泊日を入力
        reserve_date = datetime.date.today() + datetime.timedelta(days=91)
        r_year = str(reserve_date.year)
        r_month = str(reserve_date.month)
        r_day = str(reserve_date.day)

        textbox_date = page.locator("#date")
        textbox_date.fill(r_year + "/" + r_month + "/" + r_day)
        textbox_date.press("Tab")

        # 宿泊日数を入力
        page.fill("#term", "1")

        # 人数を入力
        page.fill("#head-count", "1")

        # お得なプランを選択
        page.check("#sightseeing")

        # お名前を入力
        page.fill("#username", "テスト太郎")

        # 確認のご連絡を選択
        page.select_option("#contact", "no")

        # 予約内容を確認するボタンをクリック
        page.click("#submit-button")
        # 待機処理
        page.wait_for_load_state()

        # スクリーンショットの保存
        page.screenshot(path="test-results/three_month_later.png")


        # 確認
        assert False