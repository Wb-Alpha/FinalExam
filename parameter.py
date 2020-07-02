
class Parameter():

    isTabelMode = True
    start_row = 7
    start_column = 0
    end_row = 7
    end_column = 0
    label = ""

    def setParameter(self, isTabel, sr, sc):
        Parameter.isTabelMode = isTabel
        Parameter.start_row = sr
        Parameter.start_column = sc

    def getParameter(self):
        parameter_list = [Parameter.isTabelMode, Parameter.start_row, Parameter.start_column]
        return parameter_list

