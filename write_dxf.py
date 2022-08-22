from dxfwrite import DXFEngine as dxf

drawing = dxf.drawing('test1.dxf')

drawing.add(dxf.rectangle((0, 0), 20, 20))


drawing.save()
