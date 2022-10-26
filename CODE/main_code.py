import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


#continental analysis (summarized analysis):-
def continent_load():
  '''For loading the dataset to analyze the data for continents of the world'''
  df=pd.read_csv("https://github.com/SalientPharaoh/Covid-19_Visualization/blob/main/Dataset/worldometer_coronavirus_summary_data.csv") #opening a csv dataset
  #print(df.info()) #Column data and datatype
  #print(df) #viewing the dataset
  return df #return the dataframe for further analysis

def clean_data(df):
  '''Performing data cleaning and data wrangling operations on the dataframe'''

  #removing the NaN value from the dataset
  df.dropna(inplace=True)
  #removing duplicate values in the two rows, if exists
  df.drop_duplicates(inplace=True)

  df.columns=[x.lower() for x in df.columns] #converting headers to lower case
  df['country']=[x.lower() for x in df['country']] #converting country names to lower case
  df['continent']=[x.lower() for x in df['continent']] #converting continent names to lower case

  #typecasting the data into correct datatypes.
  df.total_deaths = df.total_deaths.astype('int64')
  df.total_recovered = df.total_recovered.astype('int64')
  df.active_cases=df.active_cases.astype('int64')
  df.serious_or_critical=df.serious_or_critical.astype('int64')
  df.total_deaths_per_1m_population=df.total_deaths_per_1m_population.astype('int64')
  df.total_tests=df.total_tests.astype('int64')
  df.total_tests_per_1m_population=df.total_tests_per_1m_population.astype('int64')
  df.population=df.population.astype('int64')

  return df #returning the clean dataframe

def world_averages(df):
  '''To calculate and display average parameter of world coronavirus data'''

  avg_death=df['total_deaths_per_1m_population'].mean() #method to find mean of dataframe
  avg_case=df['total_cases_per_1m_population'].mean()
  avg_test=df['total_tests_per_1m_population'].mean()

  #displaying the data:-
  print("Average Total deaths per 1 million people:-",int(round(avg_death,0)))
  print("average percentage of deaths due to covid in world:-",round((avg_death/1000000)*100,4))
  print()
  print("Average Total positive cases per 1 million people:-",int(round(avg_case,0)))
  print("average percentage of positive covid cases in world:-",round((avg_case/1000000)*100,4))
  print()
  print("Average Total covid tests done per 1 million people:-",int(round(avg_test,0)))
  print("average percentage of covid tests done in world:-",round((avg_test/1000000)*100,4))

def continent_average(df):
  '''Average parameters of continents of the world'''

  grp=df.groupby('continent') #creating a group of data based on the names of the continent
  avg_group=grp[['total_deaths_per_1m_population','total_cases_per_1m_population','total_tests_per_1m_population']].mean() 

  avg_group.rename(columns={'total_deaths_per_1m_population':'Average deaths per million people','total_cases_per_1m_population':'Average cases per million people','total_tests_per_1m_population':"Average tests per million people"},inplace=True)
  avg_group=avg_group[['Average deaths per million people','Average cases per million people','Average tests per million people']].apply(lambda x: round(x,0))
  print(avg_group) #displaying the data
  visualize_continent_average(avg_group)
  return avg_group  #returns the grouped data frame

def visualize_continent_average(avg_group):
  '''plotting the average data of the continents on a bar chart using matplotlib library'''

  avg_group.plot.barh(y='Average deaths per million people',color='black',style='o',rot='0',title='Average deaths per million people')
  plt.show()
  print()
  avg_group.plot.barh(y='Average tests per million people',color='red',style='o',rot='0',title='Average tests per million people')
  plt.show()
  print()
  avg_group.plot.barh(y='Average cases per million people',color='blue',style='o',rot='0',title='Average cases per million people')
  plt.show()
  print()

def world_critical_average(df):
  '''critical or serious case counts in countinents'''

  grp=df.groupby('continent') #grouping the data
  critical=grp['serious_or_critical','population'].agg('sum') #extracting the column with required data and aggreagting it based on the group
  critical['serious_percentage']=(critical['serious_or_critical']/critical['population'])*100 #converting the data to percentage for proper visualization
  critical['serious_percentage']=[round(x,6) for x in critical['serious_percentage']] #appending the column to dataframe 
  print(critical)  #display the data
  critical.plot.barh(y='serious_percentage',style='o',rot='0',color='orange',title='percentage of serious or critial population')
  plt.show()
  print()

