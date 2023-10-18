import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
import numpy as np
import argparse
from tqdm import tqdm

def get_description(url):    
    r = requests.get(url)
    html_content = r.text

    soup = BeautifulSoup(html_content,'html.parser')

    comment = soup.find(string=lambda text: isinstance(text,Comment))
    if not comment:
        return np.NaN
    
    parent_element = comment.find_parent()
    p_tag=parent_element.find('p')
    if p_tag:
        text_content = ''.join(p_tag.stripped_strings)
        return text_content

parser = argparse.ArgumentParser()
parser.add_argument("file",help="Csv file with links to the descriptions")
args = parser.parse_args()

if not args.file:
    data = pd.read_csv('./toy_dataset_label.csv',sep='\t',encoding='latin-1')
else: data = pd.read_csv(args.file,sep='\t',encoding='latin-1')


with tqdm(total=len(data)) as pbar:
    for idx in range(data.shape[0]):
        pbar.set_description(f'Art Piece N°: {idx}')
        data['FILE'][idx] = './images/'+str(idx+1)+'.jpg'
        data['URL'][idx] = get_description(data['URL'][idx])
        pbar.update()
data['URL'].replace('', np.NaN, inplace=True)
data['URL'].replace('None', np.NaN,inplace=True)
data.dropna(how='any', inplace=True)

data.to_csv('described_dataset_label.csv',sep='\t', index=False)