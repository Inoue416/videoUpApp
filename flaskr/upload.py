from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, make_response, jsonify,
)
import werkzeug

from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db, close_db
import os
import re
from datetime import datetime
from flaskr.googleAPI.upload_googledrive import upload_drive

from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter

import time

bp = Blueprint('upload', __name__)
danger = "alert alert-danger"
success = "alert alert-success"

# バリデーションのための関数(ブラウザバックの対策)
def dataChecker(file_id):
    result = False
    db = get_db()
    data = db.execute('SELECT * FROM posts WHERE author_id = %s AND file_id = %s', (session.get('user_id'),file_id,))
    data = db.fetchall()
    print("data: ")
    print(data)
    if data:
        result = True
    close_db()
    return result


@bp.route('/')
def index():
    return render_template('upload/index.html')

@bp.route('/introduction')
def introduction():
    return render_template('upload/introduction.html')

@bp.route('/tweet_list')
@login_required
def tweet_list():
    data = None
    db = None
    filter = False
    if session.get("user_id") == 0:
        db = get_db()
        db.execute("SELECT * FROM tweets ORDER BY random()")
        data = db.fetchall()
    else:
        db = get_db()
        #アップロード状況を取得
        db.execute('SELECT file_id FROM posts WHERE author_id = %s', (session.get('user_id'),))
        uploaded = db.fetchall()
        # ビデオデータベース情報を取得
        data = db.execute('SELECT * FROM tweets ORDER BY id')
        data = db.fetchall()
        # フィルタ処理
        for u in uploaded:
            for d in data:
                if u[0] == d[1]:
                    data.remove(d)
        print("data: {}".format(len(data)))
        if len(data) == 0:
            filter = True

    # ページネーション
    max_age = 60 * 60 * 24
    expires = int(datetime.now().timestamp()) + max_age
    page_disp_msg = '表示範囲 <b>{start}件 - {end}件 </b> 合計：<b>{total}</b>件'
    page = request.args.get(get_page_parameter(), type=int, default=1)
    da = data[(page - 1)*10: page*10]
    pagination = Pagination(page=page, total=len(data), search=False, per_page=10, css_framework='bootstrap4',display_msg=page_disp_msg)
    resp = make_response(render_template('upload/tweet_list.html', data=da, filter=filter, pagination=pagination))
    resp.set_cookie(key='user_id', value=str(session.get('user_id')), max_age=max_age, path=request.path,
    expires=expires, httponly=True, secure=False)
    close_db()
    """else:
        resp = make_response(redirect(url_for('upload.index')))"""
    return resp

@bp.route('/ita_list')
@login_required
def ita_list():
    data = None
    db = None
    filter = False
    if session.get("user_id") == 0:
        db = get_db()
        db.execute("SELECT * FROM itas ORDER BY random()")
        data = db.fetchall()
    else:
        filter = False
        db = get_db()
        #アップロード状況を取得
        db.execute('SELECT file_id FROM posts WHERE author_id = %s', (session.get('user_id'),))
        uploaded = db.fetchall()
        # ビデオデータベース情報を取得
        data = db.execute('SELECT * FROM itas ORDER BY id')
        data = db.fetchall()
        # フィルタ処理
        for u in uploaded:
            for d in data:
                if u[0] == d[1]:
                    data.remove(d)
        print("data: {}".format(len(data)))
        if len(data) == 0:
            filter = True


    # ページネーション
    max_age = 60 * 60 * 24
    expires = int(datetime.now().timestamp()) + max_age
    page_disp_msg = '表示範囲 <b>{start}件 - {end}件 </b> 合計：<b>{total}</b>件'
    page = request.args.get(get_page_parameter(), type=int, default=1)
    da = data[(page - 1)*10: page*10]
    pagination = Pagination(page=page, total=len(data), search=False, per_page=10, css_framework='bootstrap4',display_msg=page_disp_msg)
    resp = make_response(render_template('upload/ita_list.html', data=da, filter=filter, pagination=pagination))
    resp.set_cookie(key='user_id', value=str(session.get('user_id')), max_age=max_age, path=request.path,
    expires=expires, httponly=True, secure=False)
    close_db()
    """else:
        resp = make_response(redirect(url_for('upload.index')))"""
    return resp

@bp.route('/upload_tweet/<file_id>')
@login_required
def upload_tweet(file_id):
    #if g.user:
    if file_id == None:
        flash('選択されたファイルが存在しません。', danger)
        return redirect(url_for('upload.index'))
    if dataChecker(file_id) and session.get("user_id") != 0:
        print('checker: True')
        flash('すでにこの項目はアップロードされています。', danger)
        return redirect(url_for("upload.index"))
    cur = get_db()
    cur.execute('SELECT * FROM tweets WHERE file_id = %s', (file_id,))
    data = cur.fetchone()
    close_db()
    resp = make_response(render_template('upload/upload_tweet.html', file_id=file_id, data=data))
    """else:
        resp = make_response(redirect(url_for('upload.index')))"""
    return resp

@bp.route('/upload_ita/<file_id>')
@login_required
def upload_ita(file_id):
    #if g.user:
    if file_id == None:
        flash('選択されたファイルが存在しません。', danger)
        return redirect(url_for('upload.index'))
    if dataChecker(file_id) and session.get("user_id") != 0:
        flash('すでにこの項目はアップロードされています。', danger)
        return redirect(url_for("upload.index"))
    cur = get_db()
    cur.execute('SELECT * FROM itas WHERE file_id = %s', (file_id,))
    data = cur.fetchone()
    close_db()
    resp = make_response(render_template('upload/upload_ita.html', file_id=file_id, data=data))
    """else:
        resp = make_response(redirect(url_for('upload.index')))"""
    return resp


