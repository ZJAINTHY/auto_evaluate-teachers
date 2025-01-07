from flask import Flask, render_template, request
from helium import *
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

max_score = 19	###单项评分最高得分

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    nums = int(request.form['nums'])
    start_background_task(username, password, nums)
    return render_template('progress.html')  # 显示进度页面

def start_background_task(username, password, nums):
    try:
        options = Options()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-gpu') 
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox') 
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537')
        
        driver = start_chrome('http://pj.cmu.edu.cn/static/vue/vue/#/home', options=options)

        log_in(username, password)
        time.sleep(random.uniform(1, 2))
        print(username)
        lesson(nums, driver)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()  # 确保浏览器会被关闭
        print(username, '本次任务已完成')

def log_in(username, password):
    wait_until(Text('帐号为学号或工号').exists)
    write(username, TextField('用户名'))
    write(password, TextField('密码'))
    time.sleep(random.uniform(1, 5))
    click('立即登录')

def lesson(nums, driver):
    completed = 0
    try:
        click('学生评教')
        while nums > 0:
            wait_until(Text('请点击列表中“去填写”按钮完成所有评教任务，评教任务未完成时，可能无法查询成绩。').exists)
            time.sleep(random.uniform(0.5, 0.9))
            click('去填写')
            time1 = time.time()
            implicit_wait_secs = random.uniform(0.5, 0.8)
            write(max_score, S('//html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div/div/input'))
            implicit_wait_secs = random.uniform(0.5, 0.8)
            write(max_score, S('//html/body/div[1]/div/div/div[2]/div[2]/div[3]/div/div/div/input'))
            implicit_wait_secs = random.uniform(0.5, 0.8)
            write(max_score, S('//html/body/div[1]/div/div/div[2]/div[2]/div[4]/div/div/div/input'))
            implicit_wait_secs = random.uniform(0.5, 0.8)
            write(max_score, S('//html/body/div[1]/div/div/div[2]/div[2]/div[5]/div/div/div/input'))
            implicit_wait_secs = random.uniform(0.5, 0.8)
            write(max_score, S('//html/body/div[1]/div/div/div[2]/div[2]/div[6]/div/div/div/input'))
            implicit_wait_secs = random.uniform(0.5, 0.8)
            write(max_score, S('//html/body/div[1]/div/div/div[2]/div[2]/div[7]/div/div/div/input'))
            time.sleep(random.uniform(0.5, 0.9))
            click('提交')
            wait_until(Text('本次评分：98.0，请确认提交？').exists)
            time.sleep(random.uniform(0.6, 0.9))
            click('确定')
            time2 = time.time()
            print(time2 - time1)
            nums -= 1
            completed += 1
    except Exception as e:
        print(f"An error occurred during lesson: {e}")
        # 重新启动浏览器实例
        driver.quit()
        start_background_task(username, password, nums - completed)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=29985)
