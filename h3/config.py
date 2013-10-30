import ConfigParser
import os

'''
modified from author: JohnHBrock@github
'''

def read_config(section_name, item_name):
    '''
    Return config value for given section and item names.
    '''
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg') # should be in same dir
    return config.get(section_name, item_name)
