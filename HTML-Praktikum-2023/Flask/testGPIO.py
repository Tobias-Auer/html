#!/usr/bin/python3

class API:
    def __init__(self, pins):
        self.pins = pins
        self.temp = []
        # print(self.pins)
        for i in range(len(self.pins)):
            print(self.pins[i])


API([["name", "mode"], ["pins", "name"]])
