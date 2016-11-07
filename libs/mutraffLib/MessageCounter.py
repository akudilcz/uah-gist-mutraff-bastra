'''
Created on 27/09/2016

@author: Alvaro Paricio alvaro.paricio@uah.es
'''
import sys

class MessageCounter:

  # -----------------------------------------
  def __init__(self, id, ):
    self.id = id
    self.counter = 0

  # -----------------------------------------
  def getNewMessageId(self):
    self.counter += 1
    return str(self.id)+"-"+str(self.counter)

