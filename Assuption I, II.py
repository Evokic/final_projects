import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Assumption I
# read data
def get_percentage(a, b):
    """Calcuate percentage
    :param a: Denominator to calcuate the percentage
           b: Numerator to calcuate the percentage
    :return pec: double
        the percentage of a/b
    >>> a = 2
    >>> b = 4
    >>> get_percentage(a,b)
    0.5
    """
    perc = a/b
    return perc

def state_abbrev(state_name):
    """ change full state name to state abbreviation
    :param state_name: full state name
    :return: abbreviation for each state

    >>> state_name = pd.DataFrame(['Alabama', 'Alaska', 'Arizona'])
    >>> state_abbrev(state_name)
    ['AL', 'AK', 'AZ']
    """
    us_state_abbrev = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
        'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
        'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Northern Mariana Islands': 'MP',
        'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Palau': 'PW', 'Pennsylvania': 'PA',
        'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
        'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virgin Islands': 'VI',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
    }
    return state_name.map(us_state_abbrev)

df = pd.read_excel("Education.xls")

# modify columns
df['Total adults in 1970'] = df['Less than a high school diploma, 1970'] / (df['Percent of adults with less than a high school diploma, 1970']/100)
df['Total adults in 1980'] = df['Less than a high school diploma, 1980'] / (df['Percent of adults with less than a high school diploma, 1980'] / 100)
df['Total adults in 1990'] = df['Less than a high school diploma, 1990'] / (df['Percent of adults with less than a high school diploma, 1990']/100)
df['Total adults in 2000'] = df['Less than a high school diploma, 2000'] / (df['Percent of adults with less than a high school diploma, 2000']/100)
df['Total adults in 2013-17'] = df['Less than a high school diploma, 2013-17'] / (df['Percent of adults with less than a high school diploma, 2013-17']/100)
# United States
FY = ['1970', '1980', '1990', '2000', '2013-17']
all = []
for i in FY:
    less_than_high_school = get_percentage(df['Less than a high school diploma, ' + i].sum(), df['Total adults in ' + i].sum())
    high_school = get_percentage(df['High school diploma only, ' + i].sum(), df['Total adults in ' + i].sum())
    associate = get_percentage(df['Some college (1-3 years), ' + i].sum(), df['Total adults in ' + i].sum())
    college = get_percentage(df['Four years of college or higher, ' + i].sum(),df['Total adults in ' + i].sum())

    all.append([less_than_high_school, high_school, associate, college])

all = np.asarray(all)
label = ['less than a high school', 'high school', ' some college(1-3 years)', 'four years of college or higher']
x = [1970, 1980, 1990, 2000, 2017]
for i in range(4):
    plt.plot(x, all[:,i], label = label[i])
plt.legend()
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Percentage of People receive Degree from 1970 - 2017')
plt.show()

# By States
state = df.groupby('State').sum()[['Less than a high school diploma, 1970', 'High school diploma only, 1970', 'Some college (1-3 years), 1970', 'Four years of college or higher, 1970','Total adults in 1970',
                                 'Less than a high school diploma, 1980', 'High school diploma only, 1980', 'Some college (1-3 years), 1980', 'Four years of college or higher, 1980','Total adults in 1980',
                                 'Less than a high school diploma, 1990', 'High school diploma only, 1990', 'Some college (1-3 years), 1990', 'Four years of college or higher, 1990','Total adults in 1990',
                                 'Less than a high school diploma, 2000', 'High school diploma only, 2000', 'Some college (1-3 years), 2000', 'Four years of college or higher, 2000','Total adults in 2000',
                                 'Less than a high school diploma, 2013-17', 'High school diploma only, 2013-17', 'Some college (1-3 years), 2013-17', 'Four years of college or higher, 2013-17','Total adults in 2013-17']]

for i in FY:
    state['Percentage less_than_high_school ' + i] = get_percentage(state['Less than a high school diploma, ' + i], state['Total adults in ' + i])
    state['Percentage high_school ' + i] = get_percentage(state['High school diploma only, ' + i], state['Total adults in ' + i])
    state['Percentage associate ' + i] = get_percentage(state['Some college (1-3 years), ' + i], state['Total adults in ' + i])
    state['Percentage college ' + i] = get_percentage(state['Four years of college or higher, ' + i], state['Total adults in ' + i])

print(state.head())
# sort by percentage
asc_state_1970 = state.sort_values(by = 'Percentage college 1970', ascending=False)
asc_state_1980 = state.sort_values(by = 'Percentage college 1980', ascending=False)
asc_state_2000 = state.sort_values(by = 'Percentage college 2000', ascending=False)
asc_state_2017 = state.sort_values(by = 'Percentage college 2013-17', ascending=False)

