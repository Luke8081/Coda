from datetime import datetime
import time
from pprint import pprint
from zapv2 import ZAPv2
import requests, os.path


class Assesment:
    def __init__(self, addresses, verbose):

        self.API_key = 'goqjhdjmm0vid6f7v2uftgn68d'
        self.verbose = verbose
        self.addresses = addresses
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.address_counter = 0
        
    
    def active_Scan(self, address):

        fileName = f"{address}_{self.date}"
        #Create file
        open("fileName", "w").close()

        #Gets all of the sites directories
        self.spider(address)

        #Start the active scan
        scanID = self.zap.ascan.scan(address)

        if self.verbose:
            print('Active Scanning target {}'.format(address))
            while int(self.zap.ascan.status(scanID)) < 100:
                # Loop until the scanner has finished
                print('Scan progress %: {}'.format(self.zap.ascan.status(scanID)))
                time.sleep(2)

            print('Active Scan completed')
            # Print vulnerabilities found by the scanning
            print('Hosts: {}'.format(', '.join(self.zap.core.hosts)))
            print('Alerts: ')
            print(self.zap.core.alerts(baseurl=address))
        else:
            while int(self.zap.ascan.status(scanID)) < 100:
                time.sleep(2)
        
        #Get the report of the scan
        self.get_Report(address)


    def spider(self, address):

        scanID = self.zap.spider.scan(address)

        if self.verbose:
            print(f'Spidering target {address}')
            
            #Prints the progress
            while int(self.zap.spider.status(scanID)) < 100:
                print('Spider progress %: {}'.format(self.zap.spider.status(scanID)))
                time.sleep(1)
            print('Spider has completed!')
            # Prints the URLs the spider has crawled
            print('\n'.join(map(str, self.zap.spider.results(scanID))))
        else:
            while int(self.zap.spider.status(scanID)) < 100:
                time.sleep(2)
        
    
    def scan_Ports():
        pass
    
    def run_Assesment(self):
        start_timer = time.perf_counter()

        #Connects to API. Connects to 127.0.0.1 on port 8080
        self.zap = ZAPv2(apikey=self.API_key)

        #Loop through address and scan each one and time how long it takes
        for address in self.addresses:
            self.active_Scan(address)
            self.address_counter += 1
            
        stop_timer = time.perf_counter()
        self.time = round(stop_timer - start_timer, 2)
    
    def log(self):
        #Check that assesment has been run before trying to log
        if hasattr(self, 'time') == False:
            raise Exception("Run assesment before recording log")
        
        msg = f"\nScanned {self.address_counter} addresses in {self.time} seconds. Completed on {self.date_time}\n"
        print(msg)

        file = open('scan_log.txt', 'a')
        file.write(msg)
        file.close()
    
    def get_Report(self, address):

        
        
        #Connect to API and download report

        headers = {
        'Accept': 'application/json',
        'X-ZAP-API-Key': self.API_key
        }

        response = requests.get(f"http://127.0.0.1:8080/OTHER/core/other/htmlreport/", params={
        }, headers = headers)

        if (response.status_code == 200):
            file = open('TEST.html', 'w')
            file.write(response.content.decode('utf-8'))
            file.close()
            if (self.verbose):
                print("Created HTML report. File name: ")
        else:
            raise Exception("Failed to get report. Couldn't connect to API")
    


        


        
    


def main():
    address_counter = 0
    #Read addresses from file and store as list
    addresses = open('addresses.txt', 'r').read().split('\n')
    
    test = Assesment(addresses, verbose=False)
    test.run_Assesment()
    test.log()

if __name__ == "__main__":
    main()

    


