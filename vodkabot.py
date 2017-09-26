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

wait2 = {
	'autoJoin':True,
	'autoCancel':{"on":True,"members":1},
	'autoAdd':True,
	'message':"Thanks for add me",
	"clock":True,
	"cName":"Safiqq ",
	"blacklist":{}
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

def NOTIFIED_ADD_CONTACT(op):
    try:
        sendMessage(op.param1, "Terima kasih " + client.getContact(op.param1).displayName + " telah menambahkan saya sebagai teman :]")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

def NOTIFIED_LEAVE_GROUP(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + " meninggalkan grup.")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_LEAVE_GROUP\n\n")
        return

tracer.addOpInterrupt(15,NOTIFIED_LEAVE_GROUP)

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayname + " menghapus " + client.getContact(op.param3).displayname + " dari grup.")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_LEAVE_GROUP\n\n")
        return

tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def NOTIFIED_INVITE_INTO_ROOM(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayname + " menginvite " + client.getContact(op.param3).displayname + " ke grup.")
    except Exception as e:
        print e
	print ("\n\nNOTIFIED_INVITE_INTO_ROOM\n\n")
	return

tracer.addOpInterrupt(22,NOTIFIED_INVITE_INTO_ROOM)

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

def nameUpdate():
    while True:
        try:
        #while a2():
            #pass
            if wait2["clock"] == True:
                now2 = datetime.now()
                nowT = datetime.strftime(now2,"(%H:%M)")
                profile = client.getProfile()
                profile.displayName = wait2["cName"] + nowT
                client.updateProfile(profile)
            time.sleep(60)
        except:
            pass

