from __future__ import division
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import pandas as pd
import csv
import time
import datetime
from .models import users,stock,index
from .forms import stockform,loginform,registerform
import numpy as np
from sklearn import svm,preprocessing
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer,StandardScaler
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")

# Create your views here.
df={}
first_item=list()
x=list()
#df=pd.DataFrame(columns=['Date','Open','High','Low','Close','Total Trade Quantity','Turnover (Lacs)'])
def home(request):
	return render(request,"home.html")

def login1(request):
  #next=request.GET.get('next','/stock/')
  if request.method=="POST":
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(username=username,password=password)
    if user is not None:
      if user.is_active:
        login(request,user)
        return HttpResponseRedirect('/stock/')
      else:
        HttpResponse("Inactive user!")
    else:
      return HttpResponseRedirect('/stock/login/')
  return render(request,"login.html",{})

@login_required(login_url='/stock/login/')
def upload(request):
	if request.method==	'POST':
		form=stockform(request.POST,request.FILES)
		if form.is_valid():       
	#if form is valid manipulate or save to db
			q=form.save(commit=False)
			q.save()
			#upload_data = request.FILES['stock_data'].read()
			#csv_data=csv.DictReader(upload_data)
			#print("hi")
			df=pd.DataFrame.from_csv(q.stock_data)
			'''for line in q.stock_data.readlines():
										        		array = line.split(',')
									        			first_item.append(array[0])'''
			
			date_stamp=df.index
			index_df=pd.DataFrame.from_csv('uploads/'+'uploads/'+str("NSE-NIFTY_50.csv"))
			#x=len(index_df.index)
			x= len(df)
			i=0
			j=0
			#print index_df[index_df['Close']<8200]
			#print (index_df.index[100])
			#print (df.ix[0])

			df2=pd.DataFrame()
			df2['Date']=df.index 	#uploaded stock date
			df3=pd.DataFrame() 		
			df3['Date']=index_df.index  	#index stock  date
			df4=df3    						#copy of index stock date 
			df6=pd.DataFrame()
			df6['Date']=[]					#final DataFrame
			df7=pd.DataFrame()
			df7['Shares_Traded']=[] 
			df['ymd']=df.index 
			
 			#print(df3.head())
			print (x)
			#print (df.head())
			while i<1450:
				#index_value=df3.ix[i,'Date']
				#print (index_value)
				j=0
				
				if df2.empty:
					break
				while j<1450:
					if df3.ix[0,'Date']==df2.ix[0,'Date']:
						df6.loc[-1]=df3.ix[0,'Date']
						df6.index=df6.index+1	
						year=df3.ix[0,'Date']
						df7.loc[-1]=index_df.ix[year,'Shares Traded']
						df7.index=df7.index+1
						#print (str(df3.ix[0,'Date']),str(df2.ix[0,'Date']))
						df.ix[year,'Shares_Traded']=index_df.ix[year,'Shares Traded']
						
						df2=df2.drop(df2.index[0])
						df2=df2.reset_index(drop=True)
						df3=df3.drop(df3.index[0])
						df3=df3.reset_index(drop=True)
												
						break
					
				#df3.drop(df3.index[0])
					else:
						#print (str(df3.ix[0,'Date']),str(df2.ix[0,'Date']))
						a=str(df3.ix[0,'Date'])
						b=str(df2.ix[0,'Date']) 
						if a>b:
							
							df3=df3.drop(df3.index[0])
							df3=df3.reset_index(drop=True)	
							j=j+1
							continue
						elif a<b:
							for l,row in df.iterrows():
								if df.ix[l,'ymd']==df2.ix[0,'Date']:
									df.drop(l,inplace=True)
							df2=df2.drop(df2.index[0])
							df2=df2.reset_index(drop=True)
							k=0
							while k<j:
								df3=df3.drop(df3.index[0])
								df3=df3.reset_index(drop=True) 

							break
				i=i+1
						
			x=len(df)
			i=0
			del df['ymd']
			df=df.iloc[::-1]
			stock_trade=0
			index_trade=0

			for l,row in df.iterrows():
				if stock_trade==0:
					df.ix[l,'stock_p_change']=0.0
					df.ix[l,'index_p_change']=0.0
					stock_trade=df.ix[l,'Total Trade Quantity']
					index_trade=df.ix[l,'Shares_Traded']
				else:
					stock_trade2=df.ix[l,'Total Trade Quantity']
					stock_p=((stock_trade2-stock_trade)/stock_trade)*100
					df.ix[l,'stock_p_change']=stock_p
					


					index_trade2=df.ix[l,'Shares_Traded']
					index_p=((index_trade2-index_trade)/index_trade)*100
					df.ix[l,'index_p_change']=index_p
					

					df.ix[l,'Difference']=stock_p-index_p
					stock_trade=stock_trade2
					index_trade=index_trade2	

					if df.ix[l,'Difference']>0:
						df.ix[l,'Status']="outperformed"
					elif df.ix[l,'Difference']<0:
						df.ix[l,'Status']="underperformed"

			print (df.head())
			if df['Status'][-1]=="underperformed":
				color='r'
			else:
				color='g'	
			features=["Open","Close","High","Low"]

			#df=df.reindex(np.random.permutation(df))
			X=np.array(df[features].values)
			#X = Imputer().fit_transform(X)
			X=preprocessing.scale(X)
			
			y=(df["Status"]
				.replace("underperformed",0)
				.replace("outperformed",1)
				.values.tolist())
			clf=svm.SVC(kernel="linear",C=1.0)
			size=1000
			clf = Pipeline([("StandardScaler", StandardScaler()), ("svm", SVC(C=1000))])
			clf.fit(X[:-size],y[:-size])

			'''w=clf.coef_[0]
												a=-w[0]/w[1]
												xx=np.linspace(min(X[:,0]),max(X[:,0]))
												yy=a*xx-clf.intercept_[0]/w[1]
												h0=plt.plot(xx,yy,"k-",label="non weighted")
												plt.scatter(X[:,0],X[:,1])
												#df['Difference'].plot(label=q.stock_name,color=color)
												plt.xlabel("Open")
												plt.ylabel("Close")
												plt.legend()
												plt.savefig('hi.png')'''


			print(len(X))
			correct_count=0
			for x in range(1,size+1):
				if clf.predict(X[-x])[0] ==y[-x]:
					correct_count+=1
			print("Accuracy:",(correct_count/size)*100.00)
			return HttpResponseRedirect('/stock/graph/')
	else:
		form=stockform()
	return render(request,"upload.html",{"form":form})

