from dxfwrite import DXFEngine as dxf

drawing = dxf.drawing('test1.dxf')

drawing.add(dxf.line((0, 0), (0.6, 0)))
drawing.add(dxf.line((0, 0.006), (0.6, 0.006)))
drawing.add(dxf.line((0, 0.012), (0.6, 0.012)))

drawing.save()
