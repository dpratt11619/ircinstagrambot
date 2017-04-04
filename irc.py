import socket
import urllib.request
import re

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net"
channel = "##bottesting"
botnick = "NotAPyBot"
adminname = "randomnick"
exitcode = "bye " + botnick

ircsock.connect((server,6667))
ircsock.send(bytes("USER " + botnick +" "+ botnick +" "+ botnick+" "+ botnick + "\n", "UTF-8"))
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8"))

def joinchan(chan):
    ircsock.send(bytes("JOIN "+ chan + "\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

def ping():
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

def sendmsg(msg, target=channel):
    #remove me
    target = "mosasaur"
    ircsock.send(bytes("PRIVMSG " + target + " :"+ msg + "\n", "UTF-8"))

def main():
    joinchan(channel)
    while 1:   
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)
        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
            if len(name) < 17:
                if message.find('https://www.instagram.com/p/') != -1:
                    url = message.split('https://www.instagram.com/p/',1)[1]
                    fp = urllib.request.urlopen("https://www.instagram.com/p/" + url)
                    mybytes = fp.read()

                    mystr = mybytes.decode("utf8")
                    fp.close
                    matches = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mystr)
                    mp4match = "false"
                    for match in matches:
                        if match.find("mp4") != -1:
                            if mp4match == "false":
                                sendmsg(match)
                                mp4match = "true"
                    if mp4match == "false":
                        match = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+.jpg', mystr)
                        if match:
                            sendmsg(match[0])
                if message[:5].find('.tell') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                    else:
                        target = name
                        message = "Could not parse. The message should be in the format of '.tell [target] [message]' to work properly."
                    sendmsg(message,target)
                if name.lower() == adminname.lower() and message.rstrip() == exitcode:
                    sendmsg("oh...okay. :'(")
                    ircsock.send(bytes("QUIT \n", "UTF-8"))
                    return
                if name.lower() == adminname.lower() and message.find("JOIN") != -1:
                    joinchan((message.split('JOIN')[1]).strip())
        else:
            if ircmsg.find("PING :") != -1:
                print("PINGED")
                ping()

main()
