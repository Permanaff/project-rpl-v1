from flask import Flask, render_template, session, request , redirect, url_for, flash, jsonify, send_file 
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_bcrypt import Bcrypt 
from midtransclient import Snap, CoreApi
from midtrans.paymentProcess import *
import requests
import os
import json
import random
import string
import qrcode

app = Flask(__name__)
CORS(app, origins=['http://127.0.0.1:5000'])

app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"]= ''
app.config["MYSQL_DB"] = 'cinema'
app.config["UPLOAD_FOLDER"] = 'static/images/'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

core = CoreApi(
    is_production=False,
    server_key= '< Your Server Key >',
    client_key='< Your Client Key >'
)


# -----------------------------------------------------------------
# ---------------------------- U S E R ---------------------------- 
# -----------------------------------------------------------------


@app.route('/login', methods=['POST'])
def login() : 
    try :
        email = request.json['email']
        password = request.json['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        result = cur.fetchone()

        if result:
            if not checkPassword(result[8], password) :
                return jsonify({'status': 'Error' , 'Massage' : 'Your credentials is invalid!' }),500
            user = [{"user_id" : result[0], 'username' : result[2], 'nama' : result[1], 'level_user' : result[11]}]
            return jsonify(user),200
        else : 
            return jsonify({"stauts" : 'Error', "message" : "Login Gagal!"}),500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500 



@app.route("/register", methods=["POST"])
def register():
    regis_data = request.json

    nama = regis_data["nama"]
    username = regis_data["username"]
    no_telp = regis_data["no_telp"]
    alamat = regis_data["alamat"]
    email = regis_data["email"]
    passwd = setPassword(regis_data["password"])
    gender = regis_data['gender']
    tanggal_lahir = regis_data['tanggal_lahir']
    level_user = '3'
    # image = 'default-profile.png'
    user_id = generate_user_id(tanggal_lahir)

    try : 
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (id_user, nama, username, email, tanggal_lahir, no_telp, gender, password, alamat, level_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(user_id, nama, username, email, tanggal_lahir, no_telp, gender, passwd, alamat, level_user))
        mysql.connection.commit()
        return jsonify({'massage' : 'Register Success'}),200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500 



@app.route('/get-administrator', methods=['POST'])
def get_administrator() : 
    cur = mysql.connection.cursor() 
    cur.execute('SELECT * FROM users WHERE level_user="1" OR level_user="2"')
    result = cur.fetchall() 
    cur.close() 

    users = [{'id_user' : row[0], 'nama' : row[1], 'username' : row[2], 'email' : row[3], 'tanggal_lahir' : row[4], 'no_telp': row[5], 'alamat' : row[10], 'level_user' : row[11]}   for row in result]

    return jsonify({'users' : users})


@app.route('/register-admin', methods=['POST'])
def register_admin() : 
    try : 
        data = request.json
        nama = data['nama']
        username = data['username']
        email = data['email']
        tanggal_lahir = data['tanggal_lahir']
        no_telp = data['no_telp']
        gender = data['gender']
        password = setPassword(data['password'])
        alamat = data['alamat']
        level_user = data['level_user']
        id_user = generate_user_id(tanggal_lahir)


        cur = mysql.connection.cursor() 
        cur.execute("INSERT INTO users (id_user, nama, username, email, tanggal_lahir, no_telp, gender, password, alamat, level_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id_user, nama, username, email, tanggal_lahir, no_telp, gender, password, alamat, level_user))
        mysql.connection.commit() 
        cur.close() 

        return jsonify({"Err" : False, 'message' : 'Berhasil Membuat Akun Admin!'}), 200
    except Exception as e : 
        error_message = str(e)
        print(error_message)
        return jsonify({'Err' : True, 'message' : error_message}), 500

# -----------------------------------------------------------------
# ------------------------- B O O K I N G -------------------------
# -----------------------------------------------------------------

@app.route('/save-booking', methods=['POST'])
def save_booking():
    booking_data = request.json
    date = datetime.now().strftime('%Y-%m-%d')
    user_id = booking_data['user_id']
    booking_id = generate_bookingId()
    id_schedule = booking_data['id_schedule']
    id_drink = booking_data['id_drink']
    id_seat = booking_data['id_seat']
    no_seat = booking_data['no_seat']
    total = booking_data['total']
    qr_code = generate_qr(booking_id)
    jml_seat = len(no_seat)

    cur = mysql.connection.cursor() 
    cur.execute("INSERT INTO booking (id_booking, id_user, id_schedule,  id_drink, tanggal_booking, jml_seat, total, qrcode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (booking_id, user_id, id_schedule, id_drink, date, jml_seat, total, qr_code))

    for seat, no in zip(id_seat, no_seat): 
        cur.execute("INSERT INTO detail_booking (id_booking, id_seat, no_seat) VALUES (%s, %s, %s)", (booking_id, seat, no))
    mysql.connection.commit() 

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'qrcode', f'temp_qr_{booking_id}.png')
    send_file(f'temp_qr_{booking_id}.png',file_path, 'qrcode' )

    response = {'status': 'success', 'message': 'Berhasil Memesan!', 'booking_id' : booking_id}
    return jsonify(response), 200  



@app.route('/get-unavailable-Seat/<id_schedule>')
def unvailable_seat(id_schedule):
    date = datetime.now().strftime('%Y-%m-%d')
    cur = mysql.connection.cursor() 
    cur.execute("""SELECT db.id_seat
                FROM booking b
                JOIN detail_booking db using(id_booking)
                WHERE b.id_schedule=%s AND b.tanggal_booking=%s
                """, (id_schedule, date))
    result = cur.fetchall() 

    unavailable_seat = [row[0] for row in result]
    return jsonify(unavailable_seat)



@app.route('/generate_qr/<booking_id>')
def generate_qr(booking_id):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(booking_id)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    name = f"temp_qr_{booking_id}.png"
    img_temp_path = f"static/images/qrcode/{name}"
    img.save(img_temp_path)

    return name
    # return send_file(img_temp_path, mimetype='image/png', as_attachment=True)



@app.route('/get-transaction/<id_booking>', methods=['POST'])
def get_transaksi(id_booking):
    cur = mysql.connection.cursor() 
    cur.execute("""SELECT b.*, db.*, d.drink_name, s.id_movie, s.jam, m.title
                FROM booking b 
                JOIN detail_booking db using(id_booking)
                JOIN drink d using(id_drink)
                JOIN schedule s using(id_schedule)
                JOIN movies m using(id_movie)
                WHERE id_booking=%s
                """, (id_booking,))
    result = cur.fetchall() 

    # Menggabungkan data per id_booking
    booking_detail = {}
    for row in result:
        if row[0] not in booking_detail:
            booking_detail[row[0]] = {
                'id_booking': row[0],
                'id_user': row[1],
                'tanggal_booking': row[8],
                'jml_seat': row[3],
                'total': row[6],
                'qr_code': row[7],
                'id_schedule': row[2],  
                'no_seat': [],
                'drink': row[14],
                'title' : row[17],
                'jam' : row[16],
                'minuman' : row[14],
            }
        booking_detail[row[0]]['no_seat'].append(row[12])

    # Mengonversi set ke list untuk no_seat
    for booking in booking_detail.values():
        booking['no_seat'] = list(set(booking['no_seat']))

    return jsonify({"booking_detail": list(booking_detail.values())})


# -----------------------------------------------------------------
# --------------------------- M O V I E --------------------------- 
# -----------------------------------------------------------------


@app.route('/showing-movies', methods=['POST']) 
def show_movie():
    date = datetime.now().strftime('%Y-%m-%d')
    cur = mysql.connection.cursor()
    cur.execute("""SELECT m.*, p.poster_name 
                FROM 
                    movies m
                INNER JOIN poster_image p USING(id_movie)
                WHERE  m.tanggal_rilis <= %s ORDER BY m.tanggal_rilis DESC
                """,(date,))
    movies = cur.fetchall()
    cur.close()
    showing_movies = [{'id_movie' : row[0], 'title':row[1], 'sinopsis':row[2], 'sutradara':row[3], 'penulis' : row[4], 'produser':row[5], 'produksi' : row[6], 'cast': row[7], 'genre' : row[8], 'durasi' : row[9], 'rating' : row[10], 'tahun' : row[12], 'poster' : row[13]} for row in movies]

    return jsonify({'showing_movies' : showing_movies})



@app.route('/upcoming-movies', methods=['POST']) 
def upcoming_movie():
    date = datetime.now().strftime('%Y-%m-%d')
    cur = mysql.connection.cursor()
    cur.execute("""SELECT m.*, p.poster_name 
                FROM 
                    movies m
                INNER JOIN 
                    poster_image p USING(id_movie)
                WHERE  m.tanggal_rilis > %s ORDER BY m.tanggal_rilis DESC
                """,(date,))
    movies = cur.fetchall()
    cur.close()
    showing_movies = [{'id_movie' : row[0], 'title':row[1], 'sinopsis':row[2], 'sutradara':row[3], 'penulis' : row[4], 'produser':row[5], 'produksi' : row[6], 'cast': row[7], 'genre' : row[8], 'durasi' : row[9], 'rating' : row[10], 'tahun' : row[12], 'poster' : row[13]} for row in movies]

    return jsonify({'showing_movies' : showing_movies})



@app.route('/get-movie-detail/<id_movie>', methods=['POST'])
def movie_detail(id_movie):
    cur = mysql.connection.cursor() 
    cur.execute("SELECT m.*, p.poster_name FROM movies m JOIN poster_image p using(id_movie) WHERE id_movie=%s",(id_movie,))
    movies = cur.fetchone()
    
    movies_detail =[{'id_movie' : movies[0], 'title':movies[1], 'sinopsis':movies[2], 'sutradara':movies[3], 'penulis' : movies[4], 'produser':movies[5], 'produksi' : movies[6], 'cast': movies[7], 'genre' : movies[8], 'durasi' : movies[9], 'rating' : movies[10], 'tanggal_rilis' : movies[11],'tahun' : movies[12], 'poster' : movies[13]}]

    return jsonify({'movies' : movies_detail})



@app.route('/validate-movie/<id_movies>', methods=['POST'])
def validate_id_movies(id_movies):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM movies WHERE id_movie = %s", (id_movies,))
    count = cur.fetchone()[0]
    cur.close()
    if count:
        return '', 200
    else:
        return '', 404



@app.route('/add-movies', methods=["POST"])
def add_movies(): 
    try: 
        subfolder = 'poster'
        data = request.form
        gambar = request.files['poster']
        judul = data['judul']
        sinopsis = data['sinopsis']
        penulis = data['penulis']
        sutradara = data['sutradara']
        produser = data['produser']
        produksi = data['produksi']
        durasi = data['durasi']
        rating = data['rating']
        tanggal_rilis = data['tanggal_rilis']
        tahun = data['tahun']
        cast = data['cast']
        genre = data['genre']
        id_movie = generate_movie_id()

        image_filename = secure_filename(gambar.filename)
        save_image(gambar, subfolder)

        try : 
            cur = mysql.connection.cursor() 
            cur.execute("INSERT INTO movies (id_movie, title, sinopsis, sutradara, penulis, produser, produksi, cast, genre, durasi, rating, tanggal_rilis, tahun) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id_movie, judul, sinopsis, sutradara, penulis, produser, produksi, cast, genre, durasi, rating, tanggal_rilis, tahun,))
            cur.execute("INSERT INTO poster_image (id_movie, poster_name) VALUES (%s, %s)", (id_movie, image_filename))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            error_message = str(e)
            print(error_message)



        response = {'status': 'success', 'message': 'Berhasil Menyimpan Data Film!'}
        return jsonify(response), 200 
     
    except Exception as e:
        error_message = str(e)
        response = {'status': 'error', 'message': 'Gagal Mengubah Produk', 'error': error_message}
        return jsonify(response), 500 



@app.route('/get-all-movies', methods=["POST"])
def all_movies() : 
    cur = mysql.connection.cursor() 
    cur.execute("SELECT m.*, p.poster_name FROM movies m JOIN poster_image p using(id_movie)")
    result = cur.fetchall() 

    movies = [{'id_movie' : row[0], 'title' : row[1],'sinopsis' : row[2], 'sutradara' : row[3], 'penulis' : row[4], 'produser' : row[5], 'produksi' : row[6], 'cast' : row[7], 'genre' : row[8], 'durasi' : row[9], 'rating' : row[10], 'tanggal_rilis' : row[11], 'tahun' : row[12], 'poster' : row[13]} for row in result]

    return jsonify({'movies' : movies}),200



@app.route('/delete-movie/<id_movie>', methods=['POST'])
def delete_movie(id_movie) :
    cur = mysql.connection.cursor() 
    cur.execute('DELETE FROM movies WHERE id_movie =%s', (id_movie))
    mysql.connection.commit()
    cur.close() 

    return jsonify({"Err" : False, "Message" : "Success Menghapus Film!"}), 200



@app.route('/update-movie/<id_movie>', methods=['POST'])
def update_movie(id_movie) :
    data = request.json
    title = data['title']

    cur = mysql.connection.cursor() 
    cur.execute("UPDATE movies set title=%s, sinopsis=%s, sutradara=%s, penulis=%s, produser=%s, produksi=%s, cast=%s, genre=%s, durasi=%s, rating=%s, tanggal_rilis=%s, tahun=%s", ()) 
    mysql.connection.commit() 
    cur.close() 

# -----------------------------------------------------------------
# ------------------------ S C H E D U L E ------------------------ 
# -----------------------------------------------------------------

@app.route('/get-schedule', methods=['GET','POST'])
def get_schedule(): 
    data = request.json
    schedule_id = data['schedule_id']
    cur = mysql.connection.cursor()
    cur.execute("""SELECT s.*, m.*, t.nama_theaters 
                FROM schedule s
                INNER JOIN movies m using(id_movie)
                INNER JOIN theaters t using(id_theaters)
                WHERE id_schedule=%s""",(schedule_id,))
    result = cur.fetchone()
    price = get_price(result[2])

    schedule = [{'id_schedule' : result[0], 'id_movie' : result[1], 'id_theaters' : result[2], 'jam' : result[4], 'studio' : result[5], 'price' : price}]
    schedule_detail = [{'id_schedule' : result[0], 'id_movie' : result[1], 'id_theaters' : result[2], 'tanggal_schedule' : result[3 ],'jam' : result[4], 'studio' : result[5], 'title' : result[7], 'nama_theaters' : result[19], 'price' : price}]
    
    return jsonify({'schedule' : schedule, 'schedule_detail' : schedule_detail}),200


@app.route('/schedule-detail/<id_schedule>', methods=['GET','POST'])
def schedule_detail(id_schedule): 
    cur = mysql.connection.cursor()
    cur.execute("""SELECT s.*, m.*, t.nama_theaters 
                FROM schedule s
                INNER JOIN movies m using(id_movie)
                INNER JOIN theaters t using(id_theaters)
                WHERE id_schedule=%s""",(id_schedule,))
    result = cur.fetchone()

    price = get_price(result[2])

    schedule = [{'id_schedule' : result[0], 'id_movie' : result[1], 'id_theaters' : result[2], 'jam' : result[4], 'studio' : result[5], 'price' : price}]
    schedule_detail = [{'id_schedule' : result[0], 'id_movie' : result[1], 'id_theaters' : result[2], 'jam' : result[4], 'studio' : result[5], 'title' : result[7], 'nama_theaters' : result[19], 'price' : price}]
    
    return jsonify({'schedule' : schedule, 'schedule_detail' : schedule_detail}),200


@app.route('/get-schedule-movie/<id_movies>', methods=['POST'])
def schedule_movie(id_movies):
    date = datetime.now().strftime('%Y-%m-%d')
    cur = mysql.connection.cursor() 
    cur.execute("""SELECT s.*, t.nama_theaters
                FROM schedule s
                JOIN theaters t using(id_theaters)
                WHERE id_movie=%s AND tanggal_schedule=%s """,(id_movies, date))
    result = cur.fetchall()
    cur.close()

    print(result)

    movie_schedule = [{'id_schedule' : row[0], 'id_movie' : row[1], 'id_theaters' : row[2], 'jam':row[4], 'studio' : row[5], 'nama_theaters' : row[6], 'price' : get_price(row[2]), 'tanggal' : row[3]} for row in result]

    return jsonify({'movie_schedule' : movie_schedule}),200



@app.route('/schedule-list', methods=['GET','POST'])
def schedule_list(): 
    date = datetime.now().strftime('%d-%m-%Y')
    cur = mysql.connection.cursor()
    cur.execute("""SELECT s.*, m.title, t.nama_theaters
                FROM  schedule s 
                JOIN movies m using(id_movie)
                JOIN theaters t using(id_theaters) 
                ORDER BY tanggal_schedule DESC
                """,)
    result = cur.fetchall()


    schedule = [{'id_schedule' : row[0], 'tanggal':row[3], 'nama_theaters' : row[7], 'title' : row[6],'jam' : row[4], 'studio' : row[5]} for row in result]
    
    return jsonify({'data' : schedule}),200



@app.route('/get-all-theaters', methods=['POST'])
def all_theater() : 
    cur = mysql.connection.cursor() 
    cur.execute("SELECT * FROM theaters")
    result = cur.fetchall()

    theaters = [{'id_theaters' : row[0], 'nama_theaters' : row[1], 'alamat_theaters' : row[2], 'no_telp' : row[3], 'region' : row[5]} for row in result]

    return jsonify({'theaters' : theaters}), 200



@app.route('/add-schedule', methods=["POST"])
def add_schedule() : 
    try : 
        data = request.json
        id_movie = data['id_movie']
        id_theaters = data['id_theater']
        tanggal = data['tanggal']
        jam = data['jam']
        studio = data['studio']
        id_schedule = generate_id_schedule(id_theaters)

        cur = mysql.connection.cursor() 
        cur.execute("INSERT INTO schedule (id_schedule, id_movie, id_theaters, tanggal_schedule, jam, studio) VALUES (%s, %s, %s, %s, %s, %s)",(id_schedule, id_movie, id_theaters, tanggal, jam, studio))
        mysql.connection.commit() 

        return jsonify({'Err' : False, 'message' : 'Berhasil Menambahkan Jadwal!'}), 200
    except Exception as e : 
        error_message = str(e)
        print(error_message)
        return jsonify({'Err': True ,'message' : error_message}), 500



@app.route('/get-theater-schedule/<id_theater>', methods=['POST'])
def theater_schedule(id_theater) :
    date = datetime.now().strftime('%Y-%m-%d')
    cur = mysql.connection.cursor()
    cur.execute("""SELECT s.*, m.*, t.nama_theaters, p.poster_name
                FROM schedule s
                INNER JOIN movies m using(id_movie)
                INNER JOIN theaters t using(id_theaters)
                INNER JOIN poster_image p using(id_movie)
                WHERE id_theaters=%s AND s.tanggal_schedule=%s
                ORDER BY 
                CAST(SUBSTRING_INDEX(jam, ':', 1) AS UNSIGNED),
                CAST(SUBSTRING_INDEX(jam, ':', -1) AS UNSIGNED)
                """,(id_theater, date,))
    result = cur.fetchall()
    cur.close()
    # schedule = [{'id_schedule' : row[0], 'id_movie' : row[1], 'id_theaters' : row[2], 'jam' : row[4], 'studio' : row[5], 'price' : get_price(row[2]), 'title' : row[7], 'tanggal' : row[3] } for row in result]

    schedule_dict = {}
    for row in result:
        key = (row[1], row[2])  
        if key in schedule_dict:
            schedule_dict[key]['jam'].append(row[4])
        else:
            schedule_dict[key] = {
                'id_schedule': row[0],
                'id_movie': row[1],
                'id_theaters': row[2],
                'studio': row[5],
                'price': get_price(row[2]),
                'title': row[7],
                'tanggal': row[3],
                'jam': [row[4]],
                'genre': row[14],
                'durasi': row[15],
                'rating': row[16],
                'poster': row[20],
                'nama_theaters': row[19]
            }

    schedule = list(schedule_dict.values())

    return jsonify({'schedule' : schedule}), 200



@app.route('/delete-schedule', methods=['POST'])
def delete_schedule() : 
    try : 
        data = request.json 
        id_schedule = data['id_schedule']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM schedule WHERE id_schedule=%s", (id_schedule,))
        mysql.connection.commit() 

        return jsonify({"Err" : False, "message" : "Berhasil Menghapus Schedule!"})
    except Exception as e : 
        error_message = str(e)
        return jsonify({"Err" : True, "message" : error_message })



@app.route('/update-schedule', methods=['POST'])
def update_schedule() : 
    try : 
        data = request.json 
        id_schedule = data['id_schedule']
        tanggal = data['tanggal']
        jam = data['jam']
        studio = data['studio']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE schedule SET tanggal_schedule=%s, jam=%s, studio=%s   WHERE id_schedule=%s", (tanggal, jam, studio, id_schedule))
        mysql.connection.commit() 

        return jsonify({"Err" : False, "message" : "Berhasil Mengubah Schedule!"})
    except Exception as e : 
        error_message = str(e)
        return jsonify({"Err" : True, "message" : error_message })


# -----------------------------------------------------------------
# --------------------------- D R I N K --------------------------- 
# -----------------------------------------------------------------

@app.route('/get-drink', methods=['POST'])
def get_drink():
    cur = mysql.connection.cursor() 
    cur.execute("SELECT * FROM drink")
    drink = cur.fetchall() 

    drink = [{'id_drink' : row[0], 'drink_name' : row[1], 'image_drink' : row[2]} for row in drink]

    return jsonify({'drink' : drink})



# -----------------------------------------------------------------
# ------------------------ T H E A T E R S ------------------------ 
# -----------------------------------------------------------------

@app.route('/theaters-list/<region>', methods=['POST'])
def theaters_list(region):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM theaters WHERE region =%s", (region,))
    result = cur.fetchall()
    cur.close()

    theaters = [{ "theaters_id" : row[0] ,"nama_theaters" : row[1], 'alamat' : row[2], 'no_telp' : row[3], 'price1' : row[4], 'price2' : row[5], 'price3' : row[6]} for row in result]

    return jsonify({'bioskop' : theaters})


@app.route('/get-theater/<id_theater>', methods=['POST'])
def get_theater(id_theater):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM theaters WHERE id_theaters =%s", (id_theater,))
    result = cur.fetchall()
    cur.close()

    theaters = [{ "theaters_id" : row[0] ,"nama_theaters" : row[1], 'alamat' : row[2], 'no_telp' : row[3], 'price1' : row[4], 'price2' : row[5], 'price3' : row[6]} for row in result]

    return jsonify({'bioskop' : theaters})

@app.route('/theaters-all', methods=['POST'])
def theaters_all():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM theaters")
    result = cur.fetchall()
    cur.close()

    theaters = [{ "theaters_id" : row[0] ,"nama_theaters" : row[1], 'alamat' : row[2], 'no_telp' : row[3], 'price1' : row[4], 'price2' : row[5], 'price3' : row[6]} for row in result]

    return jsonify({'bioskop' : theaters})



@app.route('/delete-theater/<id_theater>', methods=['POST'])
def delete_theater(id_theater) :
    try :
        cur = mysql.connection.cursor() 
        cur.execute("DELETE FROM theaters WHERE id_theaters=%s", (id_theater))
        mysql.connection.commit() 
        cur.close() 

        return jsonify({'Err' : False, 'Message' : 'Berhasil Menghapus Theater!'}), 200
    except Exception as e :
        error_message = str(e)
        return jsonify({'Err' : True, 'message' : error_message}),500

# -----------------------------------------------------------------
# ----------------------- C A R O U S E L ------------------------- 
# -----------------------------------------------------------------

@app.route('/add-carousel', methods=['POST'])
def add_carousel() :
    try:
        subfolder = "carousel"
        images = request.files.getlist('images[]')
        titles = request.form.getlist('titles[]')

        for i in range(len(images)): 
            image = images[i]
            title = titles[i]
            image_filename = image.filename

            cur = mysql.connection.cursor() 
            cur.execute("INSERT INTO carousel (nama_carousel, image_carousel) VALUES (%s, %s)", (title, image_filename))
            mysql.connection.commit()

            save_image(image, subfolder)

        return jsonify({'message' : 'success'}), 200
    except Exception as e :
        error_message = str(e)
        print(error_message)
        return jsonify({'message' : error_message}), 500



@app.route('/get-carousel', methods=['POST'])
def get_carousel() : 
    cur = mysql.connection.cursor() 
    cur.execute('SELECT * FROM carousel')
    result = cur.fetchall() 

    carousel = [{'id_carousel' : row[0], 'nama_carousel' : row[1], 'image_carousel': row[2]} for row in result]

    return jsonify({'carousel' : carousel})



@app.route('/delete-carousel/<int:id>', methods=['POST'])
def delete_carousel(id) : 
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM carousel WHERE id_carousel=%s', (id,))
    mysql.connection.commit() 
    cur.close()

    return jsonify({'Message' : "Success Delete Carousel!"}), 200



# -----------------------------------------------------------------
# --------------------------- U S E R ----------------------------- 
# -----------------------------------------------------------------

@app.route('/get-riwayat-transaksi/<id_user>', methods=['POST'])
def get_riwayat(id_user) :
    cur = mysql.connection.cursor() 
    cur.execute("""SELECT b.*, db.*, d.drink_name, s.id_movie, s.jam, m.title, t.nama_theaters
                FROM booking b 
                JOIN detail_booking db using(id_booking)
                JOIN drink d using(id_drink)
                JOIN schedule s using(id_schedule)
                JOIN movies m using(id_movie)
                JOIN theaters t using(id_theaters)
                WHERE id_user=%s
                ORDER BY tanggal_booking DESC
                """, (id_user,))
    result = cur.fetchall() 

    booking_detail = {}
    for row in result:
        if row[0] not in booking_detail:
            booking_detail[row[0]] = {
                'id_booking': row[0],
                'id_user': row[1],
                'tanggal_booking': row[8],
                'jml_seat': row[5],
                'total': row[6],
                'qr_code': row[7],
                'id_schedule': row[2],  
                'no_seat': [],
                'drink': row[14],
                'title' : row[17],
                'jam' : row[16],
                'theaters' : row[18]
            }
        booking_detail[row[0]]['no_seat'].append(row[12])

    # Mengonversi set ke list untuk no_seat
    for booking in booking_detail.values():
        booking['no_seat'] = list(set(booking['no_seat']))

    return jsonify({"riwayat": list(booking_detail.values())})



# -----------------------------------------------------------------
# ----------------------- M I D T R A N S ------------------------- 
# -----------------------------------------------------------------

@app.route('/token-transaction', methods=['POST'])
def token_transaction() :
    try : 
        data = request.json 
        ticket = data['items']
        subtotal = data['subtotal']
        id_user = data['user_id']
        id_drink = data['id_drink']
        id_schedule = data['id_schedule']
        id_seat = data['id_seat']
        booking_id = generate_bookingId()
        qr_code = generate_qr(booking_id)

        items = []
        seat = []

        for x in ticket['id'] :
            price = ticket['price']/len(ticket['id'])-9000
            seat.append(x)
            items.append({"id" : x, 'price' : price, 'quantity' : 1, 'name' : 'Tiket Reguler'})


        cur = mysql.connection.cursor() 
        cur.execute("SELECT drink_name FROM drink WHERE id_drink=%s", (id_drink,))
        drink = cur.fetchone() 
        items.append({'id' : id_drink, 'price' : '9000', 'quantity' : len(ticket['id']), 'name' : drink[0]})

        cur.execute("SELECT nama, no_telp, alamat, email FROM users WHERE id_user=%s", (id_user,))
        user = cur.fetchone()

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'qrcode', f'temp_qr_{booking_id}.png')
        send_file(f'temp_qr_{booking_id}.png',file_path, 'qrcode' )

        token = get_token(user, items, subtotal, booking_id, id_schedule, seat, qr_code, id_user, id_drink, id_seat)

        return jsonify(token), 200
    except Exception as e : 
        error_message = str(e)
        return jsonify({'Err' : True, 'message' : error_message}), 500

@app.route('/update-status-transaksi', methods=['POST'])
def status_transakasi() : 
    data = request.json
    status = data['status']
    id_booking = data['id_booking']

    if status == "settlement" : 
        status = 'success'

    cur = mysql.connection.cursor() 
    cur.execute("UPDATE booking SET status = %s WHERE id_booking = %s",(status, id_booking,))
    mysql.connection.commit() 

    return jsonify({'Err' : False, 'message' : 'Success Update Transaction Status!'}), 200


@app.route('/notification_handler', methods=['POST'])
def notification_handler():
    print('Notification Handler')
    # request_json = request.get_json()
    request_json = request.json
    transaction_status_dict = core.transactions.notification(request_json)

    print(request_json)

    order_id           = request_json['order_id']
    transaction_status = request_json['transaction_status']
    fraud_status       = request_json['fraud_status']
    transaction_json   = json.dumps(transaction_status_dict)

    summary = 'Transaction notification received. Order ID: {order_id}. Transaction status: {transaction_status}. Fraud status: {fraud_status}.<br>Raw notification object:<pre>{transaction_json}</pre>'.format(order_id=order_id,transaction_status=transaction_status,fraud_status=fraud_status,transaction_json=transaction_json)

    # [5.B] Handle transaction status on your backend
    # Sample transaction_status handling logic
    if transaction_status == 'capture':
        if fraud_status == 'challenge':
            # TODO set transaction status on your databaase to 'challenge'
            cur = mysql.connection.cursor() 
            cur.execute("UPDATE booking SET status = %s WHERE id_booking = %s",(transaction_status, order_id,))
            mysql.connection.commit() 

        elif fraud_status == 'accept':
            # TODO set transaction status on your databaase to 'success'
            cur = mysql.connection.cursor() 
            cur.execute("UPDATE booking SET status = %s WHERE id_booking = %s",(transaction_status, order_id,))
            mysql.connection.commit() 

    elif transaction_status == 'settlement':
        # TODO set transaction status on your databaase to 'success'
        cur = mysql.connection.cursor() 
        cur.execute("UPDATE booking SET status = %s WHERE id_booking = %s",('success', order_id,))
        mysql.connection.commit() 
        
    elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
        # TODO set transaction status on your databaase to 'failure'
        cur = mysql.connection.cursor() 
        cur.execute("UPDATE booking SET status = %s WHERE id_booking = %s",(transaction_status, order_id,))
        mysql.connection.commit() 
        
    elif transaction_status == 'pending':
        # TODO set transaction status on your databaase to 'pending' / waiting payment
        cur = mysql.connection.cursor() 
        cur.execute("UPDATE booking SET status = %s WHERE id_booking = %s",(transaction_status, order_id,))
        mysql.connection.commit() 

    elif transaction_status == 'refund':
        # TODO set transaction status on your databaase to 'refund'
        cur = mysql.connection.cursor() 
        cur.execute("UPDATE booking SET status = %s WHERE id_booking = %s",(transaction_status, order_id,))
        mysql.connection.commit() 

    # app.logger.info(summary)
    return jsonify(summary)



# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------

def setPassword(password):
    password = bcrypt.generate_password_hash(password)
    return password



def checkPassword(hash, password):
    password = bcrypt.check_password_hash(hash, password)
    return password



# def generate_userId():
#     date = datetime.now().strftime('%m%d')
#     angka = ''.join(random.choices(string.digits, k=7))
#     user_id = f"{date}{angka}"



def generate_id_schedule(id_theaters):
    huruf = ''.join(random.choices(string.ascii_uppercase, k=3))
    return f"{id_theaters[:3]}{huruf}"



def get_price(id_theaters) : 
    days = datetime.now().strftime('%w')
    cur = mysql.connection.cursor()
    cur.execute("SELECT price1, price2, price3 FROM theaters WHERE id_theaters=%s",(id_theaters,))
    result = cur.fetchone()

    if days >='1' and days <='3' :
        return  int(result[0])
    elif days >= '4'  :
        return int(result[1])
    else :
        return int(result[2])



def format_tanggal(tanggal_string):
    tanggal = datetime.strptime(tanggal_string, '%a, %d %b %Y %H:%M:%S %Z')
    formatted_tanggal = tanggal.strftime('%d-%m-%Y')
    return formatted_tanggal


def generate_bookingId():
    angka = ''.join(random.choices(string.digits, k=5))
    id_booking = (f"{angka}") 
    return id_booking



def generate_user_id(birth_date):
    birth_year, birth_month, _ = birth_date.split('-')
    angka = ''.join(random.choices(string.digits, k=4))
    user_id = birth_month + birth_year + angka
    return user_id



def save_image(file, subfolder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], subfolder, filename)
        file.save(file_path)
        send_file(filename, file_path, subfolder)



def send_file(name, file_path, subfolder):
    url = 'http://127.0.0.1:5000/save-image'
    
    with open(file_path, 'rb') as file:
        files = {'file': (name, file, 'multipart/form-data')}
        data = {'subfolder': subfolder}
        response = requests.post(url, files=files, data=data)

    return response.json()



def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def generate_movie_id():
    angka = ''.join(random.choices(string.digits, k=3))
    movie_id = f'MV{angka}'

    return movie_id




if __name__== "__main__":
    app.run(debug=True, port=4000)