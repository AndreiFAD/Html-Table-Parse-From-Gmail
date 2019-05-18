#!/usr/bin/python
# -*- coding: windows-1250 -*-
__author__ = 'Fekete Andras Demeter'

import imaplib, datetime, base64, email, json, logging, time, socket, os, multiprocessing
import email.header
from html_table_parser import HTMLTableParser


def loadconfig(gmailUSER, gmailPASSWD, gmailFROMlabel, gmailTOlabel):
    with open('config.json', 'r') as f:
        config = json.load(f)
        for compItemJson in config["data"]:
            gmailUSER = compItemJson["gmailUSER"]
            gmailPASSWD = compItemJson["gmailPASSWD"]
            gmailFROMlabel = compItemJson["gmailFROMlabel"]
            gmailTOlabel = compItemJson["gmailTOlabel"]

    return gmailUSER, gmailPASSWD, gmailFROMlabel, gmailTOlabel


def initialization_process(user_name, user_password, folder):
    imap4 = imaplib.IMAP4_SSL('imap.gmail.com')
    imap4.login(user_name, user_password)
    imap4.list()
    imap4.select(folder)
    return imap4


def logout_process(imap4):
    imap4.close()
    imap4.logout()
    return


def htmlString(html):
    result = str(html).replace("\\r", "").replace("\\n", "").strip()
    return result


def prev_month(date=datetime.datetime.today()):
    if date.month == 1:
        return date.replace(month=12, year=date.year - 1)
    else:
        try:
            return date.replace(month=date.month - 2)
        except ValueError:
            return date.replace(month=date.month - 1)


def removeOldLogfile():
    filename = 'gmail_html_table_read_LOG_' + str(prev_month().strftime('%Y-%m')) + '.log'
    if os.path.exists(filename):
        os.remove(filename)
        log = (filename + " -> Old log file delete successful!")
        logging.info(log, extra=attrib)
    else:
        log = (filename + " -> Old log file does not exist")
        logging.info(log, extra=attrib)


def mail(user_email, user_pass, scan_folder, destination_folder):
    imap4 = initialization_process(user_email, user_pass, scan_folder)
    result, items = imap4.uid('search', None, "ALL")
    datas = []
    mail_counter = 0
    mail_counter_error = 0
    if items == ['']:
        pass
    else:
        for uid in items[0].split():
            try:
                subject = ""
                local_date = datetime.datetime.now()
                rv, dataM = imap4.uid('fetch', uid, '(RFC822)')
                if rv == 'OK':
                    message = email.message_from_bytes(dataM[0][1])
                    subject = message['Subject']
                    date_tuple = email.utils.parsedate_tz(message['Date'])
                    if date_tuple:
                        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                rv2, body = imap4.uid('fetch', uid, '(UID BODY[TEXT])')
                if rv2 == 'OK':
                    mail_counter += 1
                    message = email.message_from_bytes(body[0][1])
                    html = base64.urlsafe_b64decode(str(message))
                    p = HTMLTableParser()
                    p.feed(str(message).encode().decode('unicode_escape').encode('latin1').decode('utf-8'))
                    if p.tables == []:
                        p.feed(htmlString(html).encode().decode('unicode_escape').encode('latin1').decode('utf-8'))


                    for table in p.tables:
                        datas.append(table)


                result, copy = imap4.uid('COPY', uid, destination_folder)
                if result == 'OK':
                    log = ('OK: gmail COPIED mail: ' + subject)
                    logging.info(log, extra=attrib)
                    result, delete = imap4.uid('STORE', uid, '+FLAGS', '(\Deleted)')
                    imap4.expunge()
                    if result == 'OK':
                        log = ('OK: gmail COPIED/DELETED mail: ' + subject + ' ' + local_date.strftime("%a, %d %b %Y %H:%M:%S"))
                        logging.info(log, extra=attrib)
                    elif result != 'OK':
                        log = ('ERROR: gmail mail label change: ' + subject + ' ' + local_date.strftime("%a, %d %b %Y %H:%M:%S"))
                        logging.error(log, extra=attrib)
                        continue
                elif result != 'OK':
                    log = ('ERROR: gmail mail copy error: ' + subject + ' ' + local_date.strftime("%a, %d %b %Y %H:%M:%S"))
                    logging.error(log, extra=attrib)
                    continue
            except Exception as e:
                mail_counter_error += 1
                log = ('mail process error ' + str(e))
                logging.error(log, extra=attrib)
    logout_process(imap4)
    return datas, mail_counter, mail_counter_error


if __name__ == "__main__":

    FORMAT = '%(asctime)-15s | %(levelname)s | %(clientip)s | %(user)-8s == %(message)s'
    logging.basicConfig(filename='gmail_html_table_read_LOG_' + str(time.strftime('%Y-%m')) + '.log', format=FORMAT)
    rootLogger = logging.getLogger('')
    rootLogger.setLevel(logging.ERROR)
    rootLogger.setLevel(logging.DEBUG)
    rootLogger.setLevel(logging.WARNING)
    rootLogger.setLevel(logging.INFO)

    ip = socket.gethostbyname(socket.gethostname())
    attrib = {'clientip': ip, 'user': __author__}
    socket.getaddrinfo('localhost', 8080)

    log = (str(datetime.date.today()))
    log += " client start"
    logging.info(log, extra=attrib)

    try:
        removeOldLogfile()

    except Exception as e:
        log = ('Old logfile delete error:  ' + str(e))
        logging.error(log, extra=attrib)

    gmailUSER = ""
    gmailPASSWD = ""
    gmailFROMlabel = ""
    gmailTOlabel = ""

    mail_counter = 0

    log = ('read config start')
    logging.info(log, extra=attrib)

    gmailUSER, gmailPASSWD, gmailFROMlabel, gmailTOlabel = loadconfig(gmailUSER, gmailPASSWD, gmailFROMlabel, gmailTOlabel)

    log = ('read config end')
    logging.info(log, extra=attrib)

    try:
        log = ('gmail connect')
        logging.info(log, extra=attrib)
        main_dictionary, mail_counter, mail_counter_error = mail(gmailUSER, gmailPASSWD, gmailFROMlabel, gmailTOlabel)
        log = ('gmail connect successful')
        logging.info(log, extra=attrib)

        log = (str(mail_counter) + ' e-mail has read with ' + str(mail_counter_error) + ' error')
        for table in main_dictionary:
            print(table)

        if mail_counter_error != 0:
            logging.error(log, extra=attrib)
        else:
            logging.info(log, extra=attrib)

    except Exception as e:
        log = ('gmail connect error ' + str(e))
        logging.error(log, extra=attrib)

    log = "client shutdown"
    logging.info(log, extra=attrib)
