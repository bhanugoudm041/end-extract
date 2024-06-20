from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from optparse import OptionParser 
import time
import re

#Chrome options
chrome_options = Options()
chrome_options.binary_location = '/usr/bin/chromium'
chrome_options.add_argument("--headless")

#url options
opt=OptionParser()
opt.add_option("-u", "--url", dest="url")
(options, args) = opt.parse_args()
#url empty check
if options.url == None:
        print("Please enter a url to fetch")
else:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(options.url)
        #javascript to load
        script="""(function(){var scripts=document.getElementsByTagName("script"),regex=/(?<=(\"|\'|\`))\/[a-zA-Z0-9_?&=\/\-\#\.]*(?=(\"|\'|\`))/g;const results=new Set;for(var i=0;i<scripts.length;i++){var t=scripts[i].src;""!=t&&fetch(t).then(function(t){return t.text()}).then(function(t){var e=t.matchAll(regex);for(let r of e)results.add(r[0])}).catch(function(t){console.log("An error occurred: ",t)})}var pageContent=document.documentElement.outerHTML,matches=pageContent.matchAll(regex);for(const match of matches)results.add(match[0]);function writeResults(){results.forEach(function(t){document.write(t+"<br>")})}setTimeout(writeResults,3e3);})();"""
        driver.execute_script(script)
        time.sleep(5)
        #output in html
        html_content=driver.page_source
        #regex to filter out enpoints
        pattern = r'<body>(.*?)<br>|<br>(.*?)<br>'
        matches = re.findall(pattern, html_content)
        matches = re.findall(pattern, html_content, re.DOTALL)
        content_list = [item for sublist in matches for item in sublist if item]
        #final urls as result with enpoints
        for content in content_list:
                print(options.url+content.strip())
