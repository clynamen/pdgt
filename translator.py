
####
# \class translator translate the give text via google
# translate
####

from urllib.parse import urlparse
import urllib.request
import urllib
import re

class Translator:
  ''' translator translate the given text '''

  _user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
  _headers={'User-Agent':_user_agent,}
  _regA = re.compile('(?<=\[\[\[").*')
  _regB = re.compile('.*(?=","",""]])')
  _regC = re.compile('.*(?=",")')

  def __init__(self, inlang, outlang):
    self._inlang = inlang
    self._outlang = outlang

  def _downloadTranslation(self, text):
    text = urllib.parse.quote(text)
    url = 'http://translate.google.com/translate_a/t?client=t&text={0}%0A%0A&hl={2}&sl={1}&tl={2}'.format(
        text,self._inlang,self._outlang)
    request=urllib.request.Request(url,None,Translator._headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    translationPage = data.decode("utf-8")
    return translationPage

  def _parseFirstTranslation(self, translationPage):
    res = Translator._regA.search(translationPage)
    translation = res.group()
    res = Translator._regB.search(translation,0,len(translation)+6)
    translation = res.group()
    res = Translator._regC.search(translation,0,len(translation)+6)
    translation = res.group()
    return translation

  def _parseAlternativeTranslation(self, translationPage):
    res = re.search('(?<=\]\],\[\[").*', translationPage)
    if res == None :
      return ''
    res = re.search('.*(?="\]\]\])', res.group())
    if res == None :
      return ''
    res = re.sub('",\["', ': ', res.group())
    res = re.sub('","', ', ', res)
    alternative = re.sub('"\]\],\["', ' | ', res)
    return alternative

  def translate(self, text):
    translationPage = self._downloadTranslation(text)
    firstTranslation = self._parseFirstTranslation(translationPage)
    alternativeTranslation = self._parseAlternativeTranslation(translationPage)
    if len(alternativeTranslation) != 0 :
      translation = firstTranslation + ' -- ' + alternativeTranslation 
    else:
      translation = firstTranslation
    return translation


