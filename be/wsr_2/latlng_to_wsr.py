from pykml import parser
import shapely
import pathlib

parent = pathlib.Path(__file__).parent.resolve()

with open(str(parent)+'/WRS2_descending.kml') as contents:
    root = parser.parse(contents).getroot()

def getWSR2PathAndRow(lat, lng):
    shPoint = shapely.Point(lng, lat)
    for Placemark in root.Document.Folder.Placemark:
        if not hasattr(Placemark, "Polygon"): continue
        coordinates = Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates
        strpairs = ('' + coordinates).split(' ')
        polygon = list(map(lambda v: list(map(float, v.split(','))), strpairs))
        shPolygon = shapely.Polygon(polygon)
        if (shPoint.within(shPolygon)):
            return [int(Placemark.ExtendedData.SchemaData.SimpleData[6].text),
                int(Placemark.ExtendedData.SchemaData.SimpleData[7].text)]
            


#     getWSR2PathAndRow(0.37116321872081237,-64.75769547006865,root)
