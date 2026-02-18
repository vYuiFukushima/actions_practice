#課題
from selenium import webdriver  # ブラウザを自動操作するためのライブラリ
from selenium.webdriver.common.by import By  # HTMLの要素をIDやクラス名などで指定するための方法
from selenium.webdriver.support.ui import Select  # プルダウン（<select>タグ）の操作用
from datetime import datetime, timedelta  # 日付や時間の計算、現在日時の取得に使用
from selenium.webdriver.support.ui import WebDriverWait  # 指定条件がTrueになるまで待機するためのクラス
from selenium.webdriver.support import expected_conditions as EC  # WebDriverWaitで使う「条件」をまとめたもの
from selenium.webdriver.common.keys import Keys  # キーボード操作（TABやEnterなど）を送るための定数


class TestHotelPlanisphere(object):
    
    def setup_method(self):
        # ブラウザを開く準備
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()


    # -------------　↓　①当日以前の日付を設定することができないこと　↓　---------------------------------
    def test_before_today(self):
        driver = self.driver
        driver.get("https://hotel-example-site.takeyaqa.dev/ja/reserve.html?plan-id=0")

        # ページ読み込み完了まで待機
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "submit-button"))
        )

        # 昨日 と 今日 を順番にチェックする
        for target_date in [datetime.now() - timedelta(days=1), datetime.now()]:
            target_str = target_date.strftime("%Y/%m/%d")

            # 宿泊日を入力
            textbox_date = driver.find_element(By.ID, "date")
            textbox_date.clear()
            textbox_date.send_keys(target_str)
            textbox_date.send_keys(Keys.TAB)  # フォーカスを外してバリデーションを実行

            # エラーが表示されるまで待つ
            WebDriverWait(driver, 5).until(
                lambda d: d.find_element(By.CSS_SELECTOR, ".invalid-feedback").text != ""
            )

            # エラーメッセージを確認
            error_text = driver.find_element(By.CSS_SELECTOR, ".invalid-feedback").text
            assert error_text == "翌日以降の日付を入力してください。", "日付エラーが出ること"

        # 日付を昨日にした瞬間、ブラウザはすぐにはエラーメッセージを描画できない場合がある
        # →「エラーメッセージが表示されるまで最大2秒待つ」
        # lambdaは長いコードを短縮できる名前のない関数
        
        # WebDriverWait(driver, 2) → 最大2秒間待つ
        # lambda d: ... != "" → 「テキストが空文字じゃなくなる状態」 を条件にしている
        # until(...) → その条件が True になったら先に進む
        # もし2秒たっても条件が True にならなければ タイムアウトエラー（テストが失敗したことのサイン） が出る
        
        # エラーメッセージを確認
        error_text = driver.find_element(By.CSS_SELECTOR, ".invalid-feedback").text
        assert error_text == "翌日以降の日付を入力してください。", "日付エラーが出ること"

    # -------------　↑　①当日以前の日付を設定することができないこと　↑　---------------------------------


    # -------------　↓　②名前が空の状態では予約できないこと　↓　---------------------------------
    def test_username(self):
        driver = self.driver
        driver.get("https://hotel-example-site.takeyaqa.dev/ja/reserve.html?plan-id=0")
        
        # 名前を空にして送信
        textbox = driver.find_element(By.ID,"username")  
        textbox.clear()
        textbox.send_keys("")
        driver.find_element(By.ID,"submit-button").click()

        # 名前のエラーメッセージが表示されるまで待つ
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#username~div"))
        )

        error_text = driver.find_element(By.CSS_SELECTOR,"#username~div").text
        assert error_text == "このフィールドを入力してください。", "エラーメッセージが出ること"
    # -------------　↑　②名前が空の状態では予約できないこと　↑　---------------------------------


    # -------------　↓　③３か月位以上先の日付では予約できないこと　↓　---------------------------------
    def test_reservation(self):
        driver = self.driver
        driver.get("https://hotel-example-site.takeyaqa.dev/ja/reserve.html?plan-id=0")
        # 90日後の日付を計算
        ninety_days_later = datetime.now() + timedelta(days=90)
        ninety_days_later_str = ninety_days_later.strftime("%Y/%m/%d")  

        # 宿泊日を入力
        textbox_date=driver.find_element(By.ID, "date")
        textbox_date.clear()    #入力欄の中を 空にする
        textbox_date.send_keys(ninety_days_later_str)  # 計算した日付を入力
        textbox_date.send_keys(Keys.TAB)  # ← フォーカスを外してバリデーションを実行
        dayerror = "#reserve-form > div > div.col-lg-6.ml-auto > div:nth-child(1) > small"

        # バリデーション(入力のチェック)が出るまで少し待機
        WebDriverWait(driver, 5).until(
            lambda d: d.find_element(By.CSS_SELECTOR, dayerror).text != ""       #!=はイコールじゃないという意味
        )

        # エラーメッセージを確認
        error_text = driver.find_element(By.CSS_SELECTOR, dayerror).text
        assert error_text == "ご予約は3ヶ月以内の日付のみ可能です。", "日付エラーが出ること"
    # -------------　↑　③３か月位以上先の日付では予約できないこと　↑　---------------------------------


    # 後処理メソッド　資料スライド49参照
    def teardown_method(self):              
        self.driver.quit()
