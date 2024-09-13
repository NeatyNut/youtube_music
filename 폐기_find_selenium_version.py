## selenium 버전 찾아주기
import requests
import json

myversion = "128.0.6613.120"
myos = "win64" # linux64, mac-arm64, mac-x64, win32, win64

url = 'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    all_json = json.loads(html)
    selenium_version = all_json['versions']
    for i in selenium_version:
        ## 버전이 같거나 더 높을 때
        if i['version'] == myversion or int(i['version'].split(".")[0]) < int(myversion.split(".")[0]):
            for j in i['downloads']['chrome']:
                ## 운영체제 맞는 것
                if j['platform'] == myos:
                    print(j['url'])
                    break
            break

else:
    print(f"웹페이지를 가져오는 데 실패했습니다. 상태 코드: {response.status_code}")