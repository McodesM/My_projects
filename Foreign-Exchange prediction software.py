import datetime
import time
import matplotlib.pyplot as plt
from matplotlib import style
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext, messagebox
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
from numpy import ones,vstack
from numpy.linalg import lstsq
import fxcmpy
import datetime as dt
from scipy.interpolate import interp1d
import scipy.spatial.distance as ssd 
import scipy.stats as ss
import email, smtplib, ssl

'NO SUPPORT LINES ON USD/JPY AND EUR/JPY BECAUSE RANGE OF SUPPORT RESISTANCE TO SMALL FOR THEM'


window = Tk()
window.title("Forex Pred software")
window.geometry("450x200")
lbl = Label(window, text = "Forex Pred Software", font = ("Century Gothic", 10))
lbl.pack()
lbl.place(x = 170, y = 0)

style = Style()
style.configure("TButton",foreground = "black", background = "blue")

token = 'Enter'

con = fxcmpy.fxcmpy(access_token = token, log_level = 'error', log_file = None)


for widget in window.winfo_children():
   widget.destroy()
class forex:
    def __init__ (self, currency, ex_currency):
        self.currency = str(currency)
        self.ex_currency = str(ex_currency)
   
    def Exchange(self, currency, ex_currency):
       
       pair = (currency + '/' + ex_currency)
       data = con.get_candles(pair, period = 'H4', number = 60)
       return(data)
 

