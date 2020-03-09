file_name = "raceid.txt" #レースIDファイル名
write_name = "_url.txt" #出力先のファイル名
base_url = "https://db.netkeiba.com/race/" #結合するURL(共通部分)

with open(write_name, mode="w") as fw:
    with open(file_name, mode="r") as f:
        ids = f.read().split("\n")
        for id in ids:
            fw.write(base_url + id + "\n") #書き込み