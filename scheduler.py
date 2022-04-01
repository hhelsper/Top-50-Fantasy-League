from apscheduler.schedulers.blocking import BlockingScheduler
from app import TopArtists, scheduled_job


sched = BlockingScheduler()

# sched.add_job(scheduled_job, "cron", day_of_week="mon", hour=23)
sched.add_job(scheduled_job, "interval", seconds=5)

# @sched.scheduled_job("cron", day_of_week="mon", hour=23)
# def scheduled_job():
#     # print('This job is run every weekday at 5pm.')
#     names_lists, img_lists = spotify_api()
#     for i in range(50):
#         artist_entry = TopArtists(
#             ranking=50 - i, artist_name=names_lists[i], artist_image=img_lists[i]
#         )
#         db.session.add(artist_entry)
#         db.session.commit()


sched.start()
