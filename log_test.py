import logging
import time

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s  %(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

for i in range(5):
    time.sleep(1)
    print(time.strftime('%H:%M:%S', time.localtime(time.time())) +"   page "+ str(i) + " is ready" )
    logging.info('This is info message ' + str(i))
