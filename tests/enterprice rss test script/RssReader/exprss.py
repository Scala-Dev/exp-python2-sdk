# import libraries
import exp_sdk
import scalalib
import scalatools
from scalalib import sharedvars
import scala5
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment
import tempfile
import os
import re
import urllib

scalaVars = sharedvars()
scala5.ScalaPlayer.Log('Starting EXP data sync')


# download image files
def download_file_from_net(url, filename):
    try:
        temp_dir = tempfile.gettempdir()
        save_dir = os.path.join(temp_dir, filename)
        image = urllib.URLopener()
        image.retrieve(url, save_dir)
        # install to the content folder
        scalalib.install_content(save_dir, subfolder='rss', autostart=False)
        scala5.ScalaPlayer.Log('Image ' + filename + ' downloaded from ' + url)
    except IOError as (errno, strerror):
        scala5.ScalaPlayer.LogExternalError(1000, 'I/O error({0})'.format(errno), strerror)


# get exp data
def get_rss_data():
    feed_data = None

    try:
        # authentication
        exp = exp_sdk.start(uuid=scalaVars.uuid, api_key=scalaVars.api_key, host=scalaVars.host)
        # get feed data from EXP
        feed = exp.get_feed(uuid=scalaVars.feed_uuid)
        feed_data = feed.get_data()
        # stop connection
        exp.stop()
        scala5.ScalaPlayer.Log('Connection to EXP successful data downloaded')
    except exp_sdk.ExpError or exp_sdk.UnexpectedError:
        scala5.ScalaPlayer.LogExternalError(1000, 'ExpError', 'Error downloading data from EXP')
    except exp_sdk.RuntimeError:
        scala5.ScalaPlayer.LogExternalError(1000, 'RuntimeError', 'Please check start options of EXP SDK')
    except exp_sdk.AuthenticationError:
        scala5.ScalaPlayer.LogExternalError(1000, 'AuthenticationError',
                                            'Unable to connect to EXP, please check credentials')
    except exp_sdk.ApiError:
        scala5.ScalaPlayer.LogExternalError(1000, 'ApiError', exp_sdk.ApiError.message)

    return feed_data


# save jSon to XML
def json2xml(json_obj):
    top = Element('rss')
    info = SubElement(top, 'info')
    rss_source = SubElement(info, 'source')
    rss_source.text = json_obj['search']['search']
    rss_build_date = SubElement(info, 'lastBuildDate')
    rss_build_date.text = json_obj['details']['lastBuildDate']
    rss_max_items = SubElement(info, 'maxResults')
    rss_max_items.text = str(json_obj['search']['maxResults'])
    rss_source_name = SubElement(info, 'name')
    rss_source_name.text = json_obj['details']['name']
    rss_items = SubElement(top, 'items')

    for item in json_obj['items']:
        rss_item = SubElement(rss_items, 'item')
        rss_item_title = SubElement(rss_item, 'title')
        rss_item_title.text = item['raw']['title'][0]
        rss_item_text = SubElement(rss_item, 'text')
        rss_item_text.text = re.sub('<[^<]+?>', '', item['text'])
        rss_item_text.text = re.sub('&nbps;', '', rss_item_text.text)
        rss_item_date = SubElement(rss_item, 'date')
        rss_item_date.text = item['date']

        if (len(item['images']) > 0):
            url = item['images'][0]['url']
            filename = item['images'][0]['url'].split('/')[-1]
            rss_item_file = SubElement(rss_item, 'image')
            rss_item_file.text = 'content:\\rss\\' + filename
            download_file_from_net(url, filename)
        elif (len(item['raw']['media:content']) > 0):
            url = item['raw']['media:content'][0]['$']['url']
            filename = item['raw']['media:content'][0]['$']['url'].split('/')[-1]
            rss_item_file = SubElement(rss_item, 'image')
            rss_item_file.text = 'content:\\rss\\' + filename
            download_file_from_net(url, filename)
        elif (len(item['raw']['media:thumbnail']) > 0):
            url = item['raw']['media:thumbnail'][0]['$']['url']
            filename = item['raw']['media:thumbnail'][0]['$']['url'].split('/')[-1]
            rss_item_file = SubElement(rss_item, 'image')
            rss_item_file.text = 'content:\\rss\\' + filename
            download_file_from_net(url, filename)
        else:
            rss_item_file = SubElement(rss_item, 'image')
            rss_item_file.text = ''

    return ET.tostring(top, 'utf-8')


# save xml data to file
def save_data(xml_data):
    try:
        temp_dir = tempfile.gettempdir()
        save_dir = os.path.join(temp_dir, 'rss_data.xml')
        file_ = open(save_dir, 'w')
        file_.write(xml_data)
        file_.close()
        # install to the content folder
        scalalib.install_content(save_dir, subfolder='rss', autostart=True)
        scala5.ScalaPlayer.Log('XML rss data saved in player content directory')
    except IOError as (errno, strerror):
        scala5.ScalaPlayer.LogExternalError(1000, 'I/O error({0})'.format(errno), strerror)


# main program
rss_data = None
rss_data = get_rss_data()
if rss_data:
    xml_data = json2xml(rss_data)
    save_data(xml_data)
scala5.ScalaPlayer.Log('EXP data sync ready')
