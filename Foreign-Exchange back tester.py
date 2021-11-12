import numpy as np
import scipy
from scipy.interpolate import make_interp_spline, BSpline
from numpy import ones,vstack
from numpy.linalg import lstsq
from scipy.interpolate import interp1d
import scipy.spatial.distance as ssd 
import scipy.stats as ss
import matplotlib.pyplot as plt
from matplotlib import style
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# RUN ON HEROKU IT WILL TAKE 32 HOURS

array = ['EUR/USD', 'EUR/JPY', 'USD/JPY']
year = 2018
total_correct = 0
total_incorrect = 0
for s in range(0, 60):
   Cur, Ex_cur = array[s].split('/')
   name_pred =  ((Cur + Ex_cur) + '_2018.txt')
   f = open(name_pred, 'r').read()
   lines = f.split('\n')
   length = len(lines)
   pred_a = []
   
   for i in range(1, length):
      if len(lines[i]) > 0:
         x, y, z = lines[i].split(' ')
         pred_a.append(z)
   
   pred_close_price = []
   for i in range(0, len(pred_a)):
      if len(lines[i]) > 0:
         a, b, c, d, e, f = pred_a[i].split(',')
         pred_close_price.append(float(e))
   currency = []
   future_real = []


   count = 0
   for i in range(0, len(pred_a)-13):
       
      count = count + 1
      print(count)
      
      if len(currency) > 0:
         currency = []
      
      if len(future_real) > 0:
         future_real = []
      for j in range(0, 10):
         currency.append(pred_close_price[i+j])
      
      for j in range(11, 13):
         future_real.append(pred_close_price[i+j])

      name = (Cur + Ex_cur + '_Simulation.txt')
      def test(currency, name):
         f = open(name, 'r').read()
         lines = f.split('\n')
         leg = len(lines)
           
         sim_array = []
         z_arr = []
           
         for i in range(1, leg):
            if len(lines[i]) > 0:
               x, y, z = lines[i].split(' ')
               z_arr.append(z)

         e_arr = []
         leg = len(z_arr)
         Historic = []
            
          
         for i in range(0, leg):
            if len(z_arr[i]) > 1:
              a, b, c, d, e, f = z_arr[i].split(',')
              e_arr.append(float(e))

         compare = []
         future = []
         for i in range(0, (len(e_arr) - 13)):
            if (len(compare)) > 0:
               compare = []
               future = []
               
            for j in range(0,10):
               compare.append(e_arr[i + j])

            for j in range(11, 13):
               future.append(e_arr[i + j])
                
            def similiar(currency, compare):

               x = np.linspace(0, 9, num=10)
               x2 = np.linspace(0, 9, num=10)
                 
               same = False
                 
               f = interp1d(x, currency)
               f2 = interp1d(x2, compare)
               points = 15
               xnew = np.linspace ( min(x), max(x), num = points)
               xnew2 = np.linspace ( min(x2), max(x2), num = points)
               ynew = f(xnew)
               ynew2 = f2(xnew2)
                 
               sim = (np.corrcoef(ynew, ynew2)) 
               sim2 = (ss.spearmanr(ynew, ynew2))
               similarity = str(sim[0][1])
               similarity = float(similarity)
               
                 
               if (similarity >= 0.90):
                  same = True
                  
               return same
                
            same = similiar(currency, compare)   
            if same == True:
               Historic.append(future)
            
         if (len(Historic)) > 0:
              return Historic
              
              
         elif (len(Historic)) == 0:
            print('NO MATCH for graph similiar to Current Graph')

      Historic = test(currency, name)

      if Historic != None:
         def calculate(Historic):
            num = 0
            predicted = []
            for j in range(0, 2):
               if num > 0:
                  num = 0

               for i in range(0, (len(Historic))):
                  num = (num + Historic[i][j])
               
               h = num/(len(Historic))
               predicted.append(h)  
            
            return predicted
         
         predicted = calculate(Historic)

         print(predicted)
         print(future_real)
         
         pred_gradient = (predicted[1] - predicted[0])
         gradient = (future_real[1] - future_real[0])

         if (gradient >= 0) and (pred_gradient >= 0):
            total_correct = total_correct + 1
            print('correct prediction num: ' , total_correct)
            
         elif (gradient <= 0) and (pred_gradient <= 0):
            total_correct = total_correct + 1
            print('correct prediction num: ' , total_correct)

         else:
            total_incorrect = total_incorrect + 1
            print('Wrong prediction num:' , total_incorrect)
         
msg = str('BACK TEST RESULTS for year ' + str(year) + ' are total CORRECT is: ' + str(total_correct) + '    |||||    total WRONG is: ' + str(total_incorrect))
sender_email = "######################"
receiver_email =  "####################"
body = (msg)  
subject = ("BACK TEST RESULTS")

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  

message.attach(MIMEText(body, "plain"))


text = message.as_string()


server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("#############", "############")
server.sendmail(
    "###############", 
    "###############", 
    text)
server.quit()
print('This is the number of total correct: ' ,total_correct)
print('This is the number of total incorrect: ', total_incorrect)