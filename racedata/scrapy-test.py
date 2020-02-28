import sys
import requests
import lxml.html
import re
import csv

def main():
    url =  'https://nar.netkeiba.com/?pid=race&id=p202047020701&mode=top'#コマンドライン引数からURLを取得
    html = fetch(url) #URLのWebページを取得
    result = scrape(html) #取得したWebページから欲しい部分のみを切り出す
    save('result.csv',result) #切り出した結果をCSVに保存する

def fetch(url :str): 
    r = requests.get(url) #urlのWebページを保存する
    r.encoding = r.apparent_encoding #文字化けを防ぐためにencodingの値をappearent_encodingで判定した値に変更する
    return r.text #取得データを文字列で返す

def scrape(html: str):
    html = lxml.html.fromstring(html) #fetch()での取得結果をパース
    result = [] #スクレイピング結果を格納
    for h in html.cssselect('#race_main > div > table > tr'):#スクレイピング箇所をCSSセレクタで指定
        column = ((",".join(h.text_content().split("\n"))).lstrip(",").rstrip(",")).split(",")
        #text_content()はcssselectでマッチした部分のテキストを改行文字で連結して返すので、
        #splitを使って改行文字で分割して、その結果をカンマ区切りでjoinする。
        #前と後ろに余計な空白とカンマが入っている(tdじゃなくてtrまでのセレクタをしていした分の空文字が入っちゃってる?ようわからん)ので、
        #splitで空白を、lstrip,rstripでカンマを削除してさらにそれをカンマで区切ってリストにしている
        column.pop(4) if column[4] == "" else None  #1行目以外、馬名と性齢の間に空文字が入っちゃってるので取り出す
        result.append(column) #リストに行のデータ(リストを追加)

    return result #結果を返す

def save(file_path, result):
     with open(file_path, 'w', newline='') as f: #ファイルに書き込む
         writer = csv.writer(f) #ファイルオブジェクトを引数に指定する
         writer.writerow(result.pop(0)) #一行目のフィールド名を書き込む
         writer.writerows(result) #残りの行を書き込む

if __name__ == '__main__':
    main() 