desc_state_1970 = state.sort_values(by = 'Percentage less_than_high_school 1970', ascending=True)
desc_state_1980 = state.sort_values(by = 'Percentage less_than_high_school 1980', ascending=True)
desc_state_1990 = state.sort_values(by = 'Percentage less_than_high_school 1990', ascending=True)
desc_state_2000 = state.sort_values(by = 'Percentage less_than_high_school 2000', ascending=True)
desc_state_2017 = state.sort_values(by = 'Percentage less_than_high_school 2013-17', ascending=True)

# Assumption II
poverty = pd.read_csv("poverty.csv", dtype={"Total":'Int64', "Number":"Int64"})
poverty['Percentage'] = get_percentage(poverty['Number'], poverty['Total'])

year = [1980, 1990, 2000, 2010, 2017]
pov_perc = []
for y in year:
    pov_perc.append(get_percentage(poverty[poverty['Year'] == y]['Number'].sum(),poverty[poverty['Year'] == y]['Total'].sum()))

plt.plot(year, pov_perc)
plt.xticks([1980, 1990, 2000, 2010, 2017])
plt.xlabel('Year')
plt.ylabel("Percentage")
plt.title('Percentage of Poverty Population 1980 - 2017')
plt.show()

FY13_17 = poverty[(poverty['Year'] >= 2013) &(poverty['Year'] <= 2017)]

edu_perc = state[['Percentage less_than_high_school 1970', 'Percentage high_school 1970',
       'Percentage associate 1970', 'Percentage college 1970',
       'Percentage less_than_high_school 1980', 'Percentage high_school 1980',
       'Percentage associate 1980', 'Percentage college 1980',
       'Percentage less_than_high_school 1990', 'Percentage high_school 1990',
       'Percentage associate 1990', 'Percentage college 1990',
       'Percentage less_than_high_school 2000', 'Percentage high_school 2000',
       'Percentage associate 2000', 'Percentage college 2000',
       'Percentage less_than_high_school 2013-17',
       'Percentage high_school 2013-17', 'Percentage associate 2013-17',
       'Percentage college 2013-17']]

FY13_17 = poverty[(poverty['Year'] >= 2013) &(poverty['Year'] <= 2017)]

FY13_17['Perc'] = FY13_17.loc[:,'Number'] / FY13_17.loc[:,'Total']
plt.hist(FY13_17['Perc'], 20, facecolor='blue', alpha=0.5)
plt.axvline(FY13_17['Perc'].mean(), color='k', linestyle='dashed', linewidth=1)
plt.xlabel('Poverty Percentage')
plt.ylabel('Occurance')
plt.title('Poverty Percentage Histogram')
plt.show()

poverty_state = FY13_17.groupby('STATE').agg('sum')[['Total', 'Number']]
poverty_state['perc']  = get_percentage(poverty_state['Number'],poverty_state['Total'])

poverty_state['State'] = poverty_state.index
poverty_state['abbre'] = state_abbrev(poverty_state['State'])
poverty_state = poverty_state.set_index('abbre').sort_index(axis = 0)
edu_perc = edu_perc.drop(['PR', 'US'])

plt.scatter(poverty_state['perc'], edu_perc['Percentage college 2013-17'])
plt.xlabel('Poverty Percentage')
plt.ylabel('College Degree Percentage')
plt.title("Plot Poverty by College Degree")
plt.show()

plt.scatter(poverty_state['perc'], edu_perc['Percentage less_than_high_school 2013-17'])
plt.xlabel('Poverty Percentage')
plt.ylabel('Less than High School Degree Percentage ')
plt.title("Plot Poverty by Less than High School Degree")
plt.show()

plt.scatter(poverty_state['perc'], edu_perc['Percentage associate 2013-17'])
plt.xlabel('Poverty Percentage')
plt.ylabel('Associate Degree Percentage ')
plt.title("Plot Poverty by Associate Degree")
plt.show()

plt.scatter(poverty_state['perc'], edu_perc['Percentage high_school 2013-17'])
plt.xlabel('Poverty Percentage')
plt.ylabel('High School Degree Percentage ')
plt.title("Plot Poverty by High School Degree")
plt.show()

from scipy.stats import pearsonr
print(pearsonr(poverty_state['perc'], edu_perc['Percentage high_school 2013-17']))
print(pearsonr(poverty_state['perc'], edu_perc['Percentage less_than_high_school 2013-17']))
print(pearsonr(poverty_state['perc'], edu_perc['Percentage college 2013-17']))
print(pearsonr(poverty_state['perc'], edu_perc['Percentage associate 2013-17']))