def bot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            if wait2 ["autoAdd"] == True:
                client.findAndAddContactsByMid(op.param1)
                if (wait2["message"] in [""," ","\n",None]):
                    pass
                else:
                    cl.sendText(op.param1,str(wait2["message"]))
        if op.type == 13:
            print op.param1
            print op.param2
            print op.param3
            if mid in op.param3:
                G = client.getGroup(op.param1)
                if wait2["autoJoin"] == True:
                    if wait2["autoCancel"]["on"] == True:
                        if len(G.members) <= wait2["autoCancel"]["members"]:
                            client.rejectGroupInvitation(op.param1)
                        else:
                            client.acceptGroupInvitation(op.param1)
                    else:
                        client.acceptGroupInvitation(op.param1)
                elif wait2["autoCancel"]["on"] == True:
                    if len(G.members) <= wait2["autoCancel"]["members"]:
                            client.rejectGroupInvitation(op.param1)
            else:
                Inviter = op.param3.replace("",',')
                InviterX = Inviter.split(",")
                matched_list = []
                for tag in wait2["blacklist"]:
                    matched_list+=filter(lambda str: str == tag, InviterX)
                if matched_list == []:
                    pass
                else:
                    client.cancelGroupInvitation(op.param1, matched_list)
        if op.type == 19:
                if mid in op.param3:
                    if op.param2 in Bots:
                        pass
                    try:
                        client.kickoutFromGroup(op.param1,[op.param2])
                    except:
                        try:
                            random.choice(KAC).kickoutFromGroup(op.param1,[op.param2])
                        except:
                            print ("Kicked ["+op.param1+"] by ["+op.param2+"[")
                        if op.param2 in wait2["blacklist"]:
                            pass
                        if op.param2 in wait2["whitelist"]:
                            pass
                        else:
                            wait2["blacklist"][op.param2] = True
                    G = client.getGroup(op.param1)
                    G.preventJoinByTicket = False
                    client.updateGroup(G)
                    Ti = client.reissueGroupTicket(op.param1)
                    client.acceptGroupInvitationByTicket(op.param1,Ti)
                    X = client.getGroup(op.param1)
                    X.preventJoinByTicket = True
                    client.updateGroup(X)
                    Ti = client.reissueGroupTicket(op.param1)
                    if op.param2 in wait2["blacklist"]:
                        pass
                    if op.param2 in wait2["whitelist"]:
                        pass
                    else:
                        wait2["blacklist"][op.param2] = True
        if op.type == 59:
            print op


    except Exception as error:
        print error

		
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
                if msg.text == "jam":
                    if wait2["clock"] == True:
                        client.sendText(msg.to,"Jam diperbarui!")
                    else:
			wait2["clock"] = True
                        now2 = datetime.now()
                        nowT = datetime.strftime(now2,"(%H:%M)")
                        profile = client.getProfile()
                        profile.displayName = wait2["cName"] + nowT
                        client.updateProfile(profile)
                        client.sendText(msg.to,"Jam diperbarui!")
                if "kick @" in msg.text:
                    nk0 = msg.text.replace("kick @ ","")
                    nk1 = nk0.lstrip()
                    nk2 = nk1.replace("@","")
                    nk3 = nk2.rstrip()
                    Names = nk3
                    gs = cl.getGroup(msg.to)
                    targets = []
                    for s in gs.members:
                        if Names in s.displayName:
                           targets.append(s.mid)
                    if targets == []:
                        sendMessage(msg.to,"Nama tidak ditemukan.")
                        pass
                    else:
                        for target in targets:
                             try:
                                 klist=[client]
                                 kicker=random.choice(klist)
                                 kicker.kickoutFromGroup(msg.to,[target])
                                 print (msg.to,[g.mid])
                             except:
                                 ki.sendText(msg.to, Names + " telah dihapus dari grup.")
                if "ban @" in msg.text:
		    ban0 = msg.text.replace("ban @ ","")
		    ban1 = ban0.lstrip()
		    ban2 = ban1.replace("@","")
		    ban3 = ban2.rstrip()
                    msg.toType == 2
                    print "[Ban]ok"
                    Names = [contact.displayName for contact in group.members]("unban @","")
                    nameTarget = Names.rstrip('  ')
                    group = client.getGroup(msg.to)
                    targets = []
                    for group in group.members:
                        if nameTarget == group.displayName:
                            targets.append(group.mid)
                    if targets == []:
                        client.sendText(msg.to,"Nama tidak ditemukan.")
                    else:
                        for target in targets:
                            try:
                                wait2["blacklist"][target] = True
                                f=codecs.open('st2__b.json','w','utf-8')
                                json.dump(wait2["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                                client.sendText(msg.to, Names + " telah ditambahkan ke daftar bl.")
                            except:
                                client.sendText(msg.to, "Nama tidak ditemukan.")
                if "unban @" in msg.text:
		    unban0 = msg.text.replace("unban @ ","")
		    unban1 = unban0.lstrip()
		    unban2 = unban1.replace("@","")
		    unban3 = unban2.rstrip()
                    msg.toType == 2
                    print "[Unban]ok"
                    Names = [contact.displayName for contact in group.members]("unban @","")
                    nameTarget = Names.rstrip('  ')
                    group = client.getGroup(msg.to)
                    targets = []
                    for group in group.members:
                        if nameTarget == group.displayName:
                                targets.append(group.mid)
                        if targets == []:
                            client.sendText(msg.to,"Nama tidak ditemukan.")
                        else:
                            for target in targets:
                                try:
                                    del wait2["blacklist"][target]
                                    f=codecs.open('st2__b.json','w','utf-8')
                                    json.dump(wait2["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                                    client.sendText(msg.to, Names + " berhasil di unban.")
                                except:
                                    client.sendText(msg.to, Names + " berhasil di unban.")
                if "kickall" in msg.text:
                    if msg.toType == 2:
                        print "ok"
                        Names = msg.text.replace("kickall","")
                        groups = client.getGroup(msg.to)
			client.sendText(msg.to,"Tangkis om")
			targets = []
			for g in groups.members:
			    if Names in g.displayName:
				targets.append(group.mid)
			if targets == []:
			    client.sendText(msg.to,"Tidak ada anggota.")
			else:
			    for target in targets:
				try:
				    klist=[client]
				    kicker=random.choice(klist)
				    kicker.kickoutFromGroup(msg.to,[target])
				    print (msg.to,[group.mid])
				except:
				    client.sendText(msg.to,"Tangkis om")
                if msg.text == "cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "Tidak ada orang yang diundang.")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " undangan dibatalkan.")
		if msg.text == "keyword":
		    sendMessage(msg.to, "-mid\n-gid\n-ginfo\n-url\n-open\n-close\n-nk\n-cancel\n-me\n-time\n-point\n-check")
                if msg.text == "me":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if msg.text == "time":
                    sendMessage(msg.to, "Sekarang jam " + datetime.datetime.today().strftime('%H:%M:%S'))
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

                        sendMessage(msg.to, "Dibaca oleh:\n%s\n\nSider:\n%s\n\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "Dibaca oleh:\n%s\n\nSider:\n%s\n\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
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
