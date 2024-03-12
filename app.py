from flask import Flask, render_template,request
import pickle
import numpy as np

def pediction(list):
    filename = 'Model/predictor.pickle'
    with open(filename,'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([list])
    return pred_value
    

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    pred = 0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typeName = request.form['typeName']
        operatingSystem = request.form['operatingSystem']
        cpu = request.form['cpu']
        gpu = request.form['gpu']
        touchScreen =  request.form.getlist('touchScreen')
        ips =  request.form.getlist('ips')

        #print("Received form data:", ram, weight, company, typeName, operatingSystem, cpu, gpu, touchScreen, ips)

        # Perform further processing or call your prediction function here
        feature_list = []

        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchScreen))
        feature_list.append(len(ips))

        company_list = ['Acer', 'Apple', 'Asus', 'Dell', 'HP', 'Lenovo', 'MSI', 'Other', 'Toshiba']
        type_name_list = ['2 in 1 Convertible', 'Gaming', 'Netbook', 'Notebook', 'Ultrabook', 'Workstation']
        os_list = ['Linux', 'Mac', 'Other', 'Windows']
        cpu_list = ['AMD', 'Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'Other']
        gpu_list = ['AMD', 'Intel', 'Nvidia']

        def  traverse(lst,value):
            for i in lst:
                if i == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
   
        traverse(company_list,company)    
        traverse(type_name_list,typeName)
        traverse(os_list,operatingSystem)
        traverse(cpu_list,cpu)
        traverse(gpu_list,gpu)

        #print(feature_list)
        pred = pediction(feature_list)* 336 
        pred = round(float(np.round(pred[0], 2)), 2)
        pred = '{:,.2f}'.format(pred)
        #print(pred)

         # If GET, just show the form page
    return render_template('index.html', pred = pred)  # Replace with your actual form template

if __name__ == '__main__':
    app.run(debug=True)
