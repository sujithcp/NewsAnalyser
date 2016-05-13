import datetime

from event_in_window import detectEvent


def final(start_date, end_date,window_size):
    window_size-=1

    current_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    final_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    events=[]
    while current_date <= final_date:
        next_date = (current_date + datetime.timedelta(days=window_size))

        events.append(detectEvent(current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d')))

        current_date = next_date + datetime.timedelta(days=1)

    for window in events:
        print('\n\n<<< Trending Events : ', window[0], '-', window [1])
        if window [2] ==[]:
            print('  No new trending events in news')
        else:
            for i in window [2]:
                print(' ',i)

final("2016-05-01","2016-05-12",2)