def Forex_prediction():
    for widget in window.winfo_children():
        widget.destroy()
        
    currency_pred = Combobox(window)
    currency_pred['values'] = ('USD','GBP','AUD','JPY','EUR')
    currency_pred.current(1)
    currency_pred.pack()
    currency_pred.place(x = 222, y = 7)
    currency_pred.focus()
    currency_label_pred = Label(window, text = "Please enter Currency Buy/Sell For:  ", font = ("Century Gothic", 10))
    currency_label_pred.pack()
    currency_label_pred.place(x = 0, y = 7)
    
    ex_currency_pred = Combobox(window)
    ex_currency_pred['values'] = ('USD','GBP','AUD','JPY','EUR')
    ex_currency_pred.current(1)
    ex_currency_pred.pack()
    ex_currency_pred.place(x = 246, y = 28)
    ex_currency_label_pred = Label(window, text = "Please enter Currency Buy/Sell Against:  ", font = ("Century Gothic", 10))
    ex_currency_label_pred.pack()
    ex_currency_label_pred.place(x = 0 , y = 28)

    

    
    def Pred_Calculate():
        currency = currency_pred.get()
        cur = currency_pred.get()
        ex_currency = ex_currency_pred.get()

        now = str(datetime.datetime.now())
        year = now[0:4]
        month = now[5:7]
        day = now[8:10]
        hour = now[11:13]
        minute = now[14:16]
        
        filename = (minute + "_" + hour + "_" + day + "_" + month + "_" + year)
        print(filename)
        
        def Pred_Use_inputs(currency, ex_currency, filename, cur):
            choice = forex(currency, ex_currency)
            conversion = choice.Exchange(currency, ex_currency)
            
            
                
            def form(filename):
                f = open("FXnotes.txt", "w")
                f.write(str(conversion))
                f.close()
                
                
                fig, ax1 = plt.subplots(2)

                graph_data = open("FXnotes.txt", "r").read()
                lines = graph_data.split("\n")
                L = len(lines)
                L = int(L)


                a = []
                b = []
                for i in range(2, L - 2):
                    if len(lines[i]) > 1:
                       x, y = lines[i].split('  ...  ')
                       a.append(x)
                       b.append(y)


                
                f = open("FXnotes.txt", "w")
                for i in range(0, len(a)):
                    f.write((a[i]) + '\n')
                f.close()

                graph_data = open("FXnotes.txt", "r").read()
                lines = graph_data.split("\n")
                L = len(lines)
                L = int(L)

                c = []
                d = []
               
                for i in range(0, L):
                    if len(lines[i]) > 1:
                   
                       x, y = lines[i].split('   ')
                       c.append(x)
                       d.append(y)

                
                f = open("FXnotes.txt", "w")
                for i in range(0, len(d)):
                    f.write((d[i]) + '\n')
                f.close()

                graph_data = open("FXnotes.txt", "r").read()

                lines = graph_data.split("\n")

                L = len(lines)
                L = int(L)

                e = []
                f = []

                for i in range(0, L):
                    if len(lines[i]) > 1:
                       
                       x, y = lines[i].split('  ')
                       e.append(float(x))
                       f.append(y)


                
                
                f = open("FXnotes.txt", "w")
                
                for i in range(0, len(c)):
                    f.write((c[i]) + '\n')
                f.close()

                graph_data = open("FXnotes.txt", "r").read()

                lines = graph_data.split("\n")

                L = len(lines)
                L = int(L)

                g = []
                h = []

                for i in range(0, L):
                    if len(lines[i]) > 1:
                       
                       x, y = lines[i].split('  ')
                       g.append(x)
                       h.append(y)
                       
                currency = e
                Date = g
                
                cmerge = currency
                Date = np.array(Date)
                currency = np.array(currency)
                number = []
                count = 1
                while count != 61 :
                    number.append(count)
                    count = count + 1

                x_smooth = np.linspace(0, 60, 300)
                try:
                    spl = make_interp_spline(number, currency, k = 3)
                    y_smooth = spl(x_smooth)

                except:
                    print('An error has occured calculating please try again')
                    Forex_prediction()
               
                def turning_points(array1, array2):
                   
                   idx_max, idx_min, cMax, cMin = [], [], [], []
                   for i in range(2, ((len(array1)) - 1)):
                       if (array1[i]) > (array1[i + 1]) and ((array1[i]) > (array1[i - 1])):
                           cMax.append(array1[i])
                           idx_max.append(array2[i])
                       elif ((array1[i]) < (array1[i + 1])) and ((array1[i]) < (array1[i - 1])):
                           cMin.append(array1[i])
                           idx_min.append(array2[i])

                   return idx_max, idx_min, cMax, cMin

                a = turning_points(currency, Date)

                minimum = a[0]
                
                maximum = a[1]
                

                cMax = a[2]
                
             
                

                cMin = a[3]
                

                coord_max = []
                coord_min = []

                control1 = []
                control2 = []
                
                
                for i in range(0, len(cMax) - 2):

                    if len(control1) != 0:
                           control1 = []
                    
                    if ((cMax[i + 1] - cMax[i]) <= 0.00072 and (cMax[i + 1] - cMax[i]) >= 0) or ((cMax[i + 2] - cMax[i]) <= 0.00072 and (cMax[i + 2] - cMax[i]) >= 0):
                        if ((cMax[i + 2] - cMax[i]) <= 0.00072 and (cMax[i + 2] - cMax[i]) >= 0) or (cMax[i + 2] - cMax[i] >= -0.00072 and (cMax[i + 2] - cMax[i]) <= 0):
                           control1.append(maximum[i])
                           control1.append(cMax[i])
                           control1.append(maximum[i + 2])
                           control1.append(cMax[i + 2])
                           coord_max.append(control1)
                        
                        else:
                           control1.append(maximum[i])
                           control1.append(cMax[i])
                           control1.append(maximum[i + 1])
                           control1.append(cMax[i + 1])
                           coord_max.append(control1)
                          
                    elif cMax[i + 1] - cMax[i] >= -0.00072 and (cMax[i + 1] - cMax[i]) <= 0 or (cMax[i + 2] - cMax[i] >= -0.00072 and (cMax[i + 2] - cMax[i]) <= 0):
                        if (cMax[i + 2] - cMax[i] >= -0.00072 and (cMax[i + 2] - cMax[i]) <= 0) or ((cMax[i + 2] - cMax[i]) <= 0.00072 and (cMax[i + 2] - cMax[i]) >= 0) :
                           control1.append(maximum[i])
                           control1.append(cMax[i])
                           control1.append(maximum[i + 2])
                           control1.append(cMax[i + 2])
                           coord_max.append(control1)
                           
                        else:
                            
                           control1.append(maximum[i])
                           control1.append(cMax[i])
                           control1.append(maximum[i + 1])
                           control1.append(cMax[i + 1])
                           coord_max.append(control1)
                          
                       
                
                
                p1 = []
                for i in range (0, len(coord_max)):
                    if len(p1) != 0:
                        p1 = []
                        
                    p1.append(coord_max[i][1])
                    plt.hlines(p1, 0, 60, 'g', linestyles = 'dashed')
                    
                    
                def msort(cmerge):
                    result = []
                    if len(cmerge) < 2:
                        return cmerge
                    mid = int(len(cmerge)/2)
                    y = msort(cmerge[:mid])
                    z = msort(cmerge[mid:])
                    while (len(y) > 0) or (len(z) > 0):
                        if len(y) > 0 and len(z) > 0:
                            if y[0] > z[0]:
                                result.append(z[0])
                                z.pop(0)
                            else:
                                result.append(y[0])
                                y.pop(0)
                        elif len(z) > 0:
                            for i in z:
                                result.append(i)
                                z.pop(0)
                        else:
                            for i in y:
                                result.append(i)
                                y.pop(0)
                    return result
                p = msort(cmerge)
                
                for i in range (0, len(coord_max)):
                   if (currency[59]) > (coord_max[i][1]):
                      if (currency[58]) > (coord_max[i][1]):
                         print('resistance not broken on R' + str(i + 1) )
                      else:
                         resist = ('ALERT ::: RESISTANCE BROKEN ON R' + str(i + 1))
                         print(resist)
               
                name = (cur + ex_currency + '.txt')
                def test(currency, name):
                   f = open(name, 'r').read()
                   lines = f.split('\n')
                   leg = len(lines)
                     
                   sim_array = []
                   z_arr = []
                   x_arr = []
                   for i in range(1, leg):
                      if len(lines[i]) > 0:
                         x, y, z = lines[i].split(' ')
                         z_arr.append(z)
                         x_arr.append(x)

                   b_arr = []
                   leg = len(z_arr)
                   Historic = []
                    
                  
                   for i in range(0, leg):
                      if len(z_arr[i]) > 1:
                         a, b, c, d, e, f = z_arr[i].split(',')
                         b_arr.append(float(b))

                   compare = []
                   future = []
                   for i in range(0, (len(b_arr) - 66)):
                      if (len(compare)) > 0:
                        compare = []
                        future = []
                      for j in range(0,60):
                         compare.append(b_arr[i + j])
                      for j in range(61, 67):
                         future.append(b_arr[i + j])
                        
                      def similiar(currency, compare):
                         
                         x = np.linspace(0, 59, num=60)
                         x2 = np.linspace(0, 59, num=60)
                         
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
                         a = str(sim[0][1])
                         a = float(a)
                         
                         if (a >= 0.95):
                            same = True
                            print(compare)
                            print(a)
                            
                         return same
                        
                      same = similiar(currency, compare)   
                      if same == True:
                         Historic.append(future)
                   if (len(Historic)) > 0:
                      return Historic
                      
                   elif (len(Historic)) == 0:
                      print('NO MATCH for graph similiar to Current Graph')
                      
                
                Historic = test(currency, name)
                if Historic == None:
                   server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                   server.login("################", "###################")
                   name = (cur + '/' + ex_currency)
                   msg = ('NO MATCH for graph similiar to Current Graph for: ' + name)
                   server.sendmail(
                      "############################",
                      "############################", 
                       msg)
                   server.quit()
                   return
                  
                def calculate(Historic):
                   num = 0
                   predicted = []
                   for j in range(0, 6):
                      if num > 0:
                         num = 0
                      for i in range(0, (len(Historic))):
                         num = (num + Historic[i][j])
                      
                      h = num/(len(Historic))
                      predicted.append(h)
                   
                   
                   return predicted
                
                predicted = calculate(Historic)
                x = [0, 1, 2, 3, 4, 5]
                ln = len(predicted)
                gradient = ((predicted[(ln - 1)] - predicted[0])/ln)
                if gradient < 0:
                   ax1[0].plot(x, predicted, 'r')
                   ax1[0].set_title('1-Day FORECAST')
                   gradient_text = (f" BEARISH change: {gradient}")
                elif gradient > 0:
                   ax1[0].plot(x, predicted, 'g')
                   ax1[0].set_title('1-Day FORECAST 4H')
                   gradient_text = (f" BULLISH change: {gradient}")
                   
                ax1[1].plot(Date, currency, 'b')
                ax1[1].set_title('Current Market 4H')
                plt.axis([0,60, p[0] - 0.0025, p[59] + 0.0025])
                plt.xlabel('Date')
                pair = (cur + '/' + ex_currency)
                plt.ylabel(pair)
                plt.xticks(rotation = 45)
                fig.savefig('plot.png')
                
                from email import encoders
                from email.mime.base import MIMEBase
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText

                subject = gradient_text
                body = resist
                sender_email = "##############################"
                receiver_email = "##############################"


                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject
                message["Bcc"] = receiver_email  

                message.attach(MIMEText(body, "plain"))

                filename = "plot.png"  


                with open(filename, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())


                encoders.encode_base64(part)


                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
                )

                message.attach(part)
                text = message.as_string()


                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("###############", "###############")
                server.sendmail(
                  "############################", 
                  "############################, 
                  text)
                server.quit()
                #plt.show()
                
            count = 0
            while count == 0:
               times = str(datetime.datetime.now())
               calltimes = ['01:00', '05:00', '09:00', '13:00', '17:00', '21:00', '22:10']
               hourtime = times[11:16]
               print(hourtime)
               if hourtime in calltimes:
                  form(filename)
               time.sleep(60)
        Pred_Use_inputs(currency, ex_currency, filename, cur)
    btn4 = Button(window, text = "Calculate", command = Pred_Calculate, style = "TButton")
    btn4.pack()
    btn4.place(x = 0 , y = 140)

    

Forex_prediction()

window.mainloop()