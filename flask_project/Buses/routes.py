from Buses import app, db, csrf
from Buses.models import bus_info, bus_routes
from flask import render_template, redirect, url_for, request
from Buses.forms import admin_entries, acceptFromUser
from wtforms import validators
from flask_wtf.csrf import generate_csrf
from Buses.final import predictor, predict_time_to_destination, convert_time
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

def check_departure_status(bus_entry):
    departure_time = datetime.strptime(bus_entry.predicted_time, '%H:%M:%S').time()
    current_time = datetime.now().time()
    if current_time > departure_time:
        return True
    else:
        return False

def delete_departed_buses():
    all_bus_entries = bus_info.query.all()
    for bus_entry in all_bus_entries:
        if check_departure_status(bus_entry):
            db.session.delete(bus_entry)
            db.session.commit()


@app.route('/')
@app.route('/home')
def home_page():
     return render_template('home.html')


@app.route('/available_buses')
def availableBuses():
     get_from=request.args.get('from_here')
     get_to=request.args.get('to')
     #print(f'From: {get_from}')

     get_info=bus_info.query.filter_by(current_stop=get_from, dest_stop=get_to).all()
     if get_info is None:
         print(f'Please enter a value')
     sum = 0
     time_now_hr = datetime.now().time().hour
     time_now_min = datetime.now().time().minute
     for x in get_info:
         sum+=1

     return render_template('bus_data.html',
                            info=get_info,
                            count=sum
                            )


@app.route('/user', methods=['GET', 'POST'])
def user_entries():
    csrf_token=generate_csrf()
    if request.method=='POST':
        selected_from=request.form['from']
        selected_to=request.form['to']
        return redirect(url_for('availableBuses', from_here=selected_from, to=selected_to))
    return render_template('user.html', csrf_token=csrf_token)

@app.route('/admin', methods=['GET', 'POST'])
def admin_create_new_entry():
    form=admin_entries()
    if form.validate_on_submit():
        try:
            cur_route_id=bus_routes.query.filter_by(from_stop=form.cur_stop.data).with_entities(bus_routes.route_id).first()
            if cur_route_id:
                hour=form.arrival_time.data.hour
                minute=form.arrival_time.data.minute
                whole_time = form.arrival_time.data
                time_str = f"{whole_time}"
                am_pm = whole_time.strftime("%p")
                if(am_pm == "PM"):
                    hour = hour + 12
                hour_to_sec = hour*3600
                minute_to_sec = minute*60
                time_in_sec = hour_to_sec+minute_to_sec
                time_in_sec = time_in_sec%86400
                setbit=0
                the_bus_id = form.bus_id.data
                next_predictions = predict_time_to_destination(form.cur_stop.data, form.dest_stop.data, time_in_sec, 0)
                for x in next_predictions.keys():
                    ls = ["yeola", "kopargaon", "shirdi", "pune"]
                    index_in_list=ls.index(x, 0, 4)
                    route_id_str = cur_route_id[0]
                    hr, minte, sec = convert_time(next_predictions[x])
                    ptime = f'{hr}:{minte}:{sec}'
                    if ls[index_in_list] == "pune":
                        break
                    entry_create = bus_info(bus_id = the_bus_id,
                                            current_stop=x ,
                                            dest_stop=ls[(index_in_list+1)],
                                            req_time_to_arrive_at_cur=ptime ,
                                            route_id=route_id_str)
                    db.session.add(entry_create)
                    db.session.commit()
                return redirect(url_for('user_entries'))
        except SQLAlchemyError as e:
            print(f'An error occured while accessing database', e)
        else : print('No such route')
    return render_template('bus_update.html', form=form, csrf_token=csrf)


@app.route('/adminLogin')
def login():
    return render_template('Index.html')



'''
@app.route('/update_bus_info', methods=['POST'])
def update_bus_info():
    if request.method == 'POST':
        bus_id = request.form['bus_id']

        bus_entry = bus_info.query.get(bus_id)

        if bus_entry:

            bus_entry.current_stop = request.form['current_stop']
            bus_entry.dest_stop = request.form['dest_stop']
            bus_entry.req_time_to_arrive_at_cur = request.form['arrival_time']

            db.session.commit()
            return 'Bus information updated successfully'
        else:
            return 'Bus ID not found'
'''
