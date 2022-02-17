class ParamDict(dict):
    def __init__(self, custom_type=None, *args, **kw):
        super().__init__(*args, **kw)
        self.custom_type = custom_type or None

    def __set__(self, instance, value):
        #print('===> set', instance, value)
        self[instance] = self.custom_type(value) if self.custom_type else value

    def __get__(self, instance, owner):
        return self[instance]