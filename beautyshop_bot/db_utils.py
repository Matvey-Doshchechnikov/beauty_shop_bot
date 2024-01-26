from beautyshop_bot.models import Salon, Master, Speciality, Order, Client

from datetime import datetime, timedelta


def get_salon_contacts():
    salons = Salon.objects.all()
    contacts = [
        {
            "name": salon.name,
            "address": salon.address,
            "phone": salon.phone,
        }
        for salon in salons
    ]
    return contacts


def get_masters():
    masters = Master.objects.all()
    result = [
        {
            "name": master.name,
            "surname": master.surname,
            "specialities": [
                sp.name for sp in master.speciality.all()
            ]
        }
        for master in masters
    ]
    return result

def get_master_and_timeslots(master_name):
    master = Master.objects.filter(name=master_name).first()
    # print(master)
    orders_for_master = Order.objects.filter(
        master=master,
    )
    # print(orders_for_master)
    occupied_hours = [ ts.order_time for ts in orders_for_master]

    # print(occupied_hours)
    available_time_slots = master.working_hours.all()
    # print(available_time_slots)
    hours = {}
    for ts in available_time_slots:
        # print(ts.salon.name, hours.get(ts.salon.name, []).append(1) )
        hours[ts.salon.name] = hours.get(ts.salon.name, [])
        hours[ts.salon.name].extend(list(
            ts.start_time + timedelta(hours=i) for i in range(0, (ts.end_time.hour - ts.start_time.hour)) if ts.start_time + timedelta(hours=i) not in occupied_hours
        ))
    return hours

def make_order(order_data):
    # TODO: finish client creation
    client = Client.objects.get_or_create(
        name=order_data['client_name'],
        surname=order_data['client_surname'],
        phone="test",
        telegram_chat_id="test",
        telegram_nickname="test",
    )
    print(client)
    master = Master.objects.filter(name=order_data['master_name']).first()
    print(master)
    order = Order.objects.get_or_create(
        customer=client[0],
        master=master,
        order_time=datetime.strptime(order_data['date'], "%d/%m - %H"),
    )
    print(order)
    return order