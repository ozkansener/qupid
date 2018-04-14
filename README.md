Big Data analytics require multi-faceted strategies for usage. With unstructured data this becomes even more complex because of the highly dimensionality of textual documents. The applied methods has the most influence on the functional and non-functional requirements for the intelligence (a.k.a. Knowledge gathering process) gathering process. Preprocessing Techniques like Term filtering, Stemming Graph preprocessing are techniques to normalize the textual data. Evaluation of the chosen methodology is hard. When you evaluate your result with users, the archived results are biased and metrics the F-measure are vulnerable for variance explosion. Therefore we rely on distance metrics which can represent the overall similarity between the content of the list of Web documents.
Our framework representante Web documents in an unique way by combining multiple learning styles for a set of Web documents we provide the users of our framework a large amount of Information from different views with different levels.


Files (Development Phase)

	
~~~~
qupid
├── README.md
├── app.py
├── links
│   ├── list.txt
│   └── vaccine.txt
├── logs
│   ├── gunicorn_access.log
│   └── gunicorn_error.log
├── requirements.txt
└── sub
    ├── __init__.py
    └── multi.py
    	
~~~~



Product:
* Dynamically N-based Multithreaded Web Scraper
* Latency which is measured in milliseconds
* Topic analysis perform via Latent DIrichlet allocation
* Document clustering via Kmeans where K- is dynamic assigned
* We call it dynamical because the parameter of K and N are determined by the numbers of requests
* Sample urls

Deployment (Optional)
* Basic Apache2.4
* Gunicorn create 4 child processes in virtual machine

Log
* Apache2.4:Worker Process, Server Process
* Gunicorn: Applicattion exceution, Applications Errros

Failure handling
* Network failure: Url should be accessed in less than 5 seconds
* Processing failure: After 10 seconds available
* Error bot: Init.D script that act as a error bot in terms of failure


We used Flask Rest Plus to automatically create the view of the RestServerices https://github.com/noirbizarre/flask-restplus and their are two ways how the Rest Server can be accessed:
* Via Graphical Interface:Follow the Simple instructions on the User Interface
* Via Api:127.0.0.1:5000/Multiple/”Replace quotes and this by your request”

Requirements:
* Tested on Mac OS
* Python 3.6.4

Additional Requirements: For Low Server Production
* Virtualty with Apache 2.4 and Reverse Proxy
* Gunicorn, Multiple workers and Logging with asynchronous workers


Installation:
* There are two installation procedure you always have to install the basic version first. We also assume that the file run.py is below this directory. This is important for location searching. /home/qupid/qupid

First approach:
>sudo pip3 install - r requirements.txt
Install other missing packages
Run the app via sudo python3 run.py

Second approach
You need to have successfully finished the application:
with apache2.4 and gunicorn. 
Install apache and make sure you have the right privilege root privileges, but not in the home directory.
>sudo pip3 gunicorn
sudo pip3 install dominate
sudo pip3 install visitor
sudo pip3 install  flask_appconfig
sudo pip3 install flask_wtf

>sudo a2enmod

Then insert: 
>proxy proxy_ajp proxy_http rewrite deflate headers proxy_balancer proxy_connect proxy_html for health checking.

Apache Configuration:
Delete de standaard index.html
We like to log everything, out attitude is like more data can be always good.
>sudo nano /etc/apache2/sites-available/apache2.conf

    <VirtualHost *:80>
    
        ServerAdmin 
    
    
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    
        <Proxy *>
            Order deny,allow
              Allow from all
        </Proxy>
        ProxyPreserveHost On
        <Location "/home/qupid/qupid">
              ProxyPass "http://127.0.0.1:5000/"
              ProxyPassReverse "http://127.0.0.1:5000/"
        </Location>
    </VirtualHost>

Run services apache
>sudo systemctl stop qupid
sudo systemctl reload qupid
sudo systemctl daemon-reload
sudo systemctl start qupid
sudo systemctl enable qupid

Shell Script Which Automatically reloads when it crashes
>sudo nano  /etc/init/testing.conf:
chdir /home/qupid/qupid
exec sudo gunicorn -c gunicorn.conf -b 0.0.0.0:5000 app:app  
respawn
exec python testing.py respawn
sudo systemctl status qupid | sed -n 's/.*Main PID: \(.*\)$/\1/g p' | cut -f1 -d' ' | xargs kill -HUP

Comment:
Don’t forget to configure your firewall.
* Please consider the following option depending our usage scenario
* nginx : high-performance HTTP, reverse proxy, IMAP/POP3 proxy server
* haproxy : high performance load balancer
* varnish : caching HTTP reverse proxy



