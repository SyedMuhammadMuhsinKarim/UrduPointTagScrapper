class Get_Content:
  def __init__(self, data, tag, attr, attr_value):
    self.data = data
    self.tag = tag
    self.attr = attr
    self.attr_value = attr_value
  
  def content(self):
    return [elem.find(self.tag, attrs={self.attr: self.attr_value}) for elem in self.data]