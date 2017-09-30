# -*- coding: utf-8 -*-
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin("line://au/q/")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
   }

setTime = {}
setTime = wait["setTime"]

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)

def NOTIFIED_ADD_CONTACT(op):
    try:
        sendMessage(op.param1, "Hi " + client.getContact(op.param1).displayName + ", thanks for add.")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\n・" + Name
                wait['ROM'][op.param1][op.param2] = "・" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        else:
            pass
    except KeyboardInterrupt:
	       sys.exit(0)
    except Exception as error:
        print error
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)
		
def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            msg.to = msg.from_
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "me":
                    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "gid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "ginfo":
                    group = client.getGroup(msg.to)
                    md = "[Nama grup]:\n-" + group.name + "\n\n[ID grup]:\n-" + group.id
                    if group.preventJoinByTicket is False: md += "\n\nURL: Terbuka.\n"
                    else: md += "\n\nURL: Tertutup.\n"
                    if group.invitee is None: md += "\nAnggota: " + str(len(group.members)) + " orang.\n\nUndangan: Tidak ada."
                    else: md += "\nAnggota: " + str(len(group.members)) + " orang.\n\nUndangan: " + str(len(group.invitee)) + "orang."
                    sendMessage(msg.to,md)
                if msg.text == "url":
                    sendMessage(msg.to,"http://line.me/R/ti/g/" + client._client.reissueGroupTicket(msg.to))
                if msg.text == "open":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "URL sudah terbuka.")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL dibuka.")
                if msg.text == "close":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "URL sudah tertutup.")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL ditutup.")
                if msg.text == "speed":
                    start = time.time()
                    sendMessage(msg.to, "Progress...")
                    elapsed_time = time.time() - start
                    sendMessage(msg.to, "%sseconds" % (elapsed_time))
		if msg.text == "rec":
		    elapsed_time = time.time() - start
		    sendMessage(msg.to, "Menghitung waktu..")
			if msg.text == "recc"
			    sendMessage(msg.to, "%sseconds" % (elapsed_time))
                if msg.text == "kickall":
                    print "ok"
                    _name = msg.text.replace("kickall","")
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        sendMessage(msg.to,"error")
                    else:
                        for target in targets:
                            try:
                                client.kickoutFromGroup(msg.to,[target])
                                print (msg.to,[g.mid])
                            except:
                                sendText(msg.to," _Error69")
                if msg.text == "cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "Tidak ada orang yang diundang.")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " undangan dibatalkan.")
		if msg.text == "keyword":
		    sendMessage(msg.to, "-mid\n-gid\n-ginfo\n-url\n-open\n-close\n-speed\n-cancel\n-me\n-time\n-point\n-check\n-sider")
                if msg.text == "me":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if msg.text == "time":
                    sendMessage(msg.to, "Sekarang jam " + datetime.datetime.today().strftime('%H:%M:%S') + " WIB.")
                if msg.text == "point":
                    sendMessage(msg.to, "Read point telah di set!")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%H:%M:%S, %d %m %Y')
                    wait['ROM'][msg.to] = {}
                    print wait
                if msg.text == "check":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"
                        sendMessage(msg.to, "[Dibaca oleh]:\n%s\n\n[Sider]:\n%s\n\n[%s]\n\n\n"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "[Dibaca oleh]:\n%s\n\n[Sider]:\n%s\n\n[%s]\n\n\n"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                else:
                    pass
        else:
            pass

    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
