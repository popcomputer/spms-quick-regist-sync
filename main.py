import config


def read_csv():
    import pandas as pd
    df = pd.read_csv(config.CSVFILE)
    print(df.to_string())  # print all dataframe
    ids = df.loc[:,"id"].to_numpy()  # convert to numpy array
    emails = df.loc[:, "email"].to_numpy()  # convert to numpy array
    return ids, emails


def spms_request(ids, emails):
    import requests
    from datetime import datetime
    import time
    print("Start sending data to SPMS...\n==============================================\n")
    email_index = 0

    for i in ids:
        now = datetime.now()  # current date and time
        # spmsurl = config.SPMSURL + "/quick_regist.sync?this_page=" + config.PAGEID + "&pass_phrase=" + config.PASSPHRASE + "&id=" + ids  # spms server
        spmsurl = "http://localhost/jacow.php?user_id=" + str(i) + "&page_id=" + config.PAGEID + "&passphrase=" + config.PASSPHRASE + ""  # for localhost testing
        r = requests.get(spmsurl)
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        logdata = "================ spms_id: " + str(i) + ", spms_email: " + emails[email_index] + ", " + date_time + " ================\n"
        logdata += str(r.status_code) + "\n\n" + str(r.headers) + "\n\n" + str(r.content) + "\n\n" + str(r.text) + "\n\n"
        log_file(logdata)
        email_index += 1
        time.sleep(1)
    return email_index  # number of users


def log_file(data):
    print(data)
    lines = [data]
    with open(config.LOGFILE, 'a') as f:
        f.write('\n'.join(lines))
    f.close()


if __name__ == '__main__':
    ids, emails = read_csv()
    allid = spms_request(ids, emails)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n" + str(allid) + " users data has been sent successfully.")