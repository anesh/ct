import threading
 
def run_check():
    t=threading.Timer(5, run_check)
    t.start()
    print("HTTP Request sent.")
    t.cancel()
run_check()

print("thread compleated")

