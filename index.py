import requests
import json
from flask import Flask, request, jsonify
import vlc
import atexit


@atexit.register
def atexit_fun():
    p.stop()
    p.release()


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
p = vlc.MediaPlayer()
klist = []


@app.route('/')
def index():
    return '<h1>欢迎来到Pi FM 控制台！</h1>'


@app.route('/searchfm')
def searchfm():
    k = requests.get("https://player.fm/zh/podcasts/"+request.args.get("jiemu") +
                     ".json?suggest=true&series_detail=minimal&series_limit=10")
    searchlist = k.json()["series"]
    if searchlist:
        return jsonify({"result": [i["title"]+"/"+str(i["id"]) for i in searchlist], "code": 200})
    else:
        return jsonify({"code": 404})


@app.route('/addfm')
def addfm():
    with open("fmlist.json", 'r') as f:
        datasds = json.load(f)
        datasds.append([request.args.get("name"), str(request.args.get("id"))])
        with open("fmlist.json", 'w') as f:
            json.dump(datasds, f)
    return jsonify({"code": 200})


@app.route('/choosefm')
def choosefm():
    with open("fmlist.json", 'r') as f:
        fmlist = json.load(f)
        fmlist.append(["新增电台"])
    return jsonify({"result": [i[0] for i in fmlist]})


@app.route('/choosejiemu')
def choosejiemu():
    global klist
    with open("fmlist.json", 'r') as f:
        fmlist = json.load(f)
    jiemu = [i for i in fmlist if i[0] == request.args.get("jiemu")][0]
    k = requests.get("https://player.fm/series/"+str(jiemu[1])+".json?detail=minimal&episode_detail=full&episode_offset=" +
                     str(request.args.get("limit"))+"&episode_order=newest&at=1577206316&episode_limit=10")
    klist = k.json()['episodes']
    return jsonify({"result": [n["title"] for n in klist]})


@app.route('/play')
def play():
    if request.args.get("fmname"):
        url = [n["url"]
               for n in klist if n["title"] == request.args.get("fmname")][0]
    elif request.args.get("wyurl"):
        url = request.args.get("wyurl")
    p.set_mrl(url)
    p.play()
    return jsonify({"result": url})


@app.route('/get_state')
def get_state():
    state = p.get_state()
    if state == vlc.State.Playing:
        return "1"
    elif state == vlc.State.Paused:
        return "0"
    else:
        return "-1"


@app.route('/set_volume')
def set_volume():
    p.audio_set_volume(int(request.args.get("volume")))
    return jsonify({"result": "ok"})


@app.route('/set_rate')
def set_rate():
    p.set_rate(float(request.args.get("rate")))
    return jsonify({"result": "ok"})


@app.route('/stop')
def stop():
    p.stop()
    return jsonify({"result": "ok"})


@app.route('/pause')
def pause():
    p.pause()
    return jsonify({"result": "ok"})


@app.route('/resume')
def resume():
    p.set_pause(0)
    return jsonify({"result": "ok"})


@app.route('/set_time')
def set_time():
    timed = p.get_time()
    alltimed = p.get_length()
    updown = int(request.args.get("updown"))
    if updown == 0:
        if timed-15000 >= 0:
            p.set_time(timed+15000)
        else:
            p.set_time(0)
    elif updown == 1:
        if timed+30000 <= alltimed:
            p.set_time(timed+30000)
        else:
            p.stop()
    return jsonify({"result": "ok"})


if '__main__' == __name__:
    app.run(debug=True)