@login_required(login_url='/stock/login/')
def graph(request):
	
	return render(request,"graph.html",{})	
	#data = request.FILES['datafile'].read()
			#df=pd.DataFrame(data)

#def key_stat(request,gather="trade"):

def register(request):
	if request.method=='POST':
		form=registerform(request.POST)
		if form.is_valid():
			q=form.save(commit=False)
			q.save()
			user=User.objects.create_user(username=q.username,password=q.password)
			user.save()
			return HttpResponseRedirect('/stock/')
	else:
		form=registerform()
	return render(request,'register.html',{"form":form})	

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/stock/')


@login_required(login_url='/stock/login/')
def list(request):
  queryset_list = stock.objects.all()
  if queryset_list.__len__()==0:
   	messages.error(request, 'List is Empty!')
	return render(request,'list.html')

  paginator = Paginator(queryset_list, 50) # Show 25 contacts per page
  page = request.GET.get('page')
  try:
    queryset = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    queryset = paginator.page(1)
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    queryset = paginator.page(paginator.num_pages)


  context = {
    "object_list" : queryset
  }
  return render(request,'list.html', context)

@login_required(login_url='/stock/login/')
def single_stock(request,id=None):
	object1 = get_object_or_404(stock, id=id)
	instance=pd.DataFrame.from_csv(object1.stock_data)
  	
  	for l,row in instance.iterrows():
  		x.append(row)
  	context={
  	 "instance":x
  	}
  	
  	return render(request,'single_stock.html',context)