def basic_country_summary(c1,c2,c3,c4,c5,df):
  '''Basic analysis of the coronavirus data summary for selected five countries'''

  #creating a new dataframe with data of only five selected countries
  ctry1=df.loc[df['country']==c1.lower()]
  ctry2=df.loc[df['country']==c2.lower()]
  ctry3=df.loc[df['country']==c3.lower()]
  ctry4=df.loc[df['country']==c4.lower()]
  ctry5=df.loc[df['country']==c5.lower()]
  new_df= pd.concat([ctry1,ctry2,ctry3,ctry4,ctry5],ignore_index=True)
  #print(new_df) #displaying the data

  visualizing_basic_country_summary(new_df) #calling another function

def visualizing_basic_country_summary(new_df):
  '''Visualizing the basic data summary of the selected five countries'''
  print("Population distribution pie-chart for the countries:-\n")
  plt.pie(new_df['population'], labels = new_df['country'], startangle=0, explode=[0.1,0.1,0,0,0]) #population analysis
  plt.show()
  print()
  ctry_grp=new_df.groupby('country')
  ctry_df=ctry_grp[['total_deaths_per_1m_population','total_cases_per_1m_population','total_tests_per_1m_population']].agg('mean')

  #plotting basic data on bar chart
  ctry_df.plot.barh(y='total_tests_per_1m_population',color='red',style='o',rot='0',title='total_tests_per_1m_population')
  plt.show()
  print()
  ctry_df.plot.barh(y='total_cases_per_1m_population',color='blue',style='o',rot='0',title='total_cases_per_1m_population')
  plt.show()
  print()
  ctry_df.plot.barh(y='total_deaths_per_1m_population',color='black',style='o',rot='0',title='total_deaths_per_1m_population')
  plt.show()
  print()
  
  multi_condition_country_plot(ctry_df,new_df) #calling another function

def multi_condition_country_plot(ctry_df,new_df):
  '''Analysing and visualizing the data based on change of two parameters'''

  ctry_df['perc_death_per_case']=(ctry_df['total_deaths_per_1m_population']/ctry_df['total_cases_per_1m_population'])*100
  ctry_df['perc_case_per_test']=(ctry_df['total_cases_per_1m_population']/ctry_df['total_tests_per_1m_population'])*100
  ctry_df['perc_death_per_test']=(ctry_df['total_deaths_per_1m_population']/ctry_df['total_tests_per_1m_population'])*100
  
  #visualizing the data
  ctry_df.plot.barh(y='perc_death_per_test',color='green',style='o',rot='0',title='Deaths per Test Percentage')
  plt.show()
  print()
  ctry_df.plot.barh(y='perc_case_per_test',color='yellow',style='o',rot='0',title='Positive cases per Test Percentage')
  plt.show()
  print()
  ctry_df.plot.barh(y='perc_death_per_case',color='turquoise',style='o',rot='0',title='Deaths per Positive case Percentage')
  plt.show()
  print()

  #plotting total cases versus total deaths per 1 million population
  #size of scatter refernces the total tests per 1 million population

  x=ctry_df['total_cases_per_1m_population']
  y=ctry_df['total_deaths_per_1m_population']

  size=(ctry_df['total_tests_per_1m_population']/1000)
  c=['yellow','green','turquoise','red','blue']
  plt.scatter(x,y,color=c,s=size)
  plt.title('Cases per million population versus Deaths per million population')
  plt.suptitle('Size of datapoint depends on Total tests per million population')

  plt.grid(color = 'black', linewidth = 0.5)
  plt.show()
  print()

  #plotting total cases versus total tests per 1 million population
  #size of scatter refernces to the population of the country

  x=ctry_df['total_cases_per_1m_population']
  y=ctry_df['total_tests_per_1m_population']

  size=(new_df['population']/1000000)
  c=['yellow','green','turquoise','red','blue']
  plt.scatter(x,y,color=c,s=size)
  plt.title('Cases per million population versus Test per million population')
  plt.suptitle('Size of datapoint depends on population of country')
  plt.grid(color = 'black', linewidth = 0.5)
  plt.show()


