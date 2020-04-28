import numpy as np
import datetime
#from pylab import *
#import random
from pylab import mpl
from matplotlib import pyplot as plt
from wotan import flatten
from betellib import build_string, get_mags_from_AAVSO
import requests
from bs4 import BeautifulSoup
from astropy.stats import biweight_location

#def conf_zh(font_name):
 #   from pylab import mpl
  #  mpl.rcParams['font.sans-serif'] = [font_name]
   # mpl.rcParams['axes.unicode_minus'] = False 

def make_plot(days_ago, dates, mag):
    print('Making plot...')
    time_span = np.max(dates) - np.min(dates)
    flatten_lc, trend_lc = flatten(
        days_ago,
        mag,
        method='lowess',
        window_length=time_span/5,
        return_trend=True,
        )
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif']=['Droid Sans Fallback,DejaVu Sans']    #指定默认字体 SimHei为黑体
    plt.rcParams['axes.unicode_minus']=False   #用来正常显示负号
    plt.scatter(days_ago, mag, s=5, color='blue', alpha=0.5)
    plt.scatter(days_ago1, all_mags1, s=10, color='black', alpha=0.8, marker="x")
    plt.xlabel(r'从今天往回数的天数')
    plt.ylabel(r'视星等')
    mid = 1.10
    plt.ylim(mid-1, mid+1)
    plt.xlim(-1, 20)
    plt.plot(days_ago, trend_lc, color='red', linewidth=1)
    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()
    date_text = datetime.datetime.now().strftime("%Y-%m-%d")
    data_last24hrs = np.where(days_ago<1)
    mean_last24hrs = biweight_location(mag[data_last24hrs])
    lumi = str(format(mean_last24hrs, '.2f'))
    plt.text(19.5, mid+1-0.25, u"AAVSO 观测星等(肉眼) 蓝色·", color='blue')
    plt.text(19.5, mid+1-0.15, r"AAVSO 观测星等(CCD) 黑色×", color='black')
    plt.text(19.5, mid+1-0.05, r"局部加权拟合 红色线", color='red')
    plt.text(19.5, mid-1+0.1, r'#参宿四的亮度为 ' + lumi + r" 等，于 " + date_text + r" 由 天文通 用 @betelbot 生成")
    plt.savefig(plot_file, bbox_inches='tight', dpi=300)
    print('Done.')


def get_mags_from_AAVSO_V(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    rows = soup.select('tbody tr')
    dates = []
    mags = []
    for row in rows:
        string = '' + row.text
        string = string.split('\n')
        try:
            date = float(string[3])
            mag = float(string[5])
            band = string[7]
            #print(date, mag, band)
            if band == "V":
                dates.append(date)
                mags.append(mag)
                #print(date, mag)
            #print(mag)
        except:
            pass
    return np.array(dates), np.array(mags)


# CCDs
url_base = 'https://www.aavso.org/apps/webobs/results/?star=betelgeuse&num_results=200&obs_types=dslr+ptg+pep+ccd+visdig&page='
baseline_mag = 0.5
pages = np.arange(1, 2, 1)
all_dates1 = np.array([])
all_mags1 = np.array([])
for page in pages:
    url = url_base + str(page)
    #print(url)
    dates, mags = get_mags_from_AAVSO_V(url)
    print(dates, mags)
    all_dates1 = np.concatenate((all_dates1, dates))
    all_mags1 = np.concatenate((all_mags1, mags))
    
days_ago1 = np.max(all_dates1) - all_dates1
print(all_dates1, all_mags1)



# Pull the last 10 pages from AAVSO and collate the dates and mags
plot_file = 'plot20d.png'
url_base = 'https://www.aavso.org/apps/webobs/results/?star=betelgeuse&num_results=200&obs_types=vis&page='
pages = np.arange(1, 10, 1)
all_dates = np.array([])
all_mags = np.array([])
for page in pages:
    url = url_base + str(page)
    print(url)
    dates, mags = get_mags_from_AAVSO(url)
    all_dates = np.concatenate((all_dates, dates))
    all_mags = np.concatenate((all_mags, mags))
dates = all_dates
mags = all_mags
days_ago = np.max(dates) - dates
text = build_string(days_ago, mags)
#if __name__ == "__main__":
 #   conf_zh("Droid Sans Fallback")
make_plot(days_ago, dates, mags)