@bp.route('/save_tweet/<file_id>', methods=['POST'])
def save_tweet(file_id):
    if 'video' not in request.files:
        flash('ファイルが選択されていません。', danger)
        resp = make_response(redirect(url_for('upload.upload_tweet', file_id=file_id)))
    elif dataChecker(file_id) and session.get("user_id") != 0:
        flash('すでにこの項目はアップロードされています。', danger)
        return redirect(url_for("upload.index"))
    else:
        UPLOAD_PATH = 'flaskr/video'
        db = get_db()
        db.execute('SELECT * FROM tweets WHERE file_id = %s', (file_id,))
        # 動画のデータベース情報を獲得
        data = db.fetchone()
        v_num = data['num']
        video = request.files['video']
        age = request.form['ageSelect']
        """db.execute('SELECT gender, age FROM users WHERE id = %s', (session.get('user_id'),))
        u_data = db.fetchone()
        gender = u_data['gender']
        age = u_data['age']"""
        stream = None
        exd = re.findall(r'\.\w*', video.filename)
        filename = UPLOAD_PATH + (('/{}_{}{}').format(file_id, v_num, exd[0]))
        videoname = (('{}_{}{}').format(file_id, v_num, exd[0]))
        video.save(os.path.join(UPLOAD_PATH, videoname))
        # .webm to .mp4
        """if '.webm' in exd:
            exd = ['.mp4']
            os.system("ffmpeg -i {} {}".format(filename, (os.path.join(UPLOAD_PATH, videoname.replace('.webm', '.mp4')))))
            filename = filename.replace('.webm', '.mp4')
            videoname = videoname.replace('.webm', '.mp4')"""
        upload_drive(foldername=file_id, videopath=filename, videoname=videoname)
        db.execute('INSERT INTO posts (author_id, file_id, age, created) VALUES(%s,%s,%s,CURRENT_TIMESTAMP)', (session.get('user_id'), file_id, age))
        g.conn.commit()
        v_num += 1
        db.execute('UPDATE tweets SET num = %s, created = CURRENT_TIMESTAMP WHERE file_id = %s', (v_num, file_id))
        g.conn.commit()
        close_db()
        flash('アップロードしました。ありがとうございます。', success)
        #time.sleep(5)
        # TODO: saveしたファイルと変換ファイルがあればそれも消す
        os.remove(filename)
        resp = make_response(redirect(url_for('upload.index')))
    return resp

@bp.route('/save_ita/<file_id>', methods=['POST'])
def save_ita(file_id):
    if 'video' not in request.files:
        flash('ファイルが選択されていません。', danger)
        resp = make_response(redirect(url_for('upload.upload_ita', file_id=file_id)))
    elif dataChecker(file_id) and session.get("user_id") != 0:
        flash('すでにこの項目はアップロードされています。', danger)
        return redirect(url_for("upload.index"))
    else:
        UPLOAD_PATH = 'flaskr/video'
        db = get_db()
        db.execute('SELECT * FROM itas WHERE file_id = %s', (file_id,))
        # 動画のデータベース情報を獲得
        data = db.fetchone()
        v_num = data['num']
        video = request.files['video']
        age = request.form['ageSelect']

        """db.execute('SELECT gender, age FROM users WHERE id = %s', (session.get('user_id'),))
        u_data = db.fetchone()
        gender = u_data['gender']
        age = u_data['age']"""

        exd = re.findall(r'\.\w*', video.filename)
        filename = UPLOAD_PATH + (('/{}_{}{}').format(file_id, v_num, exd[0]))
        videoname = (('{}_{}{}').format(file_id, v_num, exd[0]))
        video.save(os.path.join(UPLOAD_PATH, videoname))
        # .webm to .mp4
        """if '.webm' in exd:
            exd = ['.mp4']
            os.system("ffmpeg -i {} {}".format(filename, (os.path.join(UPLOAD_PATH, videoname.replace('.webm', '.mp4')))))
            filename = filename.replace('.webm', '.mp4')
            videoname = videoname.replace('.webm', '.mp4')"""
        upload_drive(foldername=file_id, videopath=filename, videoname=videoname)
        db.execute('INSERT INTO posts (author_id, file_id, age, created) VALUES(%s,%s,%s,CURRENT_TIMESTAMP)', (session.get('user_id'), file_id, age))
        g.conn.commit()
        v_num += 1
        db.execute('UPDATE itas SET num = %s, created = CURRENT_TIMESTAMP WHERE file_id = %s', (v_num, file_id))
        g.conn.commit()
        flash('アップロードしました。ありがとうございます。', success)
        close_db()
        # TODO: saveしたファイルと変換ファイルがあればそれも消す
        os.remove(filename)
        resp = make_response(redirect(url_for('upload.index')))
    return resp

@bp.route('/record/<file_id>')
@login_required
def record(file_id):
    if file_id == None:
        flash('選択されたファイルが存在しません。', danger)
        return redirect(url_for('upload.index'))
    if dataChecker(file_id):
        flash('すでにこの項目はアップロードされています。', danger)
        return redirect(url_for("upload.index"))
    j=None
    cur = get_db()
    if file_id[0] == 't':
        cur.execute('SELECT * FROM tweets WHERE file_id = %s', (file_id,))
    else:
        cur.execute('SELECT * FROM itas WHERE file_id = %s', (file_id,))
    data = cur.fetchone()
    close_db()
    resp = make_response(render_template('upload/record.html', file_id=file_id, data=data[3]))
    """else:
        resp = make_response(redirect(url_for('upload.index')))"""
    return resp
