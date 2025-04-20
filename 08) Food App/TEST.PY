from datetime import time

# for h in range(24):
#     for m in range(30):
#         print(time(h,m).strftime('%I:%M %P'))


# for h in range(24):
#         for m in [0, 30]:  # 30-minute intervals
#             formatted_time = time(h, m).strftime('%I:%M %p')
#             print(formatted_time)

t = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p') ) for h in range(24) for m in [0, 30] ]
print(t)