def main():
  df=continent_load() #loading data function
  df=clean_data(df) #cleaning data function and updating the dataframe with clean data

  ch=int(input("1.World Averages\n2.Continent wise averages\n3.Country wise summary\n4.exit\n"))
  if ch==1:
    world_averages(df) #world averages
    main()
  elif ch==2:
    average_group=continent_average(df) #continent wise averages
    world_critical_average(df) #critical and serious cases of continents in world
    main()
  elif ch==3:
    #selected country analysis:-
    selection=int(input("1.Top 5 most Populated countries of world\n2.Top 5 Economies of world\n3.Top 5 countries based on Literacy rate\n4.Top 5 countries with best medical facility\n5.5 countries of your choice.\n"))
    
    if selection==1:
      #considering top 5 countries based on population:-
      print("Analyzing the data for 5 most Populated countries:-\n1.CHINA\n2.INDIA\n3.UNITED STATES OF AMERICA\n4.INDONESIA\n5.UNITED KNIGDOM ")
      basic_country_summary('china','india','usa','indonesia','uk',df)
    elif selection==2:
      #considering top 5 countries based on Economy:-
      print("Analyzing the data for countries with top 5 economies of the world:-\n1.UNITED STATES OF AMERICA\n2.CHINA\n3.JAPAN\n4.GERMANY\n5.UNITED KNIGDOM ")
      basic_country_summary('usa','china','japan','germany','uk',df)

    elif selection==3:
      #considering top 5 countries based on litercay:-
      print("Analyzing the data for 5 most literate countries:-\n1.UZBEKISTAN\n2.UNITED STATES\n3.LATVIA\n4.ESTONIA\n5.LITHUANIA ")
      try:
        basic_country_summary('uzbekistan','usa','latvia','estonia','lithuania',df)
      except:
        print("Data Seems to be missing!")
    
    elif selection==4:
      #considering top 5 countries with best healthcare services:-
      print("Analyzing the data for countries with best Healthcare facilities:-\n1.DENMARK\n2.AUSTRIA\n3.JAPAN\n4.AUSTRALIA\n5.FRANCE ")
      try:
        basic_country_summary('denmark','austria','japan','australia','france',df)
      except:
        print("Data Seems to be missing!")

    elif selection==5:
      #Five country selection by user:-
      try:
        n=int(input("1.To analyse the data for 5 countries of your choice\n0.Done with this analysis\n"))
        while n==1:
          c1=input("Enter country 1:-\n").lower()
          c2=input("Enter country 2:-\n").lower()
          c3=input("Enter country 3:-\n").lower()
          c4=input("Enter country 4:-\n").lower()
          c5=input("Enter country 5:-\n").lower()
          basic_country_summary(c1,c2,c3,c4,c5,df)
          n=int(input("1.To analyse the data for 5 countries of your choice\n0.Done with this analysis\n"))
      except:
        print("Data Seems to be missing!")

    else:
      main()
    main()
  else:
    print("returning back!\n")
  
#country wise extensive data
def load_country():
  '''Loading and viewing the data'''

  import pandas as pd
  big_df=pd.read_csv("https://raw.githubusercontent.com/SalientPharaoh/Covid-19_Visualization/main/Dataset/worldometer_coronavirus_daily_data.csv",parse_dates=['date']) #loading data
  #parse_dates convert the column with dates to datetime datatype
  #print(big_df.info()) #column summary
  return big_df #return the loaded data frame

def country_clean(big_df):
  '''Data cleaning and data wrangling'''

  #removing rows with null values
  big_df.dropna(inplace=True)
  #removing duplicate values in the two rows
  big_df.drop_duplicates()

  big_df.columns=[x.lower() for x in big_df.columns] #converting headers to lower case
  big_df['country']=[x.lower() for x in big_df['country']] #converting country names to lower case

  #typecasting to integer 64 data type
  big_df.cumulative_total_cases=big_df.cumulative_total_cases.astype('int64')
  big_df.daily_new_cases=big_df.daily_new_cases.astype('int64')
  big_df.active_cases=big_df.active_cases.astype('int64')
  big_df.cumulative_total_deaths=big_df.cumulative_total_deaths.astype('int64')
  big_df.daily_new_deaths=big_df.daily_new_deaths.astype('int64')

  return big_df #returning cleaned dataframe

def monthly_spread(s,big_df):
  '''plotting the monthly spread data of corornavirus for a country'''

  month=big_df.set_index('date')
  month=month.loc[month['country']==s.lower(),['daily_new_cases','daily_new_deaths']]
  month=month.resample('M').sum()
  month.columns=month.columns.str.replace('daily','monthly')
  month.plot(secondary_y=['monthly_new_deaths'],title=s.upper())
  plt.suptitle('Monthly new deaths and cases due to coronavirus')
  plt.show()
  print()
  
def daily_spread(s,big_df):
  '''plotting the daily spread data of corornavirus for a country'''

  day=big_df.set_index('date')
  day=day.loc[day['country']==s.lower(),['daily_new_cases','daily_new_deaths']]
  day.plot(secondary_y=['daily_new_deaths'],title=s.upper())
  plt.suptitle('Daily new deaths and cases due to coronavirus')
  plt.show()
  print()

def cumulative_case_spread_monthly(s,big_df):
  '''plotting the cumulative monthly spread data of corornavirus for a country'''

  data_=big_df.loc[big_df['country']==s.lower(),['date','cumulative_total_cases','cumulative_total_deaths']]
  data_=data_[data_.date.isin(pd.date_range(start='2019-12-1',end='2022-07-01',freq='M'))]
  data_=data_.set_index('date')
  data_.plot(secondary_y=['cumulative_total_deaths'],title=s.upper())
  plt.suptitle('Monthly cumulative deaths and cases due to coronavirus')
  plt.show()
  print()

def cumulative_case_spread_daily(s,big_df):
  '''plotting thecumulative daily spread data of corornavirus for a country'''

  data_=big_df.loc[big_df['country']==s.lower(),['date','cumulative_total_cases','cumulative_total_deaths']]
  data_=data_.set_index('date')
  data_.plot(secondary_y=['cumulative_total_deaths'],title=s.upper())
  plt.suptitle('Daily new deaths and cases due to coronavirus')
  plt.show()
  print()

def monthly_compare_deaths(s,big_df):
  '''Generating the new deaths for a country monthly'''

  month=big_df.set_index('date')
  month=month.loc[month['country']==s.lower(),['daily_new_cases','daily_new_deaths']]
  month=month.resample('M').sum()
  month.columns=month.columns.str.replace('daily','monthly')
  month.plot(y='monthly_new_deaths',title=s.upper())
  plt.suptitle('Monthly new deaths due to coronavirus')
  plt.show()
  print()
  return month

def compare_deaths(c1,c2,big_df):
  '''Plotting and comparing the monthly deaths of any two countries'''

  ctry1=monthly_compare_deaths(c1,big_df)
  ctry2=monthly_compare_deaths(c2,big_df)
  ctry1['monthly_new_deaths'].plot(label=c1,color='blue')
  ctry2['monthly_new_deaths'].plot(label=c2,color='red')
  plt.title(f"{c1.upper()} and {c2.upper()}")
  plt.suptitle('Comparing monthly new deaths due to coronavirus')
  plt.xlabel('month')
  plt.legend()
  plt.show()
  print()

def daily_compare_deaths(s,big_df):
  '''generating the data for daily death for a country'''

  month=big_df.set_index('date')
  month=month.loc[month['country']==s.lower(),['daily_new_cases','daily_new_deaths']]
  month.plot(y='daily_new_deaths',title=s.upper())
  plt.suptitle('Daily new deaths due to coronavirus')
  plt.show()
  print()
  return month


def compare_daily_deaths(c1,c2,big_df):
  '''comparing daily deaths of any two countries'''

  ctry1=daily_compare_deaths(c1,big_df)
  ctry2=daily_compare_deaths(c2,big_df)
  ctry1['daily_new_deaths'].plot(label=c1,color='blue')
  ctry2['daily_new_deaths'].plot(label=c2,color='red')
  plt.title(f"{c1.upper()} and {c2.upper()}")
  plt.suptitle('Comparing daily new deaths due to coronavirus')
  plt.xlabel('date')
  plt.legend()
  plt.show()
  print()

def monthly_compare_cases(s,big_df):
  '''monthly new cases for a country'''

  month=big_df.set_index('date')
  month=month.loc[month['country']==s.lower(),['daily_new_cases','daily_new_deaths']]
  month=month.resample('M').sum()
  month.columns=month.columns.str.replace('daily','monthly')
  month.plot(y='monthly_new_cases',title=s.upper())
  plt.suptitle('Monthly new cases due to coronavirus')
  plt.show()
  print()
  return month


def compare_cases(c1,c2,big_df):
  '''comparing monthly new cases of any two country'''

  ctry1=monthly_compare_cases(c1,big_df)
  ctry2=monthly_compare_cases(c2,big_df)
  ctry1['monthly_new_cases'].plot(label=c1,color='blue',subplots=True)
  ctry2['monthly_new_cases'].plot(label=c2,color='red',subplots=True)
  plt.title(f"{c1.upper()} and {c2.upper()}")
  plt.suptitle('Comparing monthly new cases due to coronavirus')
  plt.xlabel('month')
  plt.legend()
  plt.show()
  print()

def daily_compare_cases(s,big_df):
  '''daily new cases for a country'''

  month=big_df.set_index('date')
  month=month.loc[month['country']==s.lower(),['daily_new_cases','daily_new_deaths']]
  month.plot(y='daily_new_cases',title=s.upper())
  plt.suptitle('Daily new cases due to coronavirus')
  plt.show()
  print()
  return month


def compare_daily_cases(c1,c2,big_df):
  '''comparing daily new cases of two countries'''

  ctry1=daily_compare_cases(c1,big_df)
  ctry2=daily_compare_cases(c2,big_df)
  ctry1['daily_new_cases'].plot(label=c1,color='blue')
  ctry2['daily_new_cases'].plot(label=c2,color='red')
  plt.title(f"{c1.upper()} and {c2.upper()}")
  plt.suptitle('Comparing daily new cases due to coronavirus')
  plt.xlabel('date')
  plt.legend()
  plt.show()
  print()

def main_():
  big_df=load_country() #loading the data
  big_df=country_clean(big_df) #cleaning the data

  choi=int(input("1.Reports for a particular country\n2.Reports for comparing two countries\n"))
  if choi==1:
    ctrl=int(input("0.Stop Generating reports for country\n1.Generate plots for another country:-\n"))
    while ctrl==1:

      s=input("Enter the country to generate complete report:-\n").lower()
      selc=int(input("1.Monthly cases and death in the country\n2.daily cases and death in the country\n3.Cumulative data for the country\n"))
      if selc==1:
        monthly_spread(s,big_df) #monthly spread and death for country
      elif selc==2:
        daily_spread(s,big_df) #daily spread and death for country
      elif selc==3:
        cumulative_case_spread_monthly(s,big_df) #cumulative spread and death (monthly) for the country
        cumulative_case_spread_daily(s,big_df) #cumulative spread and death (daily) for the country
      ctrl=int(input("0.Stop Generating reports for country\n1.Generate plots for another country:-\n")) #loop control
    main_()
  elif choi==2:
    ctrl2=int(input("0.Stop Generating reports for comparison\n1.Generate plots for another comparison:-\n"))
    while ctrl2==1:
      c1=input("Enter the country 1:-\n").lower()
      c2=input("Enter the country 2:-\n").lower()
      compare_deaths(c1,c2,big_df)  #monthly death comparison
      compare_daily_deaths(c1,c2,big_df) #daily death comparison
      compare_cases(c1,c2,big_df) #monthly case comparison
      compare_daily_cases(c1,c2,big_df) #daily case comparison
      ctrl2=int(input("0.Stop Generating reports for country\n1.Generate plots for another country")) #loop control
    main_()
  else:
    print("returning back!")

module=int(input("1.Analysis of continent coronavirus dataset\n2.Analysis of countrywise death and cases dataset\n"))
if module==1:
  main()
elif module==2:
  main_()
else:
  print("Invalid Command encountered!")
