import requests
import re

from bs4 import BeautifulSoup
from functools import reduce

BASE_URL = 'https://en.wikipedia.org'
RANDOM_PAGE = '/wiki/special:random'
TARGER_PAGE = '/wiki/Philosophy'
ITERATIONS_COUNT = 5

# methods
def print_cycles(cycles, dead_chain_count):
    dead_cycles_percentage = (dead_chain_count / len(cycles)) * 100
    links_to_target_page_percentage = (reduce((lambda total, cycle: total + 1 if TARGER_PAGE in cycle else total), cycles, 0) / len(cycles)) * 100
    
    print('------------------------')
    
    for cycle in cycles:
        print('cycle:')
        
        for link in cycle:
            print('\t' + link)
    
    print('percentage of dead cycles: ', dead_cycles_percentage, '%')
    print('percentage of cycles to ' + TARGER_PAGE + ':', links_to_target_page_percentage, '%')

def crawl_recursively(url, iterations_limit, visited_pages, visit_cycles, dead_chain_count, current_cycle_iteration):
    print('visiting: ', url, 'visited in total:', len(visited_pages), 'cycles count:', len(visit_cycles))

    if iterations_limit < 1: # check on total cycles limit
        return visit_cycles, dead_chain_count

    if current_cycle_iteration == 0: # append a new cycle to a cycles array
        visit_cycles.append([])

    link = find_next_link(url)    

    if not link: # dead chain
        return crawl_recursively(RANDOM_PAGE, iterations_limit - 1, visited_pages, visit_cycles, dead_chain_count + 1, 0)

    href = link.get('href')
    visit_cycles[-1].append(href) # append to a current cycle
    
    if href not in visited_pages:
        visited_pages.append(href) # append to visited pages
        
        return crawl_recursively(href, iterations_limit, visited_pages, visit_cycles, dead_chain_count, current_cycle_iteration + 1)
    else:
        return crawl_recursively(RANDOM_PAGE, iterations_limit - 1, visited_pages, visit_cycles, dead_chain_count, 0)

def find_next_link(url):
    content = requests.get(BASE_URL + url).content # load the page content
    soup = BeautifulSoup(content, features = "html.parser")
    article = soup.find('div', attrs = { 'id': 'bodyContent' }) # find an article body
    
    return article.find('a', attrs = { 'href': re.compile("^/wiki/((?!.*:))((?!.*disambiguation))") }) # find a first link to follow

cycles, dead_chain_count = crawl_recursively(RANDOM_PAGE, ITERATIONS_COUNT, [], [], 0, 0)

print_cycles(cycles, dead_chain